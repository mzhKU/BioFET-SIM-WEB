#!/Library/Frameworks/Python.framework/Versions/Current/bin/python

print "Content-type: text/plain\n"

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
target = form['target'].value

import os.path
from subprocess import Popen, PIPE
import string

# ***********************************************************************
# Global application scope variables.
import bio_lib
# .......................................................................

def rechain(target):
    """Rechaining:
    [MODEL1 (Chain A, Chain B, ...), MODEL2 (Chain A, Chain B, ...), ...]
    into 
    [MODEL1 (Chain A, Chain B, Chain C, ...)]
    Discarding **non**-'ATOM', -'TER', -'ENDMDL' and -'MODEL' lines from the
    PDB file. Piping the awk stream directly to the 'val' variable used
    for rechaining."""
    if not os.path.exists(bio_lib.pdb_base_path + target + '-rec.pdb'):
        awk_cmd = ['awk', '/(ATOM|^TER|ENDMDL|MODEL)/,//']
        awkp = Popen(awk_cmd, stdin=open(bio_lib.pdb_base_path + target + '.pdb', 'r'),
                     stdout=PIPE, stderr=PIPE, shell=False)
        val = awkp.stdout.readlines()
        rec = open(bio_lib.pdb_base_path + target + '-rec.pdb', 'w')
        # For security, 'model_id' is string, so it can not be used in 
        # mathematical operations. Here maxium 10 chains.
        codes = zip(range(1, 18), string.uppercase)
        models = [] 
        # Determine how many 'MODEL's are in the structure.
        mdl_cnt = 1
        for line in val:
            if len(line.split()) > 0:
                if line.split()[0] == 'MODEL':
                    models.append([str(mdl_cnt)])
                    mdl_cnt+=1
        # Determine how many 'TER's are in each model.
        mdl_cnt = -1
        ter_cnt = 0
        for line in val:
            if len(line.split()) > 0:
                if line.split()[0] == ('MODEL'):
                    # Set 'TER' and 'MODEL' counter.
                    #ter_cnt = 0
                    mdl_cnt += 1
                if line.split()[0] == ('TER'):
                    ter_cnt += 1
                models[mdl_cnt].append(ter_cnt) 
        # Generate unique chain identifiers.  
        atm_tot = 0
        for mdl in models:
            atm_tmp = 0
            # mdl:                        ['1', 0, 0, ..., 1, 1]
            # mdl_tmp:                    [     0, 0, ..., 1, 1]
            # mdl_tmp[atm_cnt]:           0
            # codes:                      [(1, 'A'), (2, 'B'), (3, 'C'), ...]
            # codes[mdl_tmp[atm_cnt]]:    (1, 'A')
            # codes[mdl_tmp[atm_cnt]][1]: 'A' 
            # NOTICE:
            # - 'atm_tot': Counts over all lines in the file.
            # - 'atm_tmp': Counts over all lines of a MODEL.
            for atm in mdl[1:]:
                #<CHECK_LINE>
                line_length = len(val[atm_tot])
                if line_length < 20:
                    op = val[atm_tot]
                else:
                    op = val[atm_tot][:20]\
                            + ' ' + codes[mdl[1:][atm_tmp]][1]\
                            + ' ' + val[atm_tot][23:]
                #op = val[atm_tot][:20]\
                #        + ' ' + codes[mdl[1:][atm_tmp]][1]\
                #        + ' ' + val[atm_tot][23:]
                rec.write(op)
                atm_tmp+=1
                atm_tot+=1 
        rec.close()
        print "Rechaining done."

if __name__ == "__main__":
    rechain(target)
