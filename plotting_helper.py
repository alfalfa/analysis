import os
import numpy as np

def get_cdf( unsorted_vals ):
    xvals = np.sort( unsorted_vals )
    yvals = (np.arange(len(xvals)) + 1)/float(len(xvals)) # range from 1 / len(xvals) to 1 inclusive
    return (xvals, yvals)

def write_points_to_file(xvals, yvals, dataset_title, filename):
    chart_directory = 'charts/'
    if not os.path.isdir(chart_directory):
        os.mkdir(chart_directory)

    per_dataset_directory = chart_directory + dataset_title +"/"
    if not os.path.isdir(per_dataset_directory):
        os.mkdir(per_dataset_directory)

    datapoints_directory = per_dataset_directory + 'datapoints/'
    if not os.path.isdir(datapoints_directory):
        os.mkdir(datapoints_directory)

    print("Writing " + datapoints_directory + filename)
    with open(datapoints_directory + filename, 'w') as outfile:
        for (x, y) in zip(xvals, yvals):
            outfile.write(str(x) + "  " + str(y) + "\n")
