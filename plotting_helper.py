from __future__ import print_function
import os
import numpy as np

def get_cdf( unsorted_vals ):
    xvals = np.sort( unsorted_vals )
    yvals = (np.arange(len(xvals)) + 1)/float(len(xvals)) # range from 1 / len(xvals) to 1 inclusive
    return (xvals, yvals)

def write_points_to_file(xvals, yvals, filename):
    chart_directory = 'charts/'
    if not os.path.isdir(chart_directory):
        os.mkdir(chart_directory) # TODO data_directory
    data_directory = 'charts/data/'
    if not os.path.isdir(data_directory):
        os.mkdir(data_directory)

    print("Writing " + data_directory + filename +"..")
    with open(data_directory + filename, 'w') as outfile:
        for (x, y) in zip(xvals, yvals):
            print(str(x) + ", " + str(y), file=outfile)
