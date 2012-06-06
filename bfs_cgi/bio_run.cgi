#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

print "Content-type: text/plain\n"

# DESCRIPTION:
# - Wrapper for bio_com.cgi
# - Called from AJAX.

import cgi
import cgitb
cgitb.enable() 
import bio_com

# ************************************************************************
# EXTERNAL CALCULATION SETUP
# ........................................................................
# Obtaining properties from the HTML form.
form              = cgi.FieldStorage()
target            = form['targetLab'].value 
# Stored in input type hidden
pqr               = form['pqr'].value
av_RQ             = copy.deepcopy(pqr)
abs_axis          = form['abs'].value 
# Should BioFET-SIM single or multiple charge model be used.
charge_model      = form['model'].value
# Handling the "Number of Proteins on NW" checkbox.
if form.getvalue('num_prot_box'):
    # Use default value if checked.
    calc_num_prot = "no"
else:
    calc_num_prot = "yes"

# ************************************************************************
# READ FORM DATA
# ........................................................................
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
timestamp          = form['timestamp'].value
# ........................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# BioFET-SIM Start
# ........................................................................
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
dG_G0 = round(compute(sim.rho, nw_len, nw_rad, lay_ox, L_d, L_tf, lay_bf,
                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
G0    = round(bio_lib.G0(nw_len, nw_rad, n_0, mu))
print dG_G0
