from __future__ import print_function
import os
import shutil
import sys
import multiprocessing
from multiprocessing import Pool
import re
import collections
from collections import defaultdict
import pprint
import math
from decimal import *
from datetime import datetime
#getcontext().prec = 6 # the precision of our get time syscall

def get_filenames_list(directory_path):
    filenames_list = []
    for dirpath,_,filenames in os.walk(directory_path):
        for f in filenames:
            filenames_list.append(os.path.abspath(os.path.join(dirpath, f)))
    return filenames_list

# map takes only one argument so use a five-tuple as input
def parse_logs_for_trial((trial_id, youtube_log_filename, stall_log_filename, video_stats_lookup_maps, output_directory)):
    output_filename = output_directory + "/" + trial_id + "/" + "frame-stats.dat"
    with open(output_filename, 'w') as output_file, open(youtube_log_filename) as youtube_logfile, open(stall_log_filename) as stall_logfile:
        resolution_of_frame = defaultdict(int)
        first_line = True
        for line in youtube_logfile:
            # We want to track the time of the first request to youtube server
            if first_line:
                timestamp_string = re.split(" \t", line, maxsplit=1)[0] #match up to first tab
                datetime_of_first_chunk_request = datetime.strptime(timestamp_string, "%a %b %d %H:%M:%S %Y")
                assert(timestamp_string == datetime_of_first_chunk_request.ctime())
                first_request_time_string = "first chunk request logged on server at "

                first_time_request = (datetime_of_first_chunk_request - datetime.utcfromtimestamp(0)).total_seconds()
                first_request_time_string += str(first_time_request + 1) # add one second to account for roundoff error
                print(first_request_time_string, file=output_file)
                first_line = False
            resolution = re.search("[0-9]+x([0-9]+)", line).group(1)
            byte_range_start = int(re.search("([0-9]+)-[0-9]+", line).group(1))
            byte_range_end = int(re.search("[0-9]+-([0-9]+)", line).group(1))

            assert(resolution in video_stats_lookup_maps)
            (byte_offset_to_frame_index, frame_index_to_ssim) = video_stats_lookup_maps[resolution]
            for (byte_offset, frame_index) in byte_offset_to_frame_index.iteritems():
                if byte_offset >= byte_range_start and byte_offset <= byte_range_end:
                    resolution_of_frame[frame_index] = max(resolution, resolution_of_frame[frame_index])

        frames_already_parsed = set()
        for line in stall_logfile:
            match_object = re.search("RENDER CALL ON: ([0-9]+(?:\.[0-9]+)?)s TIME: (.+)", line)
            if match_object:
                time_in_video = float(match_object.group(1))
                frame_index_float = time_in_video * 24. # because 24 fps
                frame_index_displayed = int(round(frame_index_float))
                assert(abs(float(frame_index_displayed)-(frame_index_float)) < .01)

                if frame_index_displayed not in frames_already_parsed: # rendering new frame
                    frames_already_parsed.add(frame_index_displayed)
                    system_time_of_render_call = Decimal(match_object.group(2))

                    frame_stat_string = "Time in video {:<10}".format(time_in_video)
                    frame_stat_string += " which is frame {:<6}".format(frame_index_displayed)
                    frame_stat_string += " displayed at system time {:<11}".format(system_time_of_render_call)

                    if not frame_index_displayed in resolution_of_frame:
                        print(str(frame_index_displayed) + " not in resolution map")
                        raise Exception("Got render for frame we shouldn't have had data to show")

                    frame_resolution = resolution_of_frame[frame_index_displayed]
                    frame_stat_string += " with vertical resolution {:<4}".format(frame_resolution)

                    frame_index_to_ssim = video_stats_lookup_maps[frame_resolution][1]
                    if not frame_index_displayed in frame_index_to_ssim:
                        print(str(frame_index_displayed) + " not in ssim map")
                        raise Exception("Got render for frame we shouldn't have had data to show")

                    frame_ssim = frame_index_to_ssim[frame_index_displayed]
                    frame_stat_string += " and ssim score " +str(frame_ssim)
                    print(frame_stat_string, file=output_file)

        print("Finished parsing trial " + trial_id)

def main():
    if len( sys.argv ) is not 4:
        raise ValueError("Usage: python parse-data.py SSIM_index_directory youtube_logs_directory output_directory")
    SSIM_index_directory = sys.argv[1]
    youtube_logs_directory = sys.argv[2]

    video_stats_lookup_maps = dict()
    for filename in get_filenames_list( SSIM_index_directory):
        resolution = re.search("[0-9]+x([0-9]+)", filename).group(1)
        with open(filename) as SSIM_index_file:
            for line in SSIM_index_file:
                match_object = re.search("([0-9]+) ([0-9]+.[0-9]+) [A-Z] [0-9]+ ([0-9]+)", line)
                if match_object:
                    displayed_frame_index = int(match_object.group(1))
                    SSIM_score = float(match_object.group(2))
                    byte_offset = int(match_object.group(3))

                    if resolution not in video_stats_lookup_maps:
                        video_stats_lookup_maps[resolution] = ( defaultdict(int), defaultdict(float) )

                    (byte_offset_to_frame_index, frame_index_to_ssim) = video_stats_lookup_maps[resolution]
                    byte_offset_to_frame_index[byte_offset] = displayed_frame_index
                    frame_index_to_ssim[displayed_frame_index] = SSIM_score

                    #print( displayed_frame_index + " " + SSIM_score  + " " + byte_offset )

    output_directory = sys.argv[3]
    if os.path.exists(output_directory):
        print("Removing existing contents of " + output_directory)
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    trial_id_to_youtube_logs = dict()
    trial_id_to_stall_logs = dict()
    for f in get_filenames_list( youtube_logs_directory ):
        match_object = re.search("stall-log-(.+).txt", f)
        if match_object:
            trial_id = match_object.group(1)
            assert(trial_id not in trial_id_to_stall_logs)
            trial_id_to_stall_logs[trial_id] = f

        else:
            match_object = re.search("log-(.+).txt", f)
            if match_object:
                trial_id = match_object.group(1)
                assert(trial_id not in trial_id_to_youtube_logs)
                trial_id_to_youtube_logs[trial_id] = f


    # check for missing log files
    missing_logs = False
    for trial_id in trial_id_to_stall_logs.keys():
        if trial_id not in trial_id_to_youtube_logs:
            print("Missing youtube log for " + trial_id)
            missing_logs = True
    for trial_id in trial_id_to_youtube_logs.keys():
        if trial_id not in trial_id_to_stall_logs:
            print("Missing stall log for " + trial_id)
            missing_logs = True

    if missing_logs:
        raise Exception("Logs missing")

    args_list = []
    for trial_id, youtube_log in trial_id_to_youtube_logs.iteritems():
            if trial_id not in trial_id_to_stall_logs:
                raise Exception("Missing stall log file for trial " + trial_id)

            # TODO maybe don't delete existing directory here
            os.mkdir(output_directory + "/" + trial_id)

            args_list.append((trial_id, youtube_log, trial_id_to_stall_logs[trial_id], video_stats_lookup_maps, output_directory))

    if len(args_list) is 0:
        print("No log files found in " + youtube_logs_directory )
    else:
        print("Processing " + str(2*len(args_list)) + " log files...")

    # Use process pool to parallelize calling get_inter_frame_delay
    Pool(processes=multiprocessing.cpu_count()).map(parse_logs_for_trial, args_list)

if __name__ == '__main__':
  main()
