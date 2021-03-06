set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-inter-frame-delays-ccdf.svg"
unset key
set title "CCDF of all inter-frame delays for ".dataset

set xlabel 'CCDF of all inter-frame delays'
set logscale y

set style data linespoints
plot dataset.'/datapoints/'.dataset.'-inter-frame-delays-ccdf.dat' using 1:2 with steps title column
