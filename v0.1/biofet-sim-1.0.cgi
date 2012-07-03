#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()
import time
import string
#import numpy as np
import Numeric as np
from scipy.special import i0, i1, k0, k1
import os

greekpi = 3.14159265358979323846264338327950288419716939937510
elem_charge = 1.602176487E-19 # Coulomb
h_bar = 1.054571628E-34 # reduced Plank's constant
Epsilon_0 = 8.854187817e-12 # vacuum permittivity
el_mass = 9.10938215e-31 # electron mass at rest

print "Content-Type: text/html\n\n"

def go(form):
    os.chdir('/var/www/propka/biofet-sim/v0.1/output')
    results = compute_results(form)
    make_data(results)
    make_graph(results)
    page = make_page(results)
    print page
    return

def setID(time):
    """
        Given a floating point time.time(), generate an ID.
        Use the tenths of a second to differentiate.

        Parameters
            time:  The current time.time() (float)
        Returns
            id  :  The file id (string)
    """
    strID = "%s" % time
    period = string.find(strID, ".")
    uid = "%s%s" % (strID[:period], strID[(period+1):(period+2)])
    return uid

def compute_results(form):
    results = {}
    uniqueID = setID(time.time())
    results['ID'] = uniqueID
    
    # get the values
    
    Big_L     = float(form['Big_L'    ].value)     
    Big_R     = float(form['Big_R'    ].value)     
    Delta_R   = float(form['Delta_R'  ].value)   
    Small_l   = float(form['Small_l'  ].value)   
    Lambda_d  = float(form['Lambda_d' ].value)  
    Lambda_tf = float(form['Lambda_tf'].value) 
    Epsilon_1 = float(form['Epsilon_1'].value) 
    Epsilon_2 = float(form['Epsilon_2'].value) 
    Epsilon_3 = float(form['Epsilon_3'].value) 
    Small_N   = float(form['Small_N'  ].value)   
    Small_Q   = float(form['Small_Q'  ].value)   
    Big_N     = float(form['Big_N'    ].value)     
    Big_Q     = float(form['Big_Q'    ].value)     
    n_0       = float(form['n_0'      ].value)
    mu        = float(form['mu'       ].value) 
    ms        = float(form['ms'	      ].value)
    
    np_type = form['TYPE'].value
    
    results['Big_L']	= Big_L    
    results['Big_R']	= Big_R    
    results['Delta_R']  = Delta_R  
    results['Small_l']  = Small_l  
    results['Lambda_d'] = Lambda_d 
    results['Lambda_tf']= Lambda_tf
    results['Epsilon_1']= Epsilon_1
    results['Epsilon_2']= Epsilon_2
    results['Epsilon_3']= Epsilon_3
    results['Small_N']  = Small_N  
    results['Small_Q']  = Small_Q  
    results['Big_N']	= Big_N    
    results['Big_Q']	= Big_Q    
    results['n_0']	= n_0      
    results['mu']	= mu	    
    results['np_type']  = np_type
    results['ms']       = ms
    
    # compute the results
    
    DeltaG_G0_value = DeltaG_G0_New(Big_R, Delta_R, Small_l, Lambda_d, Lambda_tf, Epsilon_1, Epsilon_2, Epsilon_3, Big_L, Big_N, Big_Q, Small_N, Small_Q, n_0, np_type)
    
    results['DG_G0'] = DeltaG_G0_value
    
    Big_R_NEW   = Big_R   * 1E-9 
    Big_L_NEW   = Big_L   * 1E-9
    G0 = greekpi * Big_R_NEW**2 * elem_charge * n_0 * mu / Big_L_NEW
    
    results['G0'] = G0
    
    results['DG'] = DeltaG_G0_value * G0
    
    results['G'] = G0 + (DeltaG_G0_value * G0)
    
    # prepare for the graph
    
    WhichX = form['GraphX'].value
    results['WhichX'] = WhichX
    
    if (form['RANGE'].value == 'Fixed'):
        percentage = float(form['FIXED'].value) / 100
	basevalue = float(form[WhichX].value)
	bottom = basevalue * (1.0 - percentage)
        top    = basevalue * (1.0 + percentage)
    else:
	bottom = float(form['XMin'].value)
	top    = float(form['XMax'].value)
    
    step = (top-bottom)/100
    eX = np.arange(bottom, top+step, step)
    
    results['bottom'] = bottom
    results['top'] = top
    results['step'] = step
    results['eX'] = eX
    
    # set the y and the x axis label

    if   (WhichX == 'Big_L'    ):
          Big_L = eX
          xlabel = 'Wire length {/Times-Italic L} (nm)'
    elif (WhichX == 'Big_R'    ):
          Big_R = eX
          xlabel = 'Wire radius {/Times-Italic R} (nm)'
    elif (WhichX == 'Delta_R'  ):
          Delta_R = eX
          xlabel = 'Oxide layer thickness {/Symbol D}{/Times-Italic R} (nm)'
    elif (WhichX == 'Small_l'  ):
          Small_l = eX
          xlabel = 'Charge Surface distance {/Times-Italic l} (nm)'
    elif (WhichX == 'Lambda_d' ):
          Lambda_d = eX
          xlabel = 'Solvent Debye length {/Symbol l}_{/Times-Italic D} (nm)'
    elif (WhichX == 'Lambda_tf'):
          n_0 = Get_n_0(eX, results)
          Lambda_tf = eX
          xlabel = 'Wire Thomas-Fermi length {/Symbol l}_{{/Times-Italic TF}} (nm)'
    elif (WhichX == 'Epsilon_1'):
          Epsilon_1 = eX
          xlabel = 'Permittivity of the wire {/Symbol e}_1 (E_0)'
    elif (WhichX == 'Epsilon_2'):
          Epsilon_2 = eX
          xlabel = 'Permittivity of the oxide {/Symbol e}_2 (E_0)'
    elif (WhichX == 'Epsilon_3'):
          Epsilon_3 = eX
          xlabel = 'Permittivity of the solvent {/Symbol e}_3 (E_0)'
    elif (WhichX == 'Small_N'  ):
          Small_N = eX
          xlabel = 'No. of charges directly on the wire'
    elif (WhichX == 'Small_Q'  ):
          Small_Q = eX
          xlabel = 'Charge of charges directly on the wire {/Times-Italic q} (e)'
    elif (WhichX == 'Big_N'    ):
          Big_N = eX
          xlabel = 'No. of charges off the wire'
    elif (WhichX == 'Big_Q'    ):
          Big_Q = eX
          xlabel = 'Charge of charges off the wire {/Times-Italic Q} (e)'
    
    whY = DeltaG_G0_New(Big_R, Delta_R, Small_l, Lambda_d, Lambda_tf, Epsilon_1, Epsilon_2, Epsilon_3, Big_L, Big_N, Big_Q, Small_N, Small_Q, n_0, np_type)
    
    results['xlabel'] = xlabel
    results['whY'] = whY
    
    return results
    
