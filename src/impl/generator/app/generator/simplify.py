"""
Implementation of Allocator class that helps Generater.
"""


def slice_size(positionx, positiony):
    """
    :param positionx: start and stop of x axis
    :param positiony: start and stop of y axis
    :return: integer size in pixels
    """
    return (positionx.stop - positionx.start) * (positiony.stop - positiony.start)

def combine_slices(firstposx, firstposy, secondposx, secondposy):
    """
    This function tries to combine 2 shapes
    :return: area where those 2 slices are
    """
    return (slice(min(firstposx.start, secondposx.start), max(firstposx.stop, secondposx.stop)),
            slice(min(firstposy.start, secondposy.start), max(firstposy.stop, secondposy.stop)))

def slices_intersect(firstposx, firstposy, secondposx, secondposy):
    """
    Function returns if 2 slices intersect or not
    """
    if firstposx.start >= secondposx.stop or \
        secondposx.start >= firstposx.stop:
        return False
    if firstposy.start >= secondposy.stop or \
        secondposy.start >= firstposy.stop:
        return False
    return True


# args bitmap, used_rows, packed, src, sx, sy, w, h
# def find_matching_rect():
#     """
#     This function tries to find if this shape is in the canvas already.
#     This should be implemented in much faster way, because naive algorithms are very slow.
#
#     See also: http://stackoverflow.com/questions/7670112/finding-a-subimage-inside-a-numpy-image
#     :return:
#     """
#     return None

def slice_tuple_size(shape):
    """
    :param s: slice
    :return: computed slice size
    """
    positionx, positiony = shape
    return (positionx.stop - positionx.start) * (positiony.stop - positiony.start)

def simplify(boxes, tolerance=0):
    """
    This function tries to combie large set of rectangles to smaller ones based on tolerance.

    :param boxes: array of frames
    :param tolerance: maximum distance between slices if they will merge or not
    :return:
    """
    out = []
    for posx, posy in boxes:
        shapesize = slice_size(posx, posy)
        did_combine = False
        for i in range(len(out)):
            secondposx, secondposy = out[i]
            combinedx, combinedy = combine_slices(posx, posy, secondposx, secondposy)
            secondshapesize = slice_size(secondposx, secondposy)
            if slices_intersect(posx, posy, secondposx, secondposy) or \
                    (slice_size(combinedx, combinedy) <= shapesize + secondshapesize + tolerance):
                # its better if slices are combined
                out[i] = (combinedx, combinedy)
                did_combine = True
                break
        if not did_combine:
            out.append((posx, posy))

    if tolerance != 0:
        return simplify(out, 0)
    else:
        return out
