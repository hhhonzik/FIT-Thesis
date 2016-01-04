# -*- coding: utf-8 -*-
"""
Definition of Export class
"""

__author__ = 'stepaj27'

import app.utils.console as console
import json
import os
import shutil
import scipy.misc as misc


def computemeta(src, dst):
    """
    This method returns an array we use in our player. It has the order
    of args same as  Canvas.prototype.drawImage for better
    handling on frontend

    :param src: source image
    :param dst: alloc position
    :return: [
            positionX,
            positionY,
            width,
            height,
            sourceX,
            sourceY,
            sourcePositionX,
            sourcePositionY
        ]
    """
    srcy, srcx = src
    canvasx, canvasy = srcx.start, srcy.start
    width, height = srcx.stop - srcx.start, srcy.stop - srcy.start
    posy, posx = dst
    return [posx, posy, width, height, canvasx, canvasy]

class Export(object):
    """
    Export class
    """
    def __init__(self, outputPath):
        """
        :param outputPath: path to a dir where I can export
        :return: self
        """
        self.path = outputPath

        # try write permissions at outputPath
        try:
            os.makedirs(outputPath)
            open(os.path.join(outputPath, 'packed.png'), 'w')
        except FileExistsError:
            pass
        except PermissionError:
            console.error('Unable to write to %s' % outputPath)
        try:
            os.makedirs(os.path.join(outputPath, 'example/'))
        except FileExistsError:
            pass

    def process(self, canvasimg, images, img_areas, allocs):
        """
        :param canvasimg: packed canvas img
        :param images: frames of animation
        :param img_areas: changes
        :param allocs: position of changes
        :return:
        """
        imgpath = os.path.join(self.path, "packed.png")
        # save packed image
        misc.imsave(imgpath, canvasimg)

        # try pngquant
        # Don't completely fail if we don't have pngcrush
        if os.system("pngquant --ext=.png --force %s" % imgpath) != 0:
            console.warn(
                "pngquant not found",
                'Try installing pngquant for better results (http://pngquant.org/)'
            )

        # Generate JSON to represent the data
        timeline = []
        for i in range(len(images)):
            src_rects = img_areas[i]
            dst_rects = allocs[i]

            blitlist = []

            for j in range(len(src_rects)):
                assert isinstance(j, object)
                metadata = computemeta(src_rects[j], dst_rects[j])
                blitlist.append(metadata)

            timeline.append(blitlist)

        metadata = {}
        metadata['size'] = {
            "width": timeline[0][0][2],
            "height": timeline[0][0][3]
        }
        metadata['frames'] = timeline
        filemeta = open(os.path.join(self.path, "timeline.json"), 'wb')
        timeline = json.dumps(metadata, filemeta)
        filemeta.write(bytes(timeline, 'UTF-8'))
        filemeta.close()

        filemeta = open(os.path.join(self.path, 'example/example.timeline.js'), 'wb')
        filemeta.write(bytes("_timeline = ", 'UTF-8'))
        timeline = json.dumps(metadata, filemeta)
        filemeta.write(bytes(timeline, 'UTF-8'))
        filemeta.close()

        shutil.copyfile(
            os.path.join(
                os.path.split(os.path.abspath(os.path.dirname(__file__)))[0],
                './player/example.html'
            ),
            os.path.join(self.path, 'example/example.html')
        )

        shutil.copyfile(
            os.path.join(
                os.path.split(os.path.abspath(os.path.dirname(__file__)))[0],
                '../../player/dist/jquery.html5anim.min.js'
            ),
            os.path.join(self.path, 'example/jquery.html5anim.min.js')
        )

        console.success('Animation generated.', 'Check out output path: %s' % self.path)
