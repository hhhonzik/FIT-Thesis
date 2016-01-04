"""
Implementation of Allocator class that helps Generater.
"""
from numpy import zeros, shape, uint32, uint8


class Allocator2D:
    """
    Allocator module
    """
    def __init__(self, rows, cols):
        self.bitmap = zeros((rows, cols), dtype=uint8)
        self.available_space = zeros(rows, dtype=uint32)
        self.available_space[:] = cols
        self.num_used_rows = 0

    def allocate(self, width, height):
        """
        :param width: Width of allocated area
        :param height: Heihgt of allocated area
        :return: position on allocated area where is still some space
        """
        canvasheight, canvaswidth = shape(self.bitmap)

        for row in range(canvasheight - height + 1):
            if self.available_space[row] < width:
                continue

            for col in range(canvaswidth - width + 1):
                if self.bitmap[row, col] == 0:
                    if not self.bitmap[row:row+height, col:col+width].any():
                        self.bitmap[row:row+height, col:col+width] = 1
                        self.available_space[row:row+height] -= width
                        self.num_used_rows = max(self.num_used_rows, row + height)
                        return row, col
        raise RuntimeError("Final image would be too big. Aborting.")
