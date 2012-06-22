#!/usr/bin/python

# ************************************************************************
# Prepare BioFET-SIM input file.
# ........................................................................

print "Content-type: text/html\n" 
import cgi
import cgitb
cgitb.enable() 
import sys
import os.path
import bio_lib
import numpy 
import copy 
import time
# ........................................................................
# ------------------------------------------------------------------------ 

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
#Q_tot             = form['Q_tot'].value
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
#timestamp          = form['timestamp'].value
# ........................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# BioFET-SIM Start
# ........................................................................
# Starting BioFET-SIM calculation.
from bio_com import compute
from bio_mod import SimMulti
from bio_mod import SimSingl

# ************************
# Multiple charge simulation.
# ........................
if charge_model == 'multi':
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
    results=[] 
    x_lbl = form['abs'].value
    x_val = float(params[x_lbl])
    x_min = float(form[x_lbl+'_x_min'].value)
    x_max = float(form[x_lbl+'_x_max'].value)

    # Prepare BFS command line version input file.
    bio_lib.generate_bfs_input(target, params, sim.rho, num_prot,
                                      comment, len(sim.rho), bfs_file_name)

# ************************
# Single charge simulation.
# ........................
if charge_model == 'singl':
    # Most likely not required.  
    sim = SimSingl(target, av_RQ, pqr, params, Q_tot)
    sim.set_rho() 

    # Configuring protein population on NW.
    if not form.getvalue('num_prot_box'):
        # Compute number of proteins based on orientation.
        num_prot = bio_lib.get_num_prot(sim.av_RQ, sim.param['nw_len'], sim.param['nw_rad']) 
    else:
        # Use constant number of proteins.
        num_prot = int(form['num_prot_inp'].value) 

    # Results data container and setting label, base value and percentage range of results graph.
    results=[]
    x_lbl = form['abs'].value
    x_val = float(params[x_lbl])
    x_min = float(form[x_lbl+'_x_min'].value)
    x_max = float(form[x_lbl+'_x_max'].value) 

    # Prepare offline BFS input (target, parameters, coordinates, x_lbl)
    #bio_lib.generate_bfs_input(target, params, sim.rho, x_lbl, num_prot, x_min, x_max,
    #                           comment, file_name)
    # <BFS_CMD_INP>
    #bio_lib.generate_bfs_input(target, params, sim.rho, x_lbl, num_prot, x_min, x_max,
    #                           comment, len(sim.rho), file_name)
    #bio_lib.generate_bfs_input(target, params, sim.rho, x_lbl, num_prot,
    #                           comment, len(sim.rho), file_name)
    bio_lib.generate_bfs_input(target, params, sim.rho, num_prot, comment, len(sim.rho), bfs_file_name)
# ........................................................................
# ------------------------------------------------------------------------
