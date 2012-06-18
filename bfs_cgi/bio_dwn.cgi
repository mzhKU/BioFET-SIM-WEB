#!/usr/bin/python

print "Content-type: text/html\n" 

# ***********************************************************************
# Download PDB file.
# Calling sequence:
# $ python bfs_cgi/bio_dwn.py <target>
import urllib
import os.path
import os
import sys
# .......................................................................  

# ***********************************************************************
# Collect data from AJAX call.
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
# .......................................................................

# ***********************************************************************
# Enable global application scope path variables.
import bio_lib
# .......................................................................

# ***********************************************************************
# Main application.
def download_pdb(target):
    #print 'bio_lib.pdb_base_path:', bio_lib.pdb_base_path + target + '.pdb'
    #print 'os.getcwd():', os.getcwd()
    if not os.path.exists(bio_lib.pdb_base_path + target + '.pdb'):
        address='http://www.pdb.org/pdb/files/%s.pdb1' % target
        dat = urllib.urlopen(address)
        val = open(bio_lib.pdb_base_path + target + '.pdb', 'w')
        for i in dat.readlines():
            val.write(i) 
        dat.close()
        val.close()
        print "Structure downloaded."
    else:
        print "Structure available, ending."
# .......................................................................
# -----------------------------------------------------------------------

# ***********************************************************************
if __name__ == "__main__":
    # Calling from Apache.
    target = form['target'].value
    download_pdb(target)
# .......................................................................  
