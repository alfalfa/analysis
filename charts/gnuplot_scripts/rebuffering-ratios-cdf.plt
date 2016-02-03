set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-rebuffering-ratios-cdf.svg"
set title "CDF rebuffering ratios"# + dataset

set xlabel 'Rebuffering ratio'

plot dataset.'/datapoints/'.dataset.'-rebuffering-ratios-cdf.dat' using 1:2 title column
