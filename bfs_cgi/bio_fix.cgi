#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

print "Content-type: text/plain\n"

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

def fix_pdb(target):
    """Discard non-'ATOM' and non-'^TER' lines, else PDB2PQR does
    not include multiple chains."""
    if not os.path.exists(bio_lib.pdb_base_path + target + '-fix.pdb'):
        # <<PATH>
        awk_cmd = ['awk', '/(ATOM|^TER)/,//']
        #awkp = Popen(awk_cmd, stdin=open('./' + target + '.pdb', 'r'),
        awkp = Popen(awk_cmd, stdin=open(bio_lib.pdb_base_path + target + '-rec.pdb', 'r'),
                     stdout=PIPE, stderr=PIPE, shell=False)
        nat = open(bio_lib.pdb_base_path + target + '-nat.pdb', 'w')
        nat.write(awkp.stdout.read())
        nat.close()
        # <<PATH>>
        #pqr_cmd = ['python', '/Users/mzh/software/pdb2pqr/pdb2pqr.py',
        #           '-v', '--chain', '--ff=CHARMM',
        #           target + '-nat.pdb', target + '-fix.pdb']
        # Deployment: copy ~/software/pdb2pqr to /opt/
        #pqr_cmd = ['python', bio_lib.pdb2pqr_base_path,
        pqr_cmd = [bio_lib.external_python_base_path, bio_lib.pdb2pqr_base_path,
                   '-v', '--chain', '--ff=CHARMM',
                   bio_lib.pdb_base_path + target + '-nat.pdb',
                   bio_lib.pdb_base_path + target + '-fix.pdb']
        #pqrp = Popen(pqr_cmd, stdout=PIPE, stdin=PIPE,
        #             stderr=open('pdb2pqr_err.dat', 'w'), shell=False)
        pqrp = Popen(pqr_cmd, stdout=PIPE, stdin=PIPE, shell=False)
        #bio_tst.test_fixPDB(pqrp)
        pqrp.communicate()
    print "Fixing done."

if __name__ == "__main__":
    fix_pdb(target)
