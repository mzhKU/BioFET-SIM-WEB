#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

print "Content-type: text/plain\n"

# DESCRIPTION:
# - Wrapper for bio_com.cgi
# - Called from AJAX.

import cgi
import cgitb
cgitb.enable() 
from bio_rho import Rho
import bio_com
import bio_lib
import copy

# ************************************************************************
# READ FORM DATA AND EXTERNAL CALCULATION SETUP
# ........................................................................
# Obtaining properties from the HTML form.
form    = cgi.FieldStorage()
target  = form['targetLab'].value 
tmp_pdb = form['tmp_pdb'].value
tmp_pqr = form['tmp_pqr'].value
tmp_pdb = bio_lib.reformat_coordinates(tmp_pdb, tmp_pqr)
print tmp_pdb
# Should BioFET-SIM single or multiple charge model be used.
charge_model      = form['model'].value
# Handling the "Number of Proteins on NW" checkbox.
if form.getvalue('num_prot_box'):
    # Use default value if checked.
    calc_num_prot = "no"
else:
    calc_num_prot = "yes"
# PARAMETERS
# NW properties
params = {}
params['nw_len' ]  = float(form['nw_len' ].value)
params['nw_rad' ]  = float(form['nw_rad' ].value)
params['L_tf'   ]  = float(form['L_tf'   ].value)
params['eps_1'  ]  = float(form['eps_1'  ].value)
params['mu'     ]  = float(form['mu'     ].value)
params['n_0'    ]  = float(form['n_0'    ].value)
params['nw_type']  =       form['nw_type'].value
# Oxide and biofunctionalization layer properties
params['lay_ox' ]  = float(form['lay_ox' ].value)
params['eps_2'  ]  = float(form['eps_2'  ].value)
params['lay_bf' ]  = float(form['lay_bf' ].value)
# Solvent properties
params['L_d'    ]  = float(form['L_d'    ].value)
params['eps_3'  ]  = float(form['eps_3'  ].value)
# Variables
nw_len             = float(form['nw_len' ].value)
nw_rad             = float(form['nw_rad' ].value)
lay_ox             = float(form['lay_ox' ].value)
lay_bf             = float(form['lay_bf' ].value) 
L_d                = float(form['L_d'    ].value)
L_tf               = float(form['L_tf'   ].value)
eps_1              = float(form['eps_1'  ].value)
eps_2              = float(form['eps_2'  ].value)
eps_3              = float(form['eps_3'  ].value) 
mu                 = float(form['mu'     ].value)
n_0                = float(form['n_0'    ].value)
nw_type            =       form['nw_type'].value 
comment            = form['comment'].value
bfs_file_name      = form['fileName'].value
#timestamp          = form['timestamp'].value
# ........................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# BioFET-SIM Start
# ........................................................................
"""
# Starting BioFET-SIM calculation.
from bio_mod import SimMulti
from bio_mod import SimSingl

# Initializing the simulation. The simulation calls the charge
# distribution when the model starts the calculation.
sim = SimMulti(target, av_RQ, pqr, params)
sim.set_rho() 
# Configuring protein population on NW.
if not form.getvalue('num_prot_box'):
    # Compute number of proteins based on orientation.
    # <<EDIT>>
    # 29.05.2012: sim.av_RQ -> sim.pqr
    #num_prot = bio_lib.get_num_prot(sim.av_RQ, sim.param['nw_len'], sim.param['nw_rad']) 
    num_prot = bio_lib.get_num_prot(sim.rho, sim.param['nw_len'], sim.param['nw_rad']) 
else:
    # Use constant number of proteins.
    num_prot = int(form['num_prot_inp'].value) 
# Results data container and setting label, base value and percentage range of results graph.
dG_G0 = round(bio_com.compute(sim.rho, nw_len, nw_rad, lay_ox, L_d, L_tf, lay_bf,
                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
G0    = round(bio_lib.G0(nw_len, nw_rad, n_0, mu))
print dG_G0
"""
# ........................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# Initialize charge distribution for pH range.
# ........................................................................
if __name__ == '__main__': 
    for pHi in range(1, 15): 
        response  = ''
        response += "%i: " % pHi
        rho = Rho(target) 
        rho.load_pdb()
        rho.unique_residue_ids()
        rho.cluster_residues()
        rho.set_terminals()
        rho.set_RQ()
        rho.set_av_RQ()
        rho.set_pqr(target, rho.av_RQ, pHi, open(bio_lib.pdb_base_path + target + '-reo.pka', 'r'))
        # ------------------------------ 
        bio_lib.write_pqr(target, pHi, rho.pqr)
        # ------------------------------ 
        response += "pqr=%s;\n" % rho.pqr
        #print response
# ........................................................................
# ------------------------------------------------------------------------ 
