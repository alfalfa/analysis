[ "$1" = "" ] && echo "Usage: $0 [dataset title]" && exit

gnuplot -e "dataset='$1'" inter-frame-delays-ccdf.plt
gnuplot -e "dataset='$1'" inverse-complement-ssim-cdf.plt
gnuplot -e "dataset='$1'" min-ssim-cdf.plt
gnuplot -e "dataset='$1'" plot-dataset.sh
gnuplot -e "dataset='$1'" proportional-playback.plt
gnuplot -e "dataset='$1'" rebuffering-ratios-cdf.plt
gnuplot -e "dataset='$1'" resume-delays-cdf.plt
gnuplot -e "dataset='$1'" ssim-cdf.plt
