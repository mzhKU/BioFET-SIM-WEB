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
from numpy import arange

# ************************************************************************
# READ FORM DATA AND EXTERNAL CALCULATION SETUP
# ........................................................................
# Obtaining properties from the HTML form.
form    = cgi.FieldStorage()
target  = form['targetLab'].value 
tmp_pqr = form['tmp_pqr'].value
pdb_new = bio_lib.rewrite_pdb(target, tmp_pqr)
# Should BioFET-SIM single or multiple charge model be used.
charge_model      = form['model'].value
# Handling the "Number of Proteins on NW" checkbox. Use default value if checked.
if form.getvalue('num_prot_box'):
    calc_num_prot = "no"
else:
    calc_num_prot = "yes"
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
# CLASS: SimMulti
# - Represents the simulation of the multiple charge model.
# ........................................................................
class SimMulti:
    """
    FIX:
    - Append float instead of string to 'rho'.
    - Refactor 'res_ids' and 'coords'.
    """ 
    # ********************************************************************
    # Initializing simulation.
    def __init__(self, target, av_RQ, pqr, param):
        #def __init__(self, target, av_RQ, pqr):
        """It appears, Jmol transfers data with unusual line delimiters,
        therefore the special split arguments.
        """
        # Reoriented charge distribution coming from Jmol.
        self.target    = target 
        self.av_RQ     = av_RQ.split('\n')
        self.param     = param
        self.pqr       = pqr.split('\n')
        self.rho       = []
        self.rho_pqr   = ''

    def set_rho(self):
        """Combining the Jmol adjusted geometry with the charge
        from the PROPKA match.
        For historic reasons, the BFS compute unit requires the
        'm' property (number of charges in biomolecule).
        """
        # Convenience abbreviations.
        av_RQ = self.av_RQ 
        pqr   = self.pqr
        rho = self.rho
        cnt = 0
        # Prepare data for BFS calculation (in list format).
        for av_rq_i in av_RQ:
            # Avoiding empty lines.
            if len(av_rq_i) != 0:
                # Avoiding 'MODEL'/'ENDMDL' in the Jmol out stream.
                if av_rq_i.split()[0] == 'ATOM': 
                    r_i = av_rq_i[32:54] + pqr[cnt][54:61]
                    rho.append(r_i.split())
                    cnt += 1
        self.m = len(rho)
    
    def get_x_range(self, x_val, percentage_range):
        """Generating the range for which to plot the sensitivity.
        """
        ini = x_val*(1.0-percentage_range/100.0)
        fin = x_val*(1.0+percentage_range/100.0)
        dif = (fin-ini)/100.0
        return numpy.arange(ini, fin+dif, dif)
    # ....................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# BioFET-SIM Start
# ........................................................................
# Starting BioFET-SIM calculation.
# Initializing the simulation. The simulation calls the charge
# distribution when the model starts the calculation.
def get_pH_resp(ph, dist):
    print "dist"
    print dist
    sim = SimMulti(target, copy.deepcopy(dist), dist, params)
    sim.set_rho() 
    print sim.rho
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
    return dG_G0
# ........................................................................
# ------------------------------------------------------------------------ 

# ************************************************************************
# Initialize charge distribution for pH range.
# ........................................................................
if __name__ == '__main__': 
    pH_resp = []
    rho = Rho(target, pdb_new)
    rho.load_pdb()
    rho.unique_residue_ids()
    rho.cluster_residues()
    rho.set_terminals()
    rho.set_RQ()
    rho.set_av_RQ()
    dist = rho.set_pqr(target, rho.av_RQ, 7.4, open(bio_lib.pdb_base_path + target + '-reo.pka', 'r'))
    print get_pH_resp(7.4, dist)
# ........................................................................
# ------------------------------------------------------------------------ 
