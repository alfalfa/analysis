set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-min-ssim-cdf.svg"
unset key
set title "CDF of minimum SSIM scores in a run for ".dataset

set style data linespoints
plot dataset.'/datapoints/'.dataset.'-min-ssim-cdf.dat' using 1:2 with steps title column
