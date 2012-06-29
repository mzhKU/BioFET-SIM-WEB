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
    #def __init__(self, target, av_RQ, pqr, param):
    def __init__(self):
        #def __init__(self, target, av_RQ, pqr):
        """It appears, Jmol transfers data with unusual line delimiters,
        therefore the special split arguments.
        """
        # Reoriented charge distribution coming from Jmol.
        #self.target    = target 
        #self.av_RQ     = av_RQ.split('\r\n')
        #self.params     = params
        #self.pqr       = pqr.split('\r\n')
        #self.dist      = dist.split('\r\n')
        self.rho       = []
        #self.rho_pqr   = ''

    def set_rho(self, dist):
        """Combining the Jmol adjusted geometry with the charge
        from the PROPKA match.
        For historic reasons, the BFS compute unit requires the
        'm' property (number of charges in biomolecule).
        """
        # Convenience abbreviations.
        #av_RQ = self.av_RQ 
        #pqr   = self.pqr
        #rho = self.rho
        #cnt = 0
        # Prepare data for BFS calculation (in list format).
        #for av_rq_i in av_RQ:
        #    # Avoiding empty lines.
        #    if len(av_rq_i) != 0:
        #        # Avoiding 'MODEL'/'ENDMDL' in the Jmol out stream.
        #        if av_rq_i.split()[0] == 'ATOM': 
        #            r_i = av_rq_i[32:54] + pqr[cnt][54:61]
        #            rho.append(r_i.split())
        #            cnt += 1
        #self.m = len(rho)

        # Prepare data for BFS calculation (in list format).
        for dist_i in dist.split('\r\n'):
            # Avoid empty lines.
            if len(dist_i) != 0:
                # Avoid 'MODEL'/'ENDMDL' tags.
                if dist_i.split()[0] == 'ATOM':
                    r_i = dist_i[32:61]
                    self.rho.append(r_i.split()) 
        self.m = len(self.rho)
        
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
