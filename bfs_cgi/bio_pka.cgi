#!/usr/bin/python

print "Content-type: text/plain\n"

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
target = form['target'].value 
pH     = float(form['pH'].value)

from subprocess import Popen, PIPE 

# ***********************************************************************
# Global application scope variables.
import bio_lib
# .......................................................................  

def calc_pKas(target): 
    pkap = Popen([bio_lib.python3_path, bio_lib.propka_path,
                  bio_lib.pdb_base_path + '%s-reo.pdb' % target], stdout=PIPE,
                  stderr=PIPE, shell=False)
    pka_dat = open(bio_lib.pdb_base_path + target + '-reo.pka', 'w')
    pka_dat.write(pkap.stdout.read())
    pka_dat.close()
    pkap.stdout.close() 

if __name__ == "__main__":
    calc_pKas(target)
    print "pHPad=%05.2f" % pH
# .......................................................................  
# -----------------------------------------------------------------------  
