set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output dataset."/".dataset."-proportional-playback.svg"
unset key
set title "Proportion playback time with less than x inter-frame delay for ".dataset

set xlabel 'Inter-frame delay (seconds)'
set logscale y

plot dataset.'/datapoints/'.dataset.'-proportional-playback.dat' using 1:2 title column
