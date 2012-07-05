import bio_lib
# ************************************************************************
# CLASS: SimMulti
# - Represents the simulation of the multiple charge model.
# ........................................................................
class SimMulti:
    """
    Fix:
    - Append float instead of string to 'rho'.
    - Refactor 'res_ids' and 'coords'.
    """ 
    def __init__(self):
        self.foo =  "bar"

    def set_bfs_inp(self, pqr):
        """
        Combining the Jmol adjusted geometry with the charge from the PROPKA match.
        BFS compute unit requires the 'm' property (number of charges in biomolecule).
        """
        self.bfs_inp = []
        # Prepare data for BFS calculation (in list format).
        # Avoid empty lines, 'MODEL' and 'ENDMDL' tags.
        for pqr_i in pqr.split('\n'):
            if len(pqr_i) != 0:
                if pqr_i.split()[0] == 'ATOM':
                    self.bfs_inp.append(pqr_i[32:61].split())
        self.m = len(self.bfs_inp)
    # ....................................................................
# ------------------------------------------------------------------------ 


# ************************************************************************
# CLASS: SimSingl
# - Reprents the simulation of the single charge model.
# ........................................................................
class SimSingle:
    """
    Description
    - No charge distribution.
    - Single charge located at bounding box center.
    """ 
    def __init__(self):
        self.foo =  "bar"

    def set_bfs_inp(self, pqr):
        """
        Combining the Jmol adjusted geometry with the charge from the PROPKA match.
        BFS compute unit requires the 'm' property (number of charges in biomolecule).
        """
        self.bfs_inp = []
        self.bfs_inp.append(self.get_single_charge_representation_of_pqr(pqr))
        self.m = len(self.bfs_inp)

    def get_single_charge_representation_of_pqr(self, pqr):
        """
        Place Q_tot at PQR bounding box center.
        """
        z_atms = []
        for pqr_i in pqr.split('\n'):
            # Get z-coordinate of the charge.
            z_atms.append(float(pqr_i.split()[7]))
        z_max = max(z_atms)
        z_min = min(z_atms)
        dz    = z_max - z_min
        z_Q   = dz/2.0
        Q_tot = bio_lib.calc_Q_tot(pqr)
        return ['0.000', '0.000', '%5.3f' % z_Q, '%5.3f' % Q_tot]
    # ....................................................................
# ------------------------------------------------------------------------ 
