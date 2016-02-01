from __future__ import print_function
import os
import sys
import re
import pprint
import math
from decimal import *
import matplotlib
matplotlib.use('pdf') # Must be before importing matplotlib.pyplot or pylab! Default uses x window manager and won't work cleanly in cloud installations.
from matplotlib import collections
import numpy as np
import pylab
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import directory_traversal_helper

def get_inverse_complement( vals ):
    ret = []
    for val in vals:
        assert(1.- val >= 0)
        if (1.- val) == 0:
            ret.append(100000000)
        else:
            ret.append(1. / (1. - val ) )
    return ret

def get_cdf( unsorted_vals ):
    xvals = np.sort( unsorted_vals )
    yvals = (np.arange(len(xvals)) + 1)/float(len(xvals)) # range from 1 / len(xvals) to 1 inclusive
    return (xvals, yvals)

def write_points_to_file(xvals, yvals, filename):
    print("Writing " + filename +".txt..")
    with open(filename + ".txt", 'w') as dataset:
        for pair in zip(xvals, yvals):
            print(pair, file=dataset)

def main():
    if len( sys.argv ) is not 2:
        raise ValueError("Usage: python plot-ssim-stats.py frame_stats_directory")
    frame_stats_directory = sys.argv[1]
    _, dataset_title  = os.path.split(os.path.abspath(frame_stats_directory))

    per_trial_min_ssim_scores = []
    all_ssim_scores = []

    for f, _ in directory_traversal_helper.get_files_matching_regex(frame_stats_directory, "frame-stats.dat"):
        print("parsing " + f)
        with open(f) as frame_stats_file:
            trial_ssim_scores = []
            for line in frame_stats_file:
                if re.search("first chunk request logged on server at ", line):
                    continue #ignore first line
                string_match = re.search("ssim score ([0-9\.]+)", line)
                if string_match is None:
                    print("Failed to parse ssim from line: " + line)
                ssim_of_frame = float(string_match.group(1))
                trial_ssim_scores.append(ssim_of_frame)

            per_trial_min_ssim_scores.append(min(trial_ssim_scores))
            all_ssim_scores += trial_ssim_scores
    if not all_ssim_scores:
        raise Exception("Couldn't parse any ssim values from " + frame_stats_directory)


    chart_directory = 'charts/'

    (xvals, yvals) = get_cdf( all_ssim_scores )
    plt.plot( xvals, yvals )
    plt.title("CDF of frame SSIM scores\n" + dataset_title +" ("+ str(len(xvals))+" datapoints)")
    plt.xlabel('SSIM score')
    filename = chart_directory + dataset_title + "-ssim-cdf"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename +"..")
    plt.savefig(filename)
    plt.clf()

    (xvals, yvals) = get_cdf( get_inverse_complement( all_ssim_scores) )
    plt.plot( xvals, yvals )
    plt.title("CDF of 1 / ( 1 - SSIM ) values \n" + dataset_title +" ("+ str(len(xvals))+" datapoints)")
    plt.xlabel('1/(1 - SSIM score)')
    plt.xlim(1, 100)
    filename = chart_directory + dataset_title + "-inverse-complement-ssim-cdf"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename +"..")
    plt.savefig(filename)
    plt.clf()

    (xvals, yvals) = get_cdf( per_trial_min_ssim_scores )
    plt.plot( xvals, yvals )
    plt.title("CDF of minimum SSIM scores in a run\n" + dataset_title +" ("+ str(len(xvals))+" datapoints)")
    plt.xlabel('Minimum SSIM score')
    filename = chart_directory + dataset_title + "-min-ssim-cdf"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename +"..")
    plt.savefig(filename)
    plt.clf()

    #analysis_directory = 'analysis/'
    #SSIM_mean_stddev_output_filename = dataset_title + "-mean_stddev_SSIM.txt"
    #SSIM_mean_stddev_output_file = open(analysis_directory + SSIM_mean_stddev_output_filename, 'w')

    #mean_ssims = [ tup[0] for tup in trial_to_ssim_stats.values() ]
    #mean_of_mean_SSIM = np.mean(mean_ssims)
    #stddev_across_mean_SSIM = np.std(mean_ssims)

    #print("Mean of SSIM Means: " + str(mean_of_mean_SSIM), file=SSIM_mean_stddev_output_file)
    #print("Standard Deviation Across SSIM Means: " + str(stddev_across_mean_SSIM), file=SSIM_mean_stddev_output_file)

    #min_ssims = [ tup[2] for tup in trial_to_ssim_stats.values() ]
    #mean_of_min_SSIM = np.mean(min_ssims)
    #stddev_across_min_SSIM = np.std(min_ssims)
    #print("Mean Across Minimum SSIMs: " + str(mean_of_min_SSIM), file=SSIM_mean_stddev_output_file)
    #print("Standard Deviation Across Minimum SSIMs: " + str(stddev_across_min_SSIM), file=SSIM_mean_stddev_output_file)
    #for trial_id in trial_to_ssim_stats:
    #    print("Trial " + trial_id + ":", file=SSIM_mean_stddev_output_file)
    #    (mean_SSIM, stddev_SSIM, min_SSIM) = trial_to_ssim_stats[trial_id]
    #    print("\tMean SSIM: " + str(mean_SSIM), file=SSIM_mean_stddev_output_file)
    #    print("\tStdDev SSIM: " + str(stddev_SSIM), file=SSIM_mean_stddev_output_file)
    #    print("\tMinimum SSIM: " + str(min_SSIM), file=SSIM_mean_stddev_output_file)



if __name__ == '__main__':
  main()
