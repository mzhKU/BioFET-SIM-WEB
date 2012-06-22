#!/usr/bin/python
import os
print "Content-Type: text/html\n\n"

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
import bio_lib

fileitem = form["thefile"]
if fileitem.filename:
    open(bio_lib.pdb_base_path + form["thefile"].filename, 'wb').write(fileitem.file.read())

for item in form.keys():
  print "<div><b>%s:</b> %s</div>\n" % (item, form[item].value)
print "Upload done."
