import os
import sys
import re
import numpy as np
import directory_traversal_helper
import plotting_helper
 

def main():
    if len( sys.argv ) is not 2:
        raise ValueError("Usage: python plot-inter-frame-delay.py frame_stats_directory")
    frame_stats_directory = sys.argv[1]
    _, dataset_title  = os.path.split(os.path.abspath(frame_stats_directory))

    inter_frame_delays_list = []
    resume_delays_list = []
    rebuffering_ratios = []
    num_files_parsed = 0
    for f, _ in directory_traversal_helper.get_files_matching_regex(frame_stats_directory, "frame-stats.dat"):
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

    total_playback_time = sum( inter_frame_delays_list )
    xvals = np.sort( inter_frame_delays_list )
    yvals = []
    subtotal_playback_time = total_playback_time
    for ifd in xvals:
        subtotal_playback_time -= ifd
        yvals.append( subtotal_playback_time / total_playback_time)

    filename = dataset_title + "-proportional-playback.dat"
    plotting_helper.write_points_to_file(xvals, yvals, filename)

    (xvals, yvals) = plotting_helper.get_cdf( inter_frame_delays_list )
    yvals = 1-yvals # CCDF
    filename = dataset_title + "-inter-frame-delays-ccdf.dat"
    plotting_helper.write_points_to_file(xvals, yvals, filename)

    (xvals, yvals) = plotting_helper.get_cdf( resume_delays_list )
    filename = dataset_title + "-resume-delays-cdf.dat"
    plotting_helper.write_points_to_file(xvals, yvals, filename)

    (xvals, yvals) = plotting_helper.get_cdf( rebuffering_ratios )
    filename = dataset_title + "-rebuffering-ratios-cdf.dat"
    plotting_helper.write_points_to_file(xvals, yvals, filename)

if __name__ == '__main__':
  main()
