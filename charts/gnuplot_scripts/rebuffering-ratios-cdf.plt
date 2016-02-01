set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output "../".dataset."-rebuffering-ratios-cdf.svg"
set title "CDF rebuffering ratios"# + dataset

set xlabel 'Rebuffering ratio'

plot '../data/'.dataset.'-rebuffering-ratios-cdf.dat' using 1 title column
