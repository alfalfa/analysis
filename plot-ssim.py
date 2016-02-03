import os
import sys
import re
import directory_traversal_helper
import plotting_helper

def get_inverse_complement( vals ):
    ret = []
    for val in vals:
        assert(1.- val >= 0)
        if (1.- val) == 0:
            ret.append(100000000)
        else:
            ret.append(1. / (1. - val ) )
    return ret

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


    filename = dataset_title + "-ssim-cdf.dat"
    (xvals, yvals) = plotting_helper.downsample_cumulative_y(plotting_helper.get_cdf(all_ssim_scores))
    plotting_helper.write_points_to_file(xvals, yvals, dataset_title, filename)

    (xvals, yvals) = plotting_helper.downsample_cumulative_y(plotting_helper.get_cdf(get_inverse_complement(all_ssim_scores)))
    filename = dataset_title + "-inverse-complement-ssim-cdf.dat"
    plotting_helper.write_points_to_file(xvals, yvals, dataset_title, filename)

    (xvals, yvals) = plotting_helper.get_cdf( per_trial_min_ssim_scores )
    filename = dataset_title + "-min-ssim-cdf.dat"
    plotting_helper.write_points_to_file(xvals, yvals, dataset_title, filename)


if __name__ == '__main__':
  main()
