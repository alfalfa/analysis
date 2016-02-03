set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-inverse-complement-ssim-cdf.svg"
unset key
set title "CDF of 1 / ( 1 - SSIM ) values for ".dataset

set xlabel '1/(1 - SSIM score)'
set xrange [0:100]

plot dataset.'/datapoints/'.dataset.'-inverse-complement-ssim-cdf.dat' using 1:2 title column
