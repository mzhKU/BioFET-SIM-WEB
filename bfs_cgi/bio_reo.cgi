#!/usr/bin/python

print "Content-type: text/html\n"

import cgi 
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
target = form['target'].value

from subprocess import Popen, PIPE
from os.path import splitext
import bio_lib
import os.path
import string
import sys
import os 

# ***********************************************************************
# Global application scope variables.
import bio_lib
# .......................................................................  


# ***********************************************************************
# Evaluate initialization form controls.
# ......................................
overwrite = form.getvalue('overwrite')
uploaded  = form.getvalue('uploaded')
if overwrite == None:
    overwrite = False
else:
    overwrite = True

if uploaded == None:
    uploaded = False
else:
    uploaded = True 
# ......................................
# -----------------------------------------------------------------------

# ***********************************************************************
# Reorient function.
# ......................................
def translate_com(target):
    """Calling VMD and returning the output directly."""
    #+ 'lappend /var/www/vmd/lib_vmd/scripts/la1.0\n'\
    #+ 'lappend /var/www/vmd/lib_vmd/scripts/orient\n'
    vmd_src = 'mol load pdb %s-fix.pdb\n' % (bio_lib.pdb_base_path + target)\
            + 'set HOME ' + bio_lib.vmd_base_path + '\n'\
            + 'molinfo 0 get center\n'\
            + 'env\n'
            #+ 'auto_path /opt/vmd_package/Contents/vmd/la1.0\n'\
            #+ 'auto_path /opt/vmd_package/Contents/vmd/orient\n'\
            #+ 'puts $HOME\n'
    comp = Popen([bio_lib.vmd_cmd_path, '-dispdev', 'text', '-eofexit'],
                  stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False) 
    comp.stdin.write(vmd_src)
    vmd_com_result = comp.communicate()[0]

    #self.reo     = bio_lib.pdb_base_path + self.target + '-reo.pdb'
    #self.vmd_cmd = bio_lib.vmd_cmd_path
    """The coordinates can be identified by opening curly brace.
    When match, cast into list of floats, discard leading and
    ending braces.  To subtract, flip the coordinates signs.
    Reorientation using Orient and la.1.0 plugins in VMD."""
    # <<PATH>>
    for line in vmd_com_result.split('\n'):
        if len(line) > 0 and line[0] == '{':
            com_xyz = [float(i) for i in line[1:-1].split()]
    com_xyz = [i*(-1) for i in com_xyz] 
    # Calling the VMD reorientation script.
    reo_src = bio_lib.get_reo_src(com_xyz, target)
    vmdp = Popen([bio_lib.vmd_cmd_path, '-dispdev', 'text', '-eofexit'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
    vmdp.stdin.write(reo_src)
    print vmdp.communicate()[0]
# --------------------------------------------------------------------------


# **************************************************************************
# DIRECT LAUNCH
# ..........................................................................
if __name__ == '__main__':
    bio_lib.availability_closure('-reo.pdb')(target, uploaded, overwrite, translate_com)
# --------------------------------------------------------------------------
