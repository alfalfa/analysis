set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-resume-delays-cdf.svg"
unset key
set title "CDF of seek delays for ".dataset

set xlabel 'Resume duration (seconds)'

set style data linespoints
plot dataset.'/datapoints/'.dataset.'-resume-delays-cdf.dat' using 1:2 with steps title column
