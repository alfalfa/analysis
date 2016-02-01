set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output "../".dataset."-inverse-complement-ssim-cdf.svg"
set title "CDF of 1 / ( 1 - SSIM ) values"# + dataset

set xlabel '1/(1 - SSIM score)'

plot '../data/'.dataset.'-inverse-complement-ssim-cdf.dat' using 1 title column
