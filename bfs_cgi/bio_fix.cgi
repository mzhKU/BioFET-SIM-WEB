#!/usr/bin/python

print "Content-type: text/html\n"

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
target = form['target'].value

import os.path
from subprocess import Popen, PIPE
import string

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
# Fix side chains.
# ......................................
def fix_pdb(target):
    """Discard non-'ATOM' and non-'^TER' lines, else PDB2PQR does not include multiple chains."""
    awk_cmd = ['awk', '/(ATOM|^TER)/,//']
    awkp = Popen(awk_cmd, stdin=open(bio_lib.pdb_base_path + target + '-rec.pdb', 'r'),
                 stdout=PIPE, stderr=PIPE, shell=False)
    nat = open(bio_lib.pdb_base_path + target + '-nat.pdb', 'w')
    nat.write(awkp.stdout.read())
    nat.close()
    pqr_cmd = [bio_lib.external_python_base_path, bio_lib.pdb2pqr_base_path,
               '-v', '--chain', '--ff=CHARMM',
               bio_lib.pdb_base_path + target + '-nat.pdb',
               bio_lib.pdb_base_path + target + '-fix.pdb']
    pqrp = Popen(pqr_cmd, stdout=PIPE, stdin=PIPE, shell=False)
    pqrp.communicate()
    print "Fixing done."
# ......................................
# -----------------------------------------------------------------------

if __name__ == "__main__":
    bio_lib.availability_closure('-fix.pdb')(target, uploaded, overwrite, fix_pdb)
