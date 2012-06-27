#!/usr/bin/python

print "Content-type: text/plain\n"

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
# Reorient structure.
# ......................................
class Reo:
    """Helper class.
    Carries out reorientation of molecular structure.
    """ 
    def __init__(self, target):
        # For PROPKA: self.vmd = '/var/www/vmd/bin_vmd/vmd' 
        # Define a 'VMD' environment to avoid path.
        self.target  = target
        self.reo     = bio_lib.pdb_base_path + self.target + '-reo.pdb'
        self.vmd_cmd = bio_lib.vmd_cmd_path

    def get_com(self): 
        """Calling VMD and returning the output directly."""
        #+ 'lappend /var/www/vmd/lib_vmd/scripts/la1.0\n'\
        #+ 'lappend /var/www/vmd/lib_vmd/scripts/orient\n'
        vmd_src = 'mol load pdb %s-fix.pdb\n' % (bio_lib.pdb_base_path + self.target)\
                + 'set HOME ' + bio_lib.vmd_base_path + '\n'\
                + 'molinfo 0 get center\n'\
                + 'env\n'
                #+ 'auto_path /opt/vmd_package/Contents/vmd/la1.0\n'\
                #+ 'auto_path /opt/vmd_package/Contents/vmd/orient\n'\
                #+ 'puts $HOME\n'
        comp = Popen([self.vmd_cmd, '-dispdev', 'text', '-eofexit'],
                      stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False) 
        comp.stdin.write(vmd_src)
        return comp.communicate()[0]

    def translate_com(self, target):
        """The coordinates can be identified by opening curly brace.
        When match, cast into list of floats, discard leading and
        ending braces.  To subtract, flip the coordinates signs.
        Reorientation using Orient and la.1.0 plugins in VMD."""
        # <<PATH>>
        if not os.path.exists(bio_lib.pdb_base_path + target + '-reo.pdb'):
            for line in self.get_com().split('\n'):
                print line
                if len(line) > 0 and line[0] == '{':
                    self.com_xyz = [float(i) for i in line[1:-1].split()]
            self.com_xyz = [i*(-1) for i in self.com_xyz] 
            # Calling the VMD reorientation script.
            reo_src = bio_lib.get_reo_src(self.com_xyz, self.target)
            vmdp = Popen([self.vmd_cmd, '-dispdev', 'text', '-eofexit'],
                          stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=False)
            vmdp.stdin.write(reo_src)
            print vmdp.communicate()[0]
# ..........................................................................
# --------------------------------------------------------------------------

# **************************************************************************
# Form control logic.
# ..........................................................................
def check_availability_and_fix(target):
    # Use upload.
    if uploaded:
        # Force overwrite.
        if overwrite:
            reo = Reo(target)
            reo.translate_com(target)
            reo_out = reo.translate_com(target)
        # Does not exist.
        if not os.path.exists(bio_lib.pdb_base_path + target + '-reo.pdb'):
            reo = Reo(target)
            reo.translate_com(target)
            reo_out = reo.translate_com(target)
    # Download.
    else:
        # Use existing.
        if os.path.exists(bio_lib.pdb_base_path + target + '-reo.pdb'):
            print "Structure available." 
        # Fixed structure not available.
        else:
            reo = Reo(target)
            reo.translate_com(target)
            reo_out = reo.translate_com(target)
# ..........................................................................
# --------------------------------------------------------------------------


# **************************************************************************
# DIRECT LAUNCH
# ..........................................................................
if __name__ == '__main__':
    bio_lib.availability_closure('-reo.pdb')(target, uploaded, overwrite, 
# --------------------------------------------------------------------------
