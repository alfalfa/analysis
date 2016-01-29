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
 
def get_filenames_list(directory_path):
    filenames_list = []
    for dirpath,_,filenames in os.walk(directory_path):
        for f in filenames:
            filenames_list.append(os.path.abspath(os.path.join(dirpath, f)))
    return filenames_list

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
        raise ValueError("Usage: python plot-inter-frame-delay.py frame_stats_directory")
    frame_stats_directory = sys.argv[1]
    _, dataset_title  = os.path.split(os.path.abspath(frame_stats_directory))

    inter_frame_delays_list = []
    resume_delays_list = []
    rebuffering_ratios = []
    num_files_parsed = 0
    for f in get_filenames_list(frame_stats_directory):
        match_object = re.search("frame-stats.dat", f)
        if match_object: # maybe change this to simpler match
            print("parsing " + f)
            num_files_parsed += 1
            with open(f) as frame_stats_file:
                total_playback_time = 0
                rebuffering_time = 0
                first_line = True
                for line in frame_stats_file:
                    if first_line:
                        string_match = re.search("first chunk request logged on server at ([0-9]+\.[0-9]+)", line)
                        if string_match is None:
                            print("Failed to parse chunk request time from first line: " + line)
                        previous_system_time = float(string_match.group(1))
                        previous_frame_shown = -100
                        first_line = False
                        continue

                    string_match = re.search("displayed at system time ([0-9\.]+) ", line)
                    if string_match is None:
                        print("Failed to parse system time from: " + line)
                    system_time = float(string_match.group(1))

                    string_match = re.search("which is frame ([0-9]+)", line)

                    if string_match is None:
                        print("Failed to parse frame number from: " + line)
                    frame_shown = int(string_match.group(1))

                    time_since_last_frame = system_time - previous_system_time
                    assert(time_since_last_frame > -1)

                    # make sure time is non-decreasing (this shows up a couple times probably because of NTP,
                    # also for first frame display time with margin of error from first chunk request)
                    if time_since_last_frame < 0:
                        time_since_last_frame = 0

                    if (frame_shown - previous_frame_shown) > 24: # consider a seek if move forward >1s in video, this also includes first frame played
                        resume_delays_list.append(time_since_last_frame)
                    else:
                        inter_frame_delays_list.append(time_since_last_frame)
                        total_playback_time += time_since_last_frame
                        if time_since_last_frame > .1:
                            rebuffering_time += time_since_last_frame


                    previous_system_time = system_time
                    previous_frame_shown = frame_shown

                rebuffering_ratios.append(rebuffering_time / total_playback_time)

    if num_files_parsed is 0:
        raise ValueError("Found no frame-stats.dat files to parse")
    else:
        print("Finished parsing " + str(num_files_parsed) + " files")
    chart_directory = 'charts/'

    total_playback_time = sum( inter_frame_delays_list )
    xvals = np.sort( inter_frame_delays_list )
    yvals = []
    subtotal_playback_time = total_playback_time
    for ifd in xvals:
        subtotal_playback_time -= ifd
        yvals.append( subtotal_playback_time / total_playback_time)

    plt.plot( xvals, yvals )

    plt.title("Proportion of total playback time with inter-frame delays less than..\n" + dataset_title +" ("+ str(len(xvals))+" datapoints)")
    plt.xlabel('Inter-frame delay (seconds)')
    plt.ylim(0,1)
    #plt.yscale('log')
    filename = chart_directory + dataset_title + "-proportional-playback"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename + "..")
    plt.savefig(filename)
    plt.clf()

    (xvals, yvals) = get_cdf( inter_frame_delays_list )
    yvals = 1-yvals # CCDF
    plt.plot( xvals, yvals )

    plt.title("CCDF of all inter-frame delays\n" + dataset_title +" ("+ str(len(xvals))+" datapoints)")
    plt.xlabel('Inter-frame delay (seconds)')
    plt.yscale('log')

    # mark 1/24s on chart
    #plt.xlim((-1./24.))
    #locs, labels = plt.xticks()
    #locs[0] = (1./24.)
    #plt.xticks(locs)

    #plt.axvline(x=1./24., ls=':', c='black')

    filename = chart_directory + dataset_title + "-inter-frame-delays-ccdf"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename +"..")
    plt.savefig(filename)
    plt.clf()

    (xvals, yvals) = get_cdf( resume_delays_list )
    plt.plot( xvals, yvals )
    plt.title("CDF of seek delays\n" + dataset_title +" ("+ str(len(xvals))+" datapoints)")
    plt.xlabel('Resume duration (seconds)')
    filename = chart_directory + dataset_title + "-resume-delays-cdf"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename +"..")
    plt.savefig(filename)
    plt.clf()

    (xvals, yvals) = get_cdf( rebuffering_ratios )
    plt.plot( xvals, yvals )
    plt.title("CDF rebuffering ratios\n" + dataset_title +" ("+ str(len(xvals))+" runs)")
    plt.xlabel('Rebuffering ratio')
    filename = chart_directory + dataset_title + "-rebuffering-ratios-cdf"
    write_points_to_file(xvals, yvals, filename)
    filename += ".svg"
    print("Writing " + filename +"..")
    plt.savefig(filename)
    plt.clf()

if __name__ == '__main__':
  main()
