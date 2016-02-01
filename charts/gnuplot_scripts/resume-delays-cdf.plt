set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output "../".dataset."-resume-delays-cdf.svg"
set title "CDF of seek delays"# + dataset

set xlabel 'Resume duration (seconds)'

plot '../data/'.dataset.'-resume-delays-cdf.dat' using 1 title column
