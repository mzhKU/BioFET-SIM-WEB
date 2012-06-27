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
# -----------------------------------------------------------------------


# ***********************************************************************
# Collect data from AJAX call.
# .......................................................................  
import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
# .......................................................................  
# -----------------------------------------------------------------------


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
# Enable global application scope path variables.
# .......................................................................
import bio_lib
# .......................................................................
# -----------------------------------------------------------------------


# ***********************************************************************
# Main application.
# .......................................................................
def download_pdb(target):
    # Use upload.
    if uploaded:
        # Force overwrite.
        if overwrite:
            print "Using uploaded structure and overwriting previous version."
        # No overwrite.
        else:
            print "Using uploaded structure without overwriting."
    # Download.
    else:
        # Use existing.
        if os.path.exists(bio_lib.pdb_base_path + target + '.pdb'):
            print "Structure available."
        # Download.
        else:
            address='http://www.pdb.org/pdb/files/%s.pdb1' % target
            dat = urllib.urlopen(address)
            val = open(bio_lib.pdb_base_path + target + '.pdb', 'w')
            for i in dat.readlines():
                val.write(i) 
            dat.close()
            val.close()
            print "Structure downloaded."
# .......................................................................
# -----------------------------------------------------------------------


# ***********************************************************************
# .......................................................................
if __name__ == "__main__":
    #if not os.path.exists(bio_lib.pdb_base_path + target + '.pdb'):
    # Calling from Apache.
    target = form['target'].value
    download_pdb(target)
# .......................................................................  
# -----------------------------------------------------------------------
