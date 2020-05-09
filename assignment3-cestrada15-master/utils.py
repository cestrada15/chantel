"""
Utility Functions
-------------------------------
Helper functions in general.

Usage:
import utils

for number in utils.progressbar(range(100)):
    result += number ** number
"""

import sys


def progressbar(it, prefix="", size=60, file=sys.stdout):
    """
    Progress bar function for long processes.
    it      : iterator
    prefix  : custom string to add on progress bar.
    size    : size of the progress bar
    file    : where the progress bar runs.
    For more information, check the original answer from
    stackoverflow, https://stackoverflow.com/a/34482761.
    """
    count = len(it)

    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()