def DeltaG_G0_New(Big_R = 36.5, Delta_R = 2.0, Small_l = 2.0, Lambda_d = 2.3, Lambda_tf = 1.0, Epsilon_1 = 12.0, Epsilon_2 = 3.9, Epsilon_3 = 78.0, Big_L = 2000.0, Big_N = 7500, Big_Q = 4.0, Small_N = 10000, Small_Q = 1.0, n_0 = 6e23, np_type='n'):

    gamma_ox = Gamma_Oxide(Big_R, Delta_R, Lambda_d, Lambda_tf, Epsilon_1, Epsilon_2, Epsilon_3)
    gamma_l  = Gamma_l(Big_R, Small_l, Lambda_d)

    sigma_s = Sigma_s(Big_R, Delta_R, 0.0, Big_L, Small_N, Small_Q)
    sigma_b = Sigma_s(Big_R, Delta_R, Small_l, Big_L, Big_N, Big_Q)

    # converts to metre

    Big_R_NEW   = Big_R   * 1E-9 

    deltaG_G0 = gamma_ox * (gamma_l * sigma_b + sigma_s) * 2 / (Big_R_NEW * elem_charge * n_0)

    if np_type == 'p':
        deltaG_G0 = -1 * deltaG_G0

    return deltaG_G0

def Gamma_Oxide(Big_R = 36.5, Delta_R = 2.0, Lambda_d = 2.3, Lambda_tf = 1.0, Epsilon_1 = 12.0, Epsilon_2 = 3.9, Epsilon_3 = 78.0):

    fact1 = (Big_R + Delta_R) / Lambda_d
    fact2 = Big_R / Lambda_tf
    fact3 = fact1**(-1)
    fact4 = (Big_R + Delta_R) / Big_R

    numerator = Epsilon_1 * k0(fact1) * (Lambda_d/Lambda_tf) * i1(fact2)
    denominator = (k0(fact1) * fact3 + np.log(fact4) * k1(fact1) * (Epsilon_3/Epsilon_2)) * Epsilon_1 * fact2 * i1(fact2) + Epsilon_3 * k1(fact1) * i0(fact2)

    gamma_ox = numerator / denominator

    return gamma_ox

def Gamma_l(Big_R = 36.5, Small_l = 2.0, Lambda_d = 2.3):

    distfactor = Big_R / (Big_R + Small_l)

    gamma_l = 2 * distfactor * ((1 + np.sqrt (distfactor) * np.exp (Small_l/Lambda_d))**(-1))

    return gamma_l

