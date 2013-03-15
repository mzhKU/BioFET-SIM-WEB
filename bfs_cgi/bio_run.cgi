#!/usr/bin/python

#print "Content-type: text/plain\n"

# ************************************************************************
# Required.
# ........................................................................
import cgi, cgitb; cgitb.enable() 
from numpy import arange
from bio_mod import SimMulti, SimSingle
from bio_rho import Rho
import bio_lib
import bio_com 
import copy
import sys
# ........................................................................
# ------------------------------------------------------------------------ 


# ************************************************************************
# READ FORM DATA AND EXTERNAL CALCULATION SETUP
# - Charge model
# - Number of proteins
# ........................................................................
form              = cgi.FieldStorage()
target            =       form['targetLab'].value 
tmp_pdb           =       form['tmp_pdb'].value
pdb_new           = bio_lib.rewrite_pdb(target, tmp_pdb)
button_clicked    =       form['action'].value 
charge_model      =       form['model'].value
x_lbl             =       form['abs'].value
x_val             = float(form[x_lbl].value)
pH                = float(form['pH'].value)
if form.getvalue('overwrite_num_prot'):
    calc_num_prot = "no"
else:
    calc_num_prot = "yes"
params            = {}
params['nw_len' ] = float(form['nw_len'  ].value)
params['nw_rad' ] = float(form['nw_rad'  ].value)
params['L_tf'   ] = float(form['L_tf'    ].value)
params['eps_1'  ] = float(form['eps_1'   ].value)
params['mu'     ] = float(form['mu'      ].value)
params['n_0'    ] = float(form['n_0'     ].value)
params['nw_type'] =       form['nw_type' ].value
params['lay_ox' ] = float(form['lay_ox'  ].value)
params['eps_2'  ] = float(form['eps_2'   ].value)
params['lay_bf' ] = float(form['lay_bf'  ].value)
params['L_d'    ] = float(form['L_d'     ].value)
params['eps_3'  ] = float(form['eps_3'   ].value)
nw_len            = float(form['nw_len'  ].value)
nw_rad            = float(form['nw_rad'  ].value)
lay_ox            = float(form['lay_ox'  ].value)
lay_bf            = float(form['lay_bf'  ].value) 
L_d               = float(form['L_d'     ].value)
L_tf              = float(form['L_tf'    ].value)
eps_1             = float(form['eps_1'   ].value)
eps_2             = float(form['eps_2'   ].value)
eps_3             = float(form['eps_3'   ].value) 
mu                = float(form['mu'      ].value)
n_0               = float(form['n_0'     ].value)
nw_type           =       form['nw_type' ].value 
comment           =       form['comment' ].value
bfs_file_name     =       form['fileName'].value
# ........................................................................
# ------------------------------------------------------------------------ 


# ************************************************************************
# BioFET-SIM Start
# ........................................................................
# Starting BioFET-SIM calculation.
# Initializing the simulation. The simulation calls the charge
# distribution when the model starts the calculation.
def get_resp(sim):
    dG_G0 = round(bio_com.compute(sim.bfs_inp, nw_len, nw_rad, lay_ox, L_d, L_tf, lay_bf,
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

    # Instance of simulation object.  
    if charge_model == 'singl':
        sim = SimSingle()
    else:
        sim = SimMulti()

    # BFS response.
    if button_clicked == 'BioFET-SIM':
        bfs_resp = ""
        rho.set_pqr(target, pH)
        sim.set_bfs_inp(rho.pqr)
        # Configuration of protein population on NW.
        #print sim.bfs_inp
        if calc_num_prot == 'yes':
            num_prot = int(bio_lib.get_num_prot(sim.bfs_inp, nw_len, nw_rad))
        else:
            num_prot = int(form['num_prot_inp'].value) 

        # Base conductance and sensitivity.
        G0, dG_G0 = get_resp(sim)

        # Return base conductance and sensitivity to client.
        print "g0=%6.6f;dg0_g0=%6.6f;num_prot=%d" % (G0, dG_G0, bio_lib.get_num_prot(sim.bfs_inp, nw_len, nw_rad))

        x_min = float(form[x_lbl+'_x_min'].value)
        x_max = float(form[x_lbl+'_x_max'].value)
        if x_lbl == 'nw_len':
            for x in arange(x_min, x_max, (x_max-x_min)/100.0): 
                dG_G0 = round(bio_com.compute(sim.bfs_inp, x, nw_rad, lay_ox, L_d, L_tf, lay_bf,
                                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
                bfs_resp += "%4.5f %4.5f\n" % (x, dG_G0)
        if x_lbl == 'nw_rad':
            for x in arange(x_min, x_max, (x_max-x_min)/100.0): 
                dG_G0 = round(bio_com.compute(sim.bfs_inp, nw_len, x, lay_ox, L_d, L_tf, lay_bf,
                                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
                bfs_resp += "%4.5f %4.5f\n" % (x, dG_G0)
        if x_lbl == 'lay_ox':
            for x in arange(x_min, x_max, (x_max-x_min)/100.0): 
                dG_G0 = round(bio_com.compute(sim.bfs_inp, nw_len, nw_rad, x, L_d, L_tf, lay_bf,
                                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
                bfs_resp += "%4.5f %4.5f\n" % (x, dG_G0)
        if x_lbl == 'L_tf':
            for x in arange(x_min, x_max, (x_max-x_min)/100.0): 
                dG_G0 = round(bio_com.compute(sim.bfs_inp, nw_len, nw_rad, lay_ox, L_d, x, lay_bf,
                                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
                bfs_resp += "%4.5f %4.5f\n" % (x, dG_G0)
        if x_lbl == 'L_d':
            for x in arange(x_min, x_max, (x_max-x_min)/100.0): 
                dG_G0 = round(bio_com.compute(sim.bfs_inp, nw_len, nw_rad, lay_ox, x, L_tf, lay_bf,
                                      eps_1, eps_2, eps_3, n_0, nw_type, num_prot), 8)
                bfs_resp += "%4.5f %4.5f\n" % (x, dG_G0)
        bio_lib.prepare_results(target, bfs_resp, x_val, x_lbl, num_prot, dG_G0, G0)
        bio_lib.generate_bfs_input(target, params, sim, num_prot, comment, bfs_file_name)

    # pH response.
    else: 
        # Base conductance and sensitivity.
        rho.set_pqr(target, pH)
        sim.set_bfs_inp(rho.pqr)
        # Configuration of protein population on NW.
        if calc_num_prot == 'yes':
            num_prot = int(bio_lib.get_num_prot(sim.bfs_inp, nw_len, nw_rad))
        else:
            num_prot = int(form['num_prot_inp'].value) 
        G0, dG_G0 = get_resp(sim)

        # Return base conductance and sensitivity to client.
        print "g0=%4.4f;dg0_g0=%4.4f" % (G0, dG_G0) 

        pH_resp  = ""
        pH_range = range(0, 15)
        for pHi in pH_range:
            rho.set_pqr(target, pHi)
            sim.set_bfs_inp(rho.pqr)
            # Configuration of protein population on NW.
            if calc_num_prot == 'yes':
                num_prot = int(bio_lib.get_num_prot(sim.bfs_inp, nw_len, nw_rad))
            else:
                num_prot = int(form['num_prot_inp'].value) 
            rho.q_tot = bio_lib.calc_Q_tot(rho.pqr)
            pH_resp += "%4.2f %4.5f\n" % (pHi, get_resp(sim)[1])
        bio_lib.prepare_pH_response_plot(target, pH_resp)
# ........................................................................
# ------------------------------------------------------------------------ 
