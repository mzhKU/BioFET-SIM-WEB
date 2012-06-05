#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

print "Content-type: text/plain\n"

# DESCRIPTION:
# - Wrapper for bio_sim.cgi program.
# - Called from AJAX.

import cgi
import cgitb
cgitb.enable()

import bio_sim
