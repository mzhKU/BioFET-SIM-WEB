#!/usr/local/bin/python

from copy import deepcopy
import bio_lib
import string

# ************************************************************************
# API:
# - set_RQ_coordinates(self)
# - parse_pdb(self)
# - unique_residue_ids(self)
# - cluster_residues(self)
class Rho:
    """Charge distribution model.
    
    ATTRIBUTES:
    - The variable namings follow the scheme: capital letters indicate
      a vector, e.g. RQ, is the vector of charge positions rq_i.
      Lists are named in plural form, in loops, the individual element
      is in singular form.

    API:
    - load_pdb
    - unique_residue_ids
    - cluster_residues
    - set_RQ
    """

    # ********************************************************************
    # Instantaniation
    def __init__(self, target, tmp_pdb):
        #self.pdb  = open(bio_lib.pdb_base_path + target + '-reo.pdb', 'r').readlines()
        self.pdb = tmp_pdb.split('\n')
        # For every atom in the data, the residue name, index and chain
        # is stored in the 'self.identifiers' attribute.
        self.identifiers = []
        self.c_terminals = []
        self.n_terminals = []
        # coords: x_i, y_i, z_i
        self.res_atm_xyz      = []
        # Unique residue identifier attributes.
        # 'self.res_ids': The first three elements are the
        # residue name, index and chain. Then the remaining
        # elements are the atom type and the coordinates of the atoms of
        # that residue. This is the most powerful datastructure of the
        # program.
        self.res_ids = []
        self.res_cnt = 0 
        self.atm_cnt = 0
        # Atoms to average coordinates.
        self.ion_atms = {'ASP':['OD1', 'OD2'],
                         'GLU':['OE1', 'OE2'],
                         'HIS':['CG', 'ND1', 'CD2', 'CE1', 'NE2'],
                         'CYS':['SG'],
                         'TYR':['OH'],
                         'LYS':['NZ'], 
                         'ARG':['CZ']}
        self.aa = ['ALA', 'ARG', 'ASN', 'ASP', 'CYS',
                   'GLU', 'GLN', 'GLY', 'HIS', 'ILE',
                   'LEU', 'LYS', 'MET', 'PHE', 'PRO',
                   'SER', 'THR', 'TRP', 'TYR', 'VAL']
        self.ion_res = self.ion_atms.keys()
        self.RQ      = [] # Atoms to average.
        self.av_RQ   = [] # Positions of the charges.
        #self.chain   = Chain()
    # ....................................................................  

    # ********************************************************************
    # Setting which atoms are included in the averaging;
    # Setting the average of coordinates.
    def set_RQ(self): 
        """Identifying the location of the atoms for which to take
        the average as the point where the charge is located.
        """ 
        # Convenience abbreviations.
        ion_atms = self.ion_atms # Atoms to average dictionary
        ion_res  = self.ion_res  # Ionizable residues
        RQ       = self.RQ       # list of q_i coordinates
        for res_id in self.res_ids:
            if res_id[0] in ion_res:
                # Atoms to average.
                av_atms = []
                # Omitting the residue id at the 0 position in the
                # 'res'-list, therefore 'res_id[3:]'.
                # 'atm.split()[0]' returns the atom type.
                for atm in res_id[3:]:
                    if atm.split()[0] in ion_atms[res_id[0]]:
                        av_atms.append(" ".join(res_id[:3])\
                                     + " " + atm.strip())
                RQ.append(av_atms) 
        self.RQ = RQ
    
    def set_av_RQ(self):
        """Computing average location based on 'self.RQ'
        """
        for ion_res in self.RQ:
            self.av_RQ.append(bio_lib.av_res(ion_res))
        for trm in self.c_terminals:
            self.av_RQ.append(bio_lib.av_trm(trm))
        for trm in self.n_terminals:
            self.av_RQ.append(bio_lib.av_trm(trm))

    def set_pqr(self, target, av_RQ, pH, pka_dat):
        """Generating the PQR file for the Jmol input.
        """
        self.pqr = bio_lib.set_pqr(target, av_RQ, pH, pka_dat)
    # ....................................................................  

    # ********************************************************************
    # Parsing of PDB; Establishing unique residue identifier set;
    # Clustering residues.
    def load_pdb(self): 
        """Load and structure PDB data.
        FIX:
        - Discard tags other than 'ATOM'
        - Include treatment of LIG/HETATM
        """
        # 'atoms': list with the residue id for every atom.
        pdb = self.pdb
        for l_i in range(len(pdb)): 
            dat = bio_lib.get_labels(pdb[l_i])
            res_atm = dat[0]
            res_nam = dat[1]
            res_ind = dat[2]
            res_chn = dat[3]
            self.identifiers.append([res_nam, res_ind, res_chn]) 
            #x_i     = dat[4]
            #y_i     = dat[5]
            #z_i     = dat[6]
            # Adjusted coordinates returned from PDB are not strictly formatted.
            if len(pdb[l_i]) > 10:
                x_i     = pdb[l_i][31:].split()[0]
                y_i     = pdb[l_i][31:].split()[1]
                z_i     = pdb[l_i][31:].split()[3]
            c_i = " ".join([res_atm, x_i, y_i, z_i])
            self.res_atm_xyz.append(c_i) 

    def unique_residue_ids(self): 
        """Sets a list as
        [['LYS', '2', 'A'], ['LYS', '2', 'A'], ... ]
        For every atom of the structure, its residue data 
        is being set in the list.
        """ 
        # Convenience abbreviations.
        identifiers = self.identifiers
        res_ids = self.res_ids
        res_cnt = self.res_cnt 
        # Preparing the list of unique residue identifiers.
        # In the end it should be: res_cnt == len(res_ids)-1.
        # The 'elif' line is controlling that only unique
        # identifiers are collected.
        for identifier in identifiers:
            if len(res_ids) == 0:
                # Require 'deepcopy', otherwise constant change
                # of 'res_ids[res_cnt]' with 'identifier'.
                res_ids.append(deepcopy(identifier))
            elif identifier[1] == res_ids[res_cnt][1]: 
                pass
            else:
                res_ids.append(deepcopy(identifier))
                res_cnt += 1 
        # Return assignments to object scope.
        self.res_ids = res_ids
        self.res_cnt = res_cnt

    def set_terminals(self, n_chains=1):
        """Set N+ and C- terminals.
        Run over all clustered residues and select 'OXT' and N+' and
        add to self.terminals.  
        For every chain, there is a 'OXT' and a 'N+' terminus.
        """ 
        res_ids   = self.res_ids
        c_terminals = self.c_terminals
        n_C_trms = self.get_n_chains()
        res_id_cnt = 0
        # Only gets the terminals from the first chain.
        for res_id in res_ids:
            if res_id[2] in string.lowercase or string.uppercase:
                atm_chn_i = res_id[2]
            for atm in res_id:
                #atm_chn_i = res_id[2]
                #if n_N_trms > 0:
                #    if atm.split()[0] == 'N':
                #        n_N_trms -= 1
                #        trm_id = " ".join(res_id[:3]) + " " + atm
                #        terminals.append(trm_id)
                if n_C_trms > 0:
                    if atm.split()[0] == 'OXT':
                        n_C_trms -= 1
                        trm_id = " ".join(res_id[:3]) + " " + atm
                        c_terminals.append(trm_id)
                res_id_cnt+=1
        self.c_terminals = c_terminals 
        self.n_terminals = self.get_n_terminals()

    def get_n_terminals(self):
        # <<EDIT>>
        # Extend documentation and testing.
        res_id_cnt = 0
        n_terminals = []
        for res_id in self.res_ids:
            # Check if 'res_id[0]' is an amino acid.
            if res_id[0] in self.aa:
                # Append first 'N' to 'n_terminals'.'.
                if res_id_cnt == 0:
                        n_terminals.append(" ".join(res_id[0:3]) + " " + res_id[3])
                # Only append 'N' to 'n_terminals', when chain ID changes.
                else:
                    # Avoid apparent chain IDs.
                    #if res_id_cnt > 0:
                    # Check if the chain ID ('A', 'B', ...) changed.
                    # If no change: no append to 'n_terminals'.
                    #print res_id[2], self.res_ids[res_id_cnt-1][2]
                    if res_id[2] == self.res_ids[res_id_cnt-1][2]:
                        pass
                    # If chain ID change, append first 'N' to 'n_terminals'.
                    else:
                        n_terminals.append(" ".join(res_id[0:3]) + " " + res_id[3])
                res_id_cnt += 1
        return n_terminals

    def get_n_chains(self):
        """Compute the number of chains based on how many times
        the chain identifier changes.
        """ 
        res_id_cnt = 0
        tot_n_res = len(self.res_ids)
        n_chns = 0
        for res_id in self.res_ids:
            res_chn_i = res_id[2]
            if res_id_cnt > 1:
                if res_chn_i == self.res_ids[res_id_cnt-1][2]:
                    pass
                else:
                    n_chns+=1
            res_id_cnt+=1
        return n_chns 

    def cluster_residues(self): 
        """The generated list is of the below shape: 
        [..., [res_i, [x_i1, y_i1, z_i1], [x_i2, y_i2, z_i2], ...], ...] 
        where 'res_i' is [res_nam, res_ind, res_chn]'.
        All atoms of a residue are in one list, where the first element
        is the index of that residue in the PDB file. This index will
        correspond to the index of the residue in the pKa file.
        """ 
        # Convenience abbreviations for local method scope.
        identifiers   = self.identifiers
        res_ids = self.res_ids
        res_atm_xyz  = self.res_atm_xyz
        atm_cnt = 0
        res_cnt = 0 
        # Run over 'starts'. len(starts) is equal to number of atoms.
        # To every residue identifier, append the corresponding atoms.
        # 'res_id[k, 1:]': are the atoms [1:] of the k residue.
        # Run over residue id, increment atom index, when residue id
        # changes, increment atom index and residue index.  
        # In every step, append the atom coordinates to the first
        # element, which is the three identifier labels.
        for identifier in identifiers: 
            if identifier[1] == res_ids[res_cnt][1]:
                res_ids[res_cnt].append(res_atm_xyz[atm_cnt])
                atm_cnt+=1
            else:
                res_cnt+=1
                res_ids[res_cnt].append(res_atm_xyz[atm_cnt])
                atm_cnt+=1
        # Return assignments to object scope.
        self.identifiers = identifiers
        self.atm_cnt = atm_cnt
        self.res_ids = res_ids
        self.res_cnt = res_cnt
    # ....................................................................  
# ------------------------------------------------------------------------

"""
# ************************************************************************
# LAUNCH
# ........................................................................
if __name__ == '__main__':
    target = '1AVD'
    pH     = 7.4

    rho = Rho(target)
    rho.load_pdb()

    rho.unique_residue_ids()
    for i in rho.res_ids:
        print i
    print

    rho.cluster_residues()

    rho.set_terminals()
    print "rho.n_terminals, rho.c_terminals"
    print rho.n_terminals
    print rho.c_terminals 
    print

    rho.set_RQ()
    rho.set_av_RQ()

    print "rho.RQ"
    for RQ_i in rho.RQ:
        print RQ_i 
    print 

    print "rho.av_RQ"
    for av_RQ_i in rho.av_RQ:
        print av_RQ_i
    print
    
    print "rho.set_pqr"
    pka_dat = bio_lib.calc_pKas(target)
    rho.set_pqr(target, rho.av_RQ, pH, pka_dat)
    for pqr_i in rho.pqr.split('\n')[:10]:
        print pqr_i
# ------------------------------------------------------------------------
"""
