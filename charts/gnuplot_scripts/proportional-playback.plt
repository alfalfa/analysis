set terminal svg size 600,400 fixed fname 'arial' fsize 12 
set output "../".dataset."-proportional-playback.svg"
set title "Proportion of total playback time with inter-frame delays less than.."# + dataset

set xlabel 'Inter-frame delay (seconds)'

plot '../data/'.dataset.'-proportional-playback.dat' using 1 title column