#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

print "Content-type: text/plain\n"

import cgi
import cgitb
#cgitb.enable()
form = cgi.FieldStorage()
target = form['target'].value 

from subprocess import Popen, PIPE 

# ***********************************************************************
# Global application scope variables.
import bio_lib
# .......................................................................  

def calc_pKas(target): 
    pkap = Popen([bio_lib.python3_path,
                  bio_lib.propka_path,
                  bio_lib.pdb_base_path + '%s-reo.pdb' % target], stdout=PIPE,
                  stderr=PIPE, shell=False)
    #return pkap.stdout.read()
    pka_dat = open(bio_lib.pdb_base_path + target + '-reo.pka', 'w')
    pka_dat.write(pkap.stdout.read())
    pka_dat.close()
    pkap.stdout.close() 

def get_pKas(pka_dat):
    """The PROPKA output is provided as a stdout file handle.
    This avoids writing a pka file."""
    pka_val = pka_dat.readlines()
    # Locate 'SUMMARY' of pKa values in PROPKA output.
    pka_start_line = 0
    for line in enumerate(pka_val):
        if len(line[1].split()) != 0 and line[1].split()[0] == 'SUMMARY':
            pka_start_line = line[0] + 2 
    # Populate pKa list of with residues and terminals.
    pka_tmp = []
    for pka_line in pka_val[pka_start_line:]:
        # Defining residue or terminal identifier 'id'.
        # The 'summary' lines are 5 elements long.
        if len(pka_line.split()) == 5:
            pka_tmp.append(pka_line.split())
    return pka_tmp

if __name__ == "__main__":
    calc_pKas(target)
