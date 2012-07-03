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
# print form
#        -->     FieldStorage(None, None, [FieldStorage('ms', None, '0.98'), FieldStorage('Epsilon_1', None, '12.0'), FieldStorage('type', None, 'direct'), FieldStorage('Lambda_tf', None, '1.0'), FieldStorage('type', None, 'inverse'), FieldStorage('n_0', None, '1.34e+25')]) 
# if empty
#                FieldStorage(None, None, [])

def go(form):
    os.chdir('/var/www/propka/biofet-sim/v0.1/output')
    results = compute_results(form)
    page = make_page(results)
    print page
    return

def compute_results(form):
    results = {}
    if len(form) == 0:
      # first instance
      # default values
      
      results['Big_L']	   = 2000.0
      results['Big_R']	   = 10.0
      results['Delta_R']   = 2.0   
      results['Small_l']   = 2.0
      results['Lambda_d']  = 2.0
      results['Lambda_tf'] = 2.0
      results['Epsilon_1'] = 12.0
      results['Epsilon_2'] = 3.9
      results['Epsilon_3'] = 78.0
      results['Small_N']   = 10000
      results['Small_Q']   = 1.0
      results['Big_N']	   = 5000
      results['Big_Q']	   = 3.0
      results['n_0']	   = 2.09e+23
      results['mu']	   = 0.01
      results['np_type']   = "n"
      results['ms']        = 0.98
      results['TYPE']      = results['np_type']
      
    else:
      # get the values

      results['Big_L']	   = float(form['Big_L'	 ].value)     
      results['Big_R']	   = float(form['Big_R'	 ].value)     
      results['Delta_R']   = float(form['Delta_R'  ].value)   
      results['Small_l']   = float(form['Small_l'  ].value)   
      results['Lambda_d']  = float(form['Lambda_d' ].value)  
      results['Lambda_tf'] = float(form['Lambda_tf'].value) 
      results['Epsilon_1'] = float(form['Epsilon_1'].value) 
      results['Epsilon_2'] = float(form['Epsilon_2'].value) 
      results['Epsilon_3'] = float(form['Epsilon_3'].value) 
      results['Small_N']   = float(form['Small_N'  ].value)   
      results['Small_Q']   = float(form['Small_Q'  ].value)   
      results['Big_N']	   = float(form['Big_N'	 ].value)     
      results['Big_Q']	   = float(form['Big_Q'	 ].value)     
      results['n_0']	   = float(form['n_0'	 ].value)
      results['mu']	   = float(form['mu'	 ].value) 
      results['np_type']   = form['TYPE'].value
      results['ms']        = float(form['ms'	 ].value)
      results['TYPE']        = form['TYPE'].value

    # compute the results

    h_bar2 = np.power(h_bar,2.0)
    Epsilon_r = Epsilon_0 * results['Epsilon_1']
    pi4_3 = np.power(greekpi,4.0/3.0)
    e2 = np.power(elem_charge,2.0)
    ms_value = results['ms'] * el_mass

    if form.has_key('whattodo'):
      if form['whattodo'].value == 'into ->':
	# from ltf to np0

	ltf = results['Lambda_tf'] * 1e-9 # from nm to m
	ltf2 = np.power(ltf, 2.0)
	results['n_0'] = np.power((h_bar2 * Epsilon_r * pi4_3)/(ms_value * e2 * ltf2),3.0)

      if form['whattodo'].value == '<- into':
	# from np0 to ltf

	np01_3 = np.power(results['n_0'], 1.0/3.0)
	ltf = np.sqrt((h_bar2 * Epsilon_r * pi4_3)/(ms_value * e2 * np01_3))
	results['Lambda_tf'] = ltf * 1e9 # from m to nm

    return results
        
def make_page(results):
    out = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head> 
<title>BIOFET-SIM 1.0</title>

