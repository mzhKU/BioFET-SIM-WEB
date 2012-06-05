#set terminal postscript eps enhanced color "Times-Roman" 22
set terminal svg
set output "result_default.svg"
set style line 1 lt 1 lw 6 pt 7 ps 1
unset title
set nokey
set grid
set xlabel "x"
set ylabel "Sensitivity"
plot [][0:1] 2
