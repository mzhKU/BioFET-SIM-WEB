#!/usr/bin/python 

# ************************************************************************
# BioFET-SIM Test Suite.
# ........................................................................  

from scipy.special import i0, i1, k0, k1, log, sqrt, exp, pi, power
from string import Template
import numpy
import subprocess
import os

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# ---------- Do not edit this module without appropriate care. -----------
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# ************************************************************************
# CONTENT:
# - Tests
# ------------------------------------------------------------------------ 
# ************************************************************************
# TESTS.
# ........................................................................  
def get_num_prot(av_RQ, nw_len, nw_rad):
    """Compute the bounding box dimension parallel to the NW
    surface, i.e. the area of the x-, y-plane.
    'av_RQ' is formatted as PQR data, but provides only a
    default charge of '1.0'.
    """ 
    X = []
    Y = []
    Z = []
    for atm in av_RQ:
        if len(atm.split()) > 0:
            if atm.split()[0] == 'ATOM':
                x = atm[30:38].strip()
                y = atm[38:46].strip()
                z = atm[46:54].strip()
                X.append(float(x)*0.1)
                Y.append(float(y)*0.1)
                Z.append(float(z)*0.1) 
    # Scan all residues.
    x_min = min(X)
    x_max = max(X)
    y_min = min(Y)
    y_max = max(Y)
    z_min = min(Z)
    z_max = max(Z) 
    prot_xy = (x_max - x_min)*(y_max - y_min)
    nw_surface = 2*pi*nw_rad*nw_len
    n_bio_molecules = nw_surface/prot_xy 
    print "<pre>"
    for i in av_RQ:
        print i
    print 'x-, y-surface area: (x_max - x_min)*(y_max - y_min), nm^2:'
    print prot_xy, "\n"
    print 'nw_surface:'
    print nw_surface, "= 2*pi*%4.2f*%4.2f\n" % (nw_len, nw_rad)
    print "x_min, x_max, y_min, y_max, z_min, z_max"
    print x_min, x_max, y_min, y_max, z_min, z_max, "\n"
    print "Number of biomolecules: nw_surface/prot_xy"
    print n_bio_molecules
    print "</pre>" 

def test_fixPDB(pqrp):
    print "<pre>"
    print '\n'.join(pqrp.communicate())
    print "</pre>"

def calcG_0(nw_rad, nw_len, n_0, mu):
    return (pi*(nw_rad*1E-9)**2*q_elem*n_0*mu/(nw_len*1E-9))

def print_rho(mod):
    # 'of' is a filename.
    print 'Charge distribution of:', mod.system
    print 'x[nm]'.rjust(4+2+3+10) +\
          'y[nm]'.rjust(10) +\
          'z[nm]'.rjust(10) +\
          '[Unitary Charges]'.rjust(20) 
    for qi in range(0, mod.m):
        print 'q[' + str(qi).rjust(4) + ']'.rjust(2) +\
                     str(mod.rho[qi][0]).rjust(10) +\
                     str(mod.rho[qi][1]).rjust(10) +\
                     str(mod.rho[qi][2]).rjust(10) +\
                     str(mod.rho[qi][3]).rjust(20)

def test_res_ids(rho):
    print "<pre>"
    print "*"*40
    print 'TEST: rho.res_ids()'
    #print 'CALL: if rho.res_cnt == len(rho.res_ids)-1:'
    #print '          print \'rho.res_cnt:      \', rho.res_cnt'
    #print '          print \'len(rho.res_ids): \', len(rho.res_ids)'
    #print '          print \'rho.res_ids:      \', rho.res_ids'
    #print '          print \'len(rho.starts):  \', len(rho.starts)'
    #print '          print \'rho.starts:       \', rho.starts' 
    #print 'NOTE: \'len(rho.res_ids)-1\' is because finally the residue\n'\
    #      '      counter is 1 lower than the number of items in the list.' 
    print "."*40
    if rho.res_cnt == len(rho.res_ids)-1:
        print 'rho.res_cnt:         ', rho.res_cnt
        print 'len(rho.res_ids)-1:  ', len(rho.res_ids)-1
        print 'len(rho.res_ids):    ', len(rho.res_ids)
        print 'rho.res_ids:         '
        for i in rho.res_ids:
            print i
        print 'len(rho.identifiers):', len(rho.identifiers)
        print 'rho.identifiers:     ', rho.identifiers
        print 'len(rho.identifiers):', len(rho.identifiers)
    print "-"*40
    print "</pre>"
    print

def test_load_pdb(rho):
    print "<pre>"
    print "*"*40
    print 'TEST: rho.load_pdb()'
    print 'CALL: print \'\'.join(rho.coords)'
    print '      print \'len(rho.coords)\', len(rho.coords)'
    print "."*40
    print '\n'.join(rho.coords)
    print 'len(rho.coords)', len(rho.coords)
    print "-"*40
    print "</pre>"
    print

def test_cluster_residues(rho): 
    print "<pre>"
    print "*"*40
    print 'TEST: rho.cluster_residues()'
    print 'CALL: [...]'
    print 'NOTE: Subtraction of "3" since the first three elements'
    print '      of the "res_id" element are the name, index and chain.'
    print "."*40
    identifiers  = rho.identifiers
    res_ids = rho.res_ids
    coords  = rho.coords
    atm_cnt = 0
    res_cnt = 0 
    for res_id in res_ids:
        print 'res_id[0]: %s,' % res_id[0],\
              'len(res_id)-3: %i' % (len(res_id)-3) 
    print 
    res_cnt = 0
    for res_id in res_ids:
        print 'res_ids[%i]: ' % res_cnt
        print res_id
        res_cnt += 1
    print "-"*40
    print "</pre>"
    print

def test_set_RQ(rho):
    print "<pre>"
    print "*"*40
    print 'TEST: rho.set_RQ()'
    print 'CALL: print \'rho.RQ\''
    print "."*40
    for rq_i in rho.RQ:
        print rq_i
    print "-"*40
    print "</pre>"
    print

def test_set_av_RQ(rho):
    print "<pre>"
    print "*"*40
    print 'TEST: rho.set_av_RQ()'
    print 'CALL: print \'rho.av_RQ\''
    print "."*40
    for av_rq_i in rho.av_RQ:
        print av_rq_i
    print "-"*40
    print "</pre>"
    print

def test_set_pqr(rho):
    print "<pre>"
    print "*"*40
    print 'TEST: rho.set_pqr()'
    print 'CALL: print \'rho.pqr\''
    print "."*40
    print rho.pqr 
    print "-"*40
    print "</pre>"
    print

def test_set_terminals(rho):
    print "<pre>"
    print "*"*40
    print 'TEST: rho.set_terminals()'
    print 'CALL: print \'rho.terminals\''
    print "."*40
    print rho.c_terminals
    print rho.n_terminals
    print "-"*40
    print "</pre>"
    print

def test_all(rho):
    rho.test_parsing()
    rho.test_res_ids() 
    rho.test_cluster_residues()
# ........................................................................
# ------------------------------------------------------------------------ 
