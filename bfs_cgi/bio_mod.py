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
    def __init__(self):
        self.foo =  "bar"

    def set_bfs_inp(self, pqr):
        """Combining the Jmol adjusted geometry with the charge from the PROPKA match.
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
class SimSingl:
    """
    DOCUMENT
    - No charge distribution.
    - Single charge located at bounding box center.
    """ 
    # ********************************************************************
    # Initializing simulation.
    def __init__(self, target, av_RQ, pqr, param, Q_tot):
        #def __init__(self, target, av_RQ, pqr):
        """It appears, Jmol transfers data with unusual line delimiters,
        therefore the special split arguments.
        """
        # Reoriented charge distribution coming from Jmol.
        self.target = target 
        self.av_RQ  = av_RQ.split('\r\n')
        self.param  = param
        self.pqr    = pqr.split('\r\n')
        self.rho    = [] 
        self.Q_tot  = float(Q_tot)
    
    def set_rho(self):
        """Place Q_tot in center of PQR bounding box.
        """
        z_atms = []
        for atm in self.pqr:
            # Get z coordinate of the charge.
            z_atms.append(float(atm.split()[7]))
        z_max = max(z_atms)
        z_min = min(z_atms)
        dz    = z_max - z_min
        z_Q   = dz/2.0
        #print z_max, z_min, dz, z_Q
        self.rho.append(['0.000', '0.000', '%5.3f' % z_Q, '%5.3f' % self.Q_tot])
        self.m = len(self.rho) 
    # ....................................................................
# ------------------------------------------------------------------------ 
