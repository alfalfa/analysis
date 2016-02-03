set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-rebuffering-ratios-cdf.svg"
unset key
set title "CDF rebuffering ratios for ".dataset

set xlabel 'Rebuffering ratio'

set style data linespoints
plot dataset.'/datapoints/'.dataset.'-rebuffering-ratios-cdf.dat' using 1:2 with steps title column
