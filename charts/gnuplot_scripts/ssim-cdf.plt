set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-ssim-cdf.svg"
unset key
set title "CDF of frame SSIM scores for ".dataset

set xlabel 'SSIM score'

set style data linespoints
plot dataset.'/datapoints/'.dataset.'-ssim-cdf.dat' using 1:2 with steps title column
