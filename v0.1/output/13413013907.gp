
set term postscript eps enhanced color "Times-Roman" 22
set style line 1 lt 1 lw 6 pt 7 ps 1
set nokey
set border 15 lw 2
set xlabel "Solvent Debye length {/Symbol l}_{/Times-Italic D} (nm)"
set ylabel "{/Symbol D}G/G_0"

set out "/var/www/propka/biofet-sim/v0.1/output/13413013907.eps"

plot "/var/www/propka/biofet-sim/v0.1/output/13413013907.data" u 1:2 w p ls 1
    