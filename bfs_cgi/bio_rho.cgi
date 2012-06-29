#!/usr/bin/python

print "Content-type: text/html\n"

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
target = form['target'].value
pH     = float(form['pH'].value)

# **************************************************************************
from copy import deepcopy
import bio_lib
from bio_rho import Rho
import string
# ..........................................................................


# ************************************************************************
# LAUNCH
# ........................................................................
if __name__ == '__main__':
    response = ''
    from bio_rho import Rho
    rho = Rho(target, open(bio_lib.pdb_base_path + target + '-reo.pdb', 'r').read())
    rho.load_pdb()
    rho.unique_residue_ids()
    rho.cluster_residues()
    rho.set_terminals()
    rho.set_RQ()
    rho.set_av_RQ()
    rho.set_pqr(target, pH)
    # ------------------------------ 
    # Exporting Q_tot to Javascript on client side.
    Q_tot = bio_lib.calc_Q_tot(rho.pqr)
    response += "Q_tot=%4.2f;\n" % Q_tot
    # ------------------------------ 
    z_dim = bio_lib.get_box_dimensions(rho.pqr)[2]
    bio_lib.get_nw_surface(z_dim, target)
    bio_lib.write_pqr(target,pH,rho.pqr)
    # ------------------------------ 
    # Exporting charge distribution to client side.
    print response
# ------------------------------------------------------------------------