def Sigma_s(Big_R = 36.5, Delta_R = 2.0, Small_l = 4.0, Big_L = 2000.0, Big_N = 15000, Big_Q = 4.0):

    # converts to metre

    Big_R   = Big_R   * 1E-9 
    Delta_R = Delta_R * 1E-9 
    Small_l = Small_l * 1E-9
    Big_L   = Big_L   * 1E-9

    # converts to coulomb

    Big_Q   = Big_Q   * elem_charge

    sigma_s = Big_N * Big_Q / (2 * greekpi * (Big_R + Delta_R + Small_l) * Big_L)

    return sigma_s

def Get_n_0(ltf, results):
    h_bar2 = np.power(h_bar,2.0)
    Epsilon_r = Epsilon_0 * float(results['Epsilon_1'])
    pi4_3 = np.power(greekpi,4.0/3.0)
    e2 = np.power(elem_charge,2.0)
    ltf = ltf * 1e-9 # from nm to m
    ltf2 = np.power(ltf, 2.0)
    ms_value = float(results['ms']) * el_mass
    ch_dens = np.power((h_bar2 * Epsilon_r * pi4_3)/(ms_value * e2 * ltf2),3.0)
    return ch_dens

def make_data(results):
    
    # write the data file
    
    data  = '#######################################################\n'
    data += '#                                                     #\n'
    data += '#              BioFET-SIM version 1.0                 #\n'
    data += '#   Luca De Vico, University of Copenhagen, Denmark   #\n'
    data += '#                                                     #\n'
    data += '#             ' + time.asctime() +   '                #\n'
    data += '#                                                     #\n'
    data += '#######################################################\n'
    data += '#                                                     #\n'
    data += '#       Please cite the usage of this program as      #\n'
    data += '#                                                     #\n'
    data += '# De Vico, L.; Sorensen, M. H.; Iversen, L.; Rogers,  #\n'
    data += '# D. M.; Sorensen, B. S.; Brandbyge, M.; Nygard, J.;  #\n'
    data += '# Martinez, K. L.; Jensen, J. H.                      #\n'
    data += '#                                                     #\n'
    data += '# Quantifying signal changes in nano-wire based       #\n'
    data += '# biosensors.                                         #\n'
    data += '#                                                     #\n'
    data += '# Nanoscale, 2011, 3, 706-717 DOI:10.1039/C0NR00442A  #\n'
    data += '#                                                     #\n'
    data += '#######################################################\n'
    
    # the data used for the simulation

    data += '#\n'
    data += '# Simulation data:\n'
    data += '#\n'
    data += '# Nano-wire length = %.2f nm\n' %results['Big_L']
    data += '# Nano-wire radius = %.2f nm\n' %results['Big_R']    
    data += '# Nano-wire Thomas-Fermi length = %.2f nm\n' %results['Lambda_tf']
    data += '# Nano-wire permittivity = %.2f E_0\n' %results['Epsilon_1']
    data += '# Nano-wire charge carrier mobility mu = %.3f m^2 V^-1 s^-1\n' %results['mu']
    data += '# Nano-wire type: ' + results['np_type'] + '\n'
    data += '# Nano-wire charge carrier density n/p_0 = %.2e m^-3\n' %results['n_0']
    data += '# Oxide layer thickness = %.2f nm\n' %results['Delta_R']
    data += '# Oxide layer permittivity = %.2f E_0\n' %results['Epsilon_2']
    data += '# Solvent Debye length = %.2f nm\n' %results['Lambda_d']
    data += '# Solvent permittivity = %.2f E_0\n' %results['Epsilon_3']
    data += '# Number of charges on the nano-wire surface = %.0f\n' %results['Small_N']  
    data += '# Charge of charges on the nano-wire surface = %.2f elementary charges\n' %results['Small_Q']
    data += '# Distance of the charges in the solvent buffer = %.2f nm\n' %results['Small_l']
    data += '# Number of charges in the solvent buffer = %.0f\n' %results['Big_N']
    data += '# Charge of charges in the solvent buffer = %.2f elementary charges\n' %results['Big_Q']    
    
    # results. first for the single data set ...

    data += '#\n'
    data += '# Simulation results:\n'
    data += '#\n'
    data += '# Base Conductance = %.3f nano Siemens\n' %(results['G0'] * 1e9)
    data += '# Conductance Sensitivity = %.3f\n' %results['DG_G0']
    data += '# Conductance Change = %.3f nano Siemens\n' %(results['DG'] * 1e9)
    data += '# Conductance = %.3f nano Siemens\n' %(results['G'] * 1e9)
    
    data += '#\n'
    data += '# Simulation results for values (x) of the \n'

    if   (results['WhichX'] == 'Big_L'    ):
        data += '# nano-wire length\n'
    elif (results['WhichX'] == 'Big_R'    ):
        data += '# nano-wire radius\n'
    elif (results['WhichX'] == 'Delta_R'  ):
        data += '# oxide layer thickness\n'
    elif (results['WhichX'] == 'Small_l'  ):
        data += '# distance of the charges in the solvent buffer\n'
    elif (results['WhichX'] == 'Lambda_d' ):
        data += '# solvent Debye length\n'
    elif (results['WhichX'] == 'Lambda_tf'):
        data += '# nano-wire Thomas-Fermi length\n'
    elif (results['WhichX'] == 'Epsilon_1'):
        data += '# nano-wire permittivity\n'
    elif (results['WhichX'] == 'Epsilon_2'):
        data += '# oxide layer permittivity\n'
    elif (results['WhichX'] == 'Epsilon_3'):
        data += '# solvent permittivity\n'
    elif (results['WhichX'] == 'Small_N'  ):
        data += '# number of charges on the nano-wire surface\n'
    elif (results['WhichX'] == 'Small_Q'  ):
        data += '# charge of charges on the nano-wire surface\n'
    elif (results['WhichX'] == 'Big_N'    ):
        data += '# number of charges in the solvent buffer \n'
    elif (results['WhichX'] == 'Big_Q'    ):
        data += '# charge of charges in the solvent buffer \n'

    data += '# in the range %.4f - %.4f\n' %(results['bottom'], results['top'])
    data += '# of the Conductance Sensitivity y = DG/G_0\n'
    
    data += '#\n'
    data += '#     x           y\n'

    for i in np.arange(0,101):
        data += '%.6f      %.6f\n' %(results['eX'][i], results['whY'][i])
    
    dataname = results['ID']
    
    data_file_name = '%s.data'%dataname
    data_file = open(data_file_name, 'w')
    data_file.write(data)
    data_file.close()
    
