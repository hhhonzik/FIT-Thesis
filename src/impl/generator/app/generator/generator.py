# -*- coding: utf-8 -*-
"""
Definition of a Generator class
"""
__author__ = 'stepaj27'

from time import time

from numpy import sign, shape, uint8, zeros
import scipy.ndimage.measurements as me

from app.generator.allocator import Allocator2D
import app.utils.console as console
from app.generator.simplify import simplify, slice_tuple_size


SIMPLIFICATION_TOLERANCE = 512
MAX_PACKED_HEIGHT = 1000000



class Generator(object):

    """
    Implementation of generator algorithm
    """
    def __init__(self, images):
        self.images = images
        self.talk = False


    # pylint: disable=invalid-name,unused-variable,too-many-locals
    def generate(self, export):
        """
        Generate from self.images[] animation and send it to export
        :param export: Export class
        :return:
        """
        zero = self.images[0] - self.images[0]
        pairs = zip([zero] + self.images[:-1], self.images)
        diffs = [sign((b - a).max(2)) for a, b in pairs]

        if self.talk:
            console.warn("Looking for diffs")
        # Find different objects for each frame
        img_areas = [me.find_objects(me.label(d)[0]) for d in diffs]

        # Simplify areas
        img_areas = [simplify(x, SIMPLIFICATION_TOLERANCE) for x in img_areas]

        if self.talk:
            console.warn("Areas found and simplified")

        ih, iw, _ = shape(self.images[0])

        # Generate a packed image
        allocator = Allocator2D(MAX_PACKED_HEIGHT, iw)
        packed = zeros((MAX_PACKED_HEIGHT, iw, 3), dtype=uint8)


        # Sort the rects to be packed by largest size first, to improve the packing
        rects_by_size = []
        for i in range(len(self.images)):
            src_rects = img_areas[i]
            for j in range(len(src_rects)):
                rects_by_size.append((slice_tuple_size(src_rects[j]), i, j))
        rects_by_size.sort(reverse=True)

        if self.talk:
            console.warn("Areas sorted by size")


        allocs = [[None] * len(src_rects) for src_rects in img_areas]

        console.warn(
            "Packing",
            "num rects: {0} num frames: {1}".format(
                len(rects_by_size),
                len(self.images)
            )
        )
        t0 = time()
        counter = 0
        for size, i, j in rects_by_size:
            src = self.images[i]
            src_rects = img_areas[i]

            a, b = src_rects[j]
            sx, sy = b.start, a.start
            w, h = b.stop - b.start, a.stop - a.start

            # finding matching rectangle is very expensive and its disabled for now.
            # existing = find_matching_rect(
            #  allocator.bitmap,
            #  allocator.num_used_rows,
            #  packed,
            #  src,
            #  sx,
            #  sy,
            #  w,
            #  h
            # )
            # if existing:
            #     dy, dx = existing
            #     allocs[i][j] = (dy, dx)
            # else:
            counter += 1
            if self.talk:
                console.warn("Allocation area ({0}/{1}): ".format(
                    counter,
                    len(rects_by_size)
                ), "{0}x{1} ({2})".format(i, j, size))

            dy, dx = allocator.allocate(w, h)
            allocs[i][j] = (dy, dx)
            packed[dy:dy+h, dx:dx+w] = src[sy:sy+h, sx:sx+w]

        console.success("Packing finished", "took: %s" % (time() - t0))

        packed = packed[0:allocator.num_used_rows]
        export.process(packed, self.images, img_areas, allocs)


