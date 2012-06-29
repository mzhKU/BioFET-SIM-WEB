#!/usr/bin/python

print "Content-type: text/plain\n"

# ************************************************************************
# Required.
# ........................................................................
import cgi, cgitb; cgitb.enable() 
from numpy import arange
from bio_mod import SimMulti
from bio_rho import Rho
import bio_lib
import bio_com 
import sys
# ........................................................................
# ------------------------------------------------------------------------ 


# ************************************************************************
# READ FORM DATA AND EXTERNAL CALCULATION SETUP
# - Charge model
# - Number of proteins
# ........................................................................
form              = cgi.FieldStorage()
target            = form['targetLab'].value 
tmp_pdb           = form['tmp_pdb'].value
pdb_new           = bio_lib.rewrite_pdb(target, tmp_pdb)
abs_axis          = form['abs'].value
charge_model      = form['model'].value
button_clicked    = form['action'].value 
pH                = float(form['pH'].value)
if form.getvalue('num_prot_box'):
    calc_num_prot = "no"
else:
    calc_num_prot = "yes"
params            = {}
params['nw_len' ] = float(form['nw_len' ].value)
params['nw_rad' ] = float(form['nw_rad' ].value)
params['L_tf'   ] = float(form['L_tf'   ].value)
params['eps_1'  ] = float(form['eps_1'  ].value)
params['mu'     ] = float(form['mu'     ].value)
params['n_0'    ] = float(form['n_0'    ].value)
params['nw_type'] =       form['nw_type'].value
params['lay_ox' ] = float(form['lay_ox' ].value)
params['eps_2'  ] = float(form['eps_2'  ].value)
params['lay_bf' ] = float(form['lay_bf' ].value)
params['L_d'    ] = float(form['L_d'    ].value)
params['eps_3'  ] = float(form['eps_3'  ].value)
nw_len            = float(form['nw_len' ].value)
nw_rad            = float(form['nw_rad' ].value)
lay_ox            = float(form['lay_ox' ].value)
lay_bf            = float(form['lay_bf' ].value) 
L_d               = float(form['L_d'    ].value)
L_tf              = float(form['L_tf'   ].value)
eps_1             = float(form['eps_1'  ].value)
eps_2             = float(form['eps_2'  ].value)
eps_3             = float(form['eps_3'  ].value) 
mu                = float(form['mu'     ].value)
n_0               = float(form['n_0'    ].value)
nw_type           =       form['nw_type'].value 
comment           =       form['comment'].value
bfs_file_name     =       form['fileName'].value
# ........................................................................
# ------------------------------------------------------------------------ 


# ************************************************************************
# BioFET-SIM Start
# ........................................................................
# Starting BioFET-SIM calculation.
# Initializing the simulation. The simulation calls the charge
# distribution when the model starts the calculation.
def get_resp(ph, sim):
    #sim = SimMulti(target, copy.deepcopy(dist), dist, params)
    #sim = SimMulti(copy.deepcopy(dist))
    #sim.set_rho() 
    print sim.rho
    # Number of proteins on wire.
    if calc_num_prot == 'yes':
        #num_prot = bio_lib.get_num_prot(sim.rho, sim.params['nw_len'], sim.params['nw_rad']) 
        num_prot = bio_lib.get_num_prot(sim.rho, nw_len, nw_rad)
    else:
        # Use constant number of proteins.
        num_prot = int(form['num_prot_inp'].value) 
    # Results data container and setting label, base value and percentage range of results graph.
    results = []
    x_val = float(params[abs_axis])
    x_min = float(form[abs_axis+'_x_min'].value)
    x_max = float(form[abs_axis+'_x_max'].value)

    dG_G0 = round(bio_com.compute(sim.rho, nw_len, nw_rad, lay_ox, L_d, L_tf, lay_bf,
                          eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
    G0    = round(bio_lib.G0(nw_len, nw_rad, n_0, mu)) 
    return G0, dG_G0
# ........................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# Initialize charge distribution for pH range.
# ........................................................................
if __name__ == '__main__': 
    # Initialize charge distribution after move.
    rho = Rho(target, pdb_new)
    rho.load_pdb()
    rho.unique_residue_ids()
    rho.cluster_residues()
    rho.set_terminals()
    rho.set_RQ()
    rho.set_av_RQ()
    rho.set_pqr(target, rho.av_RQ, pH, open(bio_lib.pdb_base_path + target + '-reo.pka', 'r')) 
    print rho.pqr
    sys.exit(0)
    # Initialization of simulation object.
    # Simulation calls charge distribution when model starts calculation.
    #sim = SimMulti(target, copy.deepcopy(pqr_new), pqr_new, params)
    #sim.set_rho() 
    sim = SimMulti()
    sim.set_bfs_inp()

    # Configuration of protein population on NW.
    if calc_num_prot == 'yes':
        num_prot = bio_lib.get_num_prot(sim.bfs_inp, sim.param['nw_len'], sim.param['nw_rad']) 
    else:
        num_prot = int(form['num_prot_inp'].value) 

    # BFS response or pH response.
    if button_clicked == 'BioFET-SIM':
        print "BioFET-SIM"
    else: 
        pH_resp  = []
        pH_range = range(1,15)
        for pHi in pH_range:
            dist = rho.set_pqr(target,rho.av_RQ,pHi,open(bio_lib.pdb_base_path+target+'-reo.pka','r'))
            sim.set_rho(copy.deepcopy(dist)) 
            #pH_resp.append(get_resp(pHi, dist)[1])
            pH_resp.append(get_resp(pHi, sim)[1])
        bio_lib.prepare_pH_response_plot(target, pH_resp)
# ........................................................................
# ------------------------------------------------------------------------ 
