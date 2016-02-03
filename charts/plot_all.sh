#/bin/bash
for d in */datapoints
do
    dataset=`echo $d | sed 's/\/datapoints//g'`

    gnuplot -e "dataset='$dataset'" gnuplot_scripts/inter-frame-delays-ccdf.plt &
    gnuplot -e "dataset='$dataset'" gnuplot_scripts/inverse-complement-ssim-cdf.plt &
    gnuplot -e "dataset='$dataset'" gnuplot_scripts/proportional-playback.plt &
    gnuplot -e "dataset='$dataset'" gnuplot_scripts/rebuffering-ratios-cdf.plt &
    gnuplot -e "dataset='$dataset'" gnuplot_scripts/resume-delays-cdf.plt &
    gnuplot -e "dataset='$dataset'" gnuplot_scripts/ssim-cdf.plt &
    gnuplot -e "dataset='$dataset'" gnuplot_scripts/min-ssim-cdf.plt &
    wait
    echo Finished graphs for $dataset
done