<link rel="stylesheet" href="./baker.css" type="text/css">
<link rel="shortcut icon" href="favicon.png" type="image/png">
<meta name="Keywords" content="BIOFET-SIM, biofet, nano-wire, nano wire, nanowire, Thomas-Fermi, Debye length, propka, simulation, nanobiofet, Jan Jensen, Luca De Vico">
<meta name="Description" content="Free, BIOFET-SIM, biofet, nano-wire, nano wire, nanowire, Thomas-Fermi, Debye length, propka, simulation, nanobiofet, Jan Jensen, Luca De Vico">
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">

</head>

<BODY>

<script LANGUAGE="JavaScript" type="text/javascript">

function OnSubmitForm()
{
	if(document.pressed == 'BIOFET-SIM Web Interface')
	{
		document.thisform.action ="biofet-sim-1.0-interface.cgi";
	}
	else
	{
		document.thisform.action ="lambda_TF_np_0.cgi";
	}
	return true;
}

</script>


<h2>The BIOFET-SIM Web Interface 1.0 <img src="favicon.png" alt="BioFET-SIM" height="100"> </h2>

<p>Created by <a href="http://propka.ki.ku.dk/~luca/">Luca De Vico</a></p>

<p>The relationship between Thomas-Fermi length (&lambda;<sub>TF</sub>) and charge carrier density 
(p<sub>0</sub> in case of p-type semiconductor) is regulated by:</p>

<img src="l_TF.png" alt="lambda_TF equation" height="100">

<p>where &#8463; is the reduced Planck's constant, &epsilon;<sub>r</sub> = 
&epsilon;<sub>0</sub>&epsilon;<sub>1</sub>, m<sup>*</sup> is the effective charge carrier mass, and e the
elementary charge. In case of a n-type semiconductor one uses n<sub>0</sub>. The effective mass of the 
charge carrier (hole or electron) is commonly expressed as a fraction of the mass of an electron at rest.
Typical values of m<sup>*</sup> are reported in Table 1.</p>

<hr>

<FORM onSubmit="return OnSubmitForm();" METHOD="POST" ENCTYPE="multipart/form-data" name="thisform">

<blockquote>

<table style="width:300pt;">

<tr>
  <td>Effective charge carrier mass m<sup>*</sup>:</td>
  <td><input type="text" name="ms" size=4 value="%.3f"></td>
</tr>

<tr>
  <td>Semiconductor permittivity &epsilon;<sub>1</sub>:</td>
  <td><input type="text" name="Epsilon_1" size=4 value="%.1f"></td>
</tr>

</table>

<br><br>

<table style="width:400pt;">

<tr>
  <td align="center">Thomas-Fermi length</td>
  <td><input type="submit" name="whattodo" value="into ->" onClick="document.pressed=this.value"></td>
  <td align="center">Charge carrier density</td>
</tr>

<tr>
  <td align="center"><input type="text" name="Lambda_tf" size=4 value="%.2f"> nm</td>
  <td><input type="submit" name="whattodo" value="<- into" onClick="document.pressed=this.value"></td>
  <td align="center"><input type="text" name="n_0" size=7 value="%.2e"> m<sup>-3</sup></td>
</tr>

</table>

<input type="hidden" name="Big_L" size=10 value="%.1f">
<input type="hidden" name="Big_R" size=10 value="%.1f">
<input type="hidden" name="mu" size=10 value="%.2f">
<input type="hidden" name="Delta_R" size=10 value="%.1f">
<input type="hidden" name="Epsilon_2" size=10 value="%.1f">
<input type="hidden" name="Lambda_d" size=10 value="%.1f">
<input type="hidden" name="Epsilon_3" size=10 value="%.1f">
<input type="hidden" name="Small_N" size=10 value="%.0f">
<input type="hidden" name="Small_Q" size=10 value="%.1f">
<input type="hidden" name="Small_l" size=10 value="%.1f">
<input type="hidden" name="Big_N" size=10 value="%.0f">
<input type="hidden" name="Big_Q" size=10 value="%.1f">
<input type="hidden" name="TYPE"  value="%.s">


</blockquote>

<hr>
<p>Export these values to the <input type="submit" value="BIOFET-SIM Web Interface" onClick="document.pressed=this.value"></p>

</form>

