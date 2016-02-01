set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output "../".dataset."-ssim-cdf.svg"
set title "CDF of frame SSIM scores"# + dataset

set xlabel 'SSIM score'

plot '../data/'.dataset.'-ssim-cdf.dat' using 1 title column
