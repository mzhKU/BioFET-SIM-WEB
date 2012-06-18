#!/usr/bin/python

print "Content-type: text/plain\n" 

print "Unable to handle request. Please enable JavaScript for your browser."
r1 = "Return 1."
r2 =  "Return 2."

#print "THEIS"

#print json.dumps([r1, r2])
import bio_lib
import time

print "X"*40
w=open(bio_lib.pdb_base_path + 'test.pdb', 'w')
w.write('test' + str(time.time()))
w.close()