<table style="width:300pt; border-top:solid 1px; border-bottom:solid 1px;">
<caption> Table 1: typical values of m<sup>*</sup> as fraction of the mass of an electron at rest.</caption>

<tr>
  <th>Semiconductor type</th>
  <th>m<sup>*</sup></th>
  <th>&epsilon;<sub>1</sub></th>
  <th>Ref.</th>
</tr>

<tr>
  <td>Silicon n-type</td>
  <td>0.98</td>
  <td>12.0</td>
  <td>(1)</td>
</tr>

<tr>
  <td>Silicon p-type</td>
  <td>0.54</td>
  <td>12.0</td>
  <td>(1)</td>
</tr>

<tr>
  <td>Indium oxide intrinsic n-type</td>
  <td>0.35</td>
  <td>9.0</td>
  <td>(2)</td>
</tr>

<tr>
  <td>Indium Arsenide in inversion layer n-type</td>
  <td>0.026</td>
  <td>20.0</td>
  <td>(1)</td>
</tr>

<tr>
  <td colspan="3" style="border-top:dashed 1px">(1) Yacobi, B. G. Semiconductors Materials An Introduction to Basic Principles; Microdevices; Kluver Academic Publisher, New York, 2003; p 54</td>
</tr>
<tr>
  <td colspan="3">(2) Kostlin, H.; Jost, R.; Lems, W. Phys. Status Solidi A 1975, 29, 87-93</td>
</tr>

</table>

<BR>

<p>(Please report errors to "luca _at_  chem.ku.dk".) </p>

<P CLASS="western" ALIGN=CENTER STYLE="margin-bottom: 0in; widows: 0; orphans: 0">
The BioFET method is developed by the<br>
<font COLOR="#0000ff"><U><A HREF="http://propka.ki.ku.dk/~jhjensen">Jensen
Research Group</A></U></font><br>
Department of Chemistry<br>

University of Copenhagen</P>

<p>Please cite these references in publications:
<p> De Vico, L.; S&oslash;rensen, M. H.; Iversen, L.; Rogers, D. M.; S&oslash;rensen, B. S.; Brandbyge, M.; Nyg&aring;rd, J.; Martinez, K. L.; Jensen, J. H. &quot;<a href="http://dx.doi.org/10.1039/C0NR00442A">Quantifying signal changes in nano-wire based biosensors</a>&quot; <I>Nanoscale</I>, 2011, 3, 706-717, DOI:10.1039/C0NR00442A.

<p>Reprints can be obtained by contacting <font COLOR="#0000ff"><U><A HREF="mailto:jhjensen@chem.ku.dk">Jan
Jensen</A></U></font>.</P>

<hr>

<p align=center><font size="-1"><I>Last Updated March 8th, 2011</I></font>

  <a href="http://validator.w3.org/check?uri=referer"><img
      src="http://www.w3.org/Icons/valid-html401"
      alt="Valid HTML 4.01 Transitional" height="31" width="88"></a>

  <a href="http://jigsaw.w3.org/css-validator/check/referer">
      <img style="border:0;width:88px;height:31px"
          src="http://jigsaw.w3.org/css-validator/images/vcss"
          alt="Valid CSS!">
  </a>

<!-- Site Meter -->
<script type="text/javascript" src="http://s47.sitemeter.com/js/counter.js?site=s47biofet-sim">
</script>
<noscript>
<a href="http://s47.sitemeter.com/stats.asp?site=s47biofet-sim" target="_top">
<img src="http://s47.sitemeter.com/meter.asp?site=s47biofet-sim" alt="Site Meter" border="0"></a>
</noscript>
<!-- Copyright (c)2009 Site Meter -->


</BODY>
</HTML>

    """%(results['ms'], results['Epsilon_1'], results['Lambda_tf'], results['n_0'], results['Big_L'], results['Big_R'], results['mu'], results['Delta_R'], results['Epsilon_2'], results['Lambda_d'], results['Epsilon_3'], results['Small_N'], results['Small_Q'], results['Small_l'], results['Big_N'], results['Big_Q'], results['TYPE'])
    
    return out

go(form)
