set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-ssim-cdf.svg"
unset key
set title "CDF of frame SSIM scores for ".dataset

set xlabel 'SSIM score'

plot dataset.'/datapoints/'.dataset.'-ssim-cdf.dat' using 1:2 lt 1 lc 3 title column
