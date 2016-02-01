set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output "../".dataset."-inter-frame-delays-ccdf.svg"
set title "CCDF of all inter-frame delays"# + dataset

set xlabel 'CCDF of all inter-frame delays'

plot '../data/'.dataset.'-inter-frame-delays-ccdf.dat' using 1 title column