def make_graph(results):
    
    #make the graph
    
    graphname = results['ID']
    
    # make plot script
    script = """
set term postscript eps enhanced color "Times-Roman" 22
set style line 1 lt 1 lw 6 pt 7 ps 1
set nokey
set border 15 lw 2
set xlabel \"%s\"
set ylabel \"{/Symbol D}G/G_0\"

set out \"/var/www/propka/biofet-sim/v0.1/output/%s.eps\"

plot \"/var/www/propka/biofet-sim/v0.1/output/%s.data\" u 1:2 w p ls 1
    """%(results['xlabel'], graphname, graphname)
    
    # print the gnuplot script
    
    script_file_name = '%s.gp'%graphname
    script_file = open(script_file_name,'w')
    script_file.write(script)
    script_file.close()
    
    # execute gnuplot and convert the eps to png
    
    os.system('/usr/bin/gnuplot /var/www/propka/biofet-sim/v0.1/output/%s'%script_file_name)
    os.system('/usr/bin/convert -resample 200x200 -density 200x200 /var/www/propka/biofet-sim/v0.1/output/%s.eps /var/www/propka/biofet-sim/v0.1/output/%s.png'%(graphname,graphname))
    
def make_page(results):
    # make html page
    html =  '<h2>BIOFET-SIM results <img src="favicon.png" alt="BioFET-SIM" height="100"/> </h2>\n'
    html += '<br><br>\n'
    html += '<b>&Delta;G/G<sub>0</sub> = %s</b><br><br>\n'%results['DG_G0']
    html += '<b>G<sub>0</sub> = %s nano Siemens</b><br><br>\n'%(results['G0']*1e9)
    html += '<b>&Delta;G = %s nano Siemens</b><br><br>\n'%(results['DG']*1e9)
    html += '<b>G = %s nano Siemens</b><br><br>\n'%(results['G']*1e9)
    html += '<b><img src="http://propka.ki.ku.dk/biofet-sim/v0.1/output/%s.png" alt="Results" height="300"/> </b>\n'%results['ID']
    html += '<br><br>\n'
    html += '<b><a href="http://propka.ki.ku.dk/biofet-sim/v0.1/output/%s.data">Output data file.</a></b><br><br>\n'%results['ID']
    html += '<br><br>\n'
    # put it all together
    out = """
<html>
<head>
<link rel="stylesheet" href="http://propka.ki.ku.dk/biofet-sim/v0.1/baker.css" type=\"text/css\">
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon" />
<title>BIOFET-SIM 1.0 Results</title>
</head>
<body>

%s

</body>
</html>
    """%(html)
    
    return out

go(form)
