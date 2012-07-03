#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()
form = cgi.FieldStorage()

print "Content-Type: text/html\n\n"

def go(form):
    results = get_results(form)
    page = make_page(results)
    print page
    return

def get_results(form):
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

<body>

<script LANGUAGE="JavaScript" type="text/javascript">
var ie4 = false;
if(document.all) {
  ie4 = true; 
}

function IDObject(id) {
	if (ie4) {
		return document.all[id]; 
	} else {
		return document.getElementById(id); 
	}
}

function showhide(divId) { 
	var d = IDObject(divId);
	var Stat = d.style.display; 
	if (Stat == 'none') { 
		d.style.display = 'block'; 
	}else{ 
		d.style.display = 'none';
	}
}


function setprotopt(){

if(document.thisform.WATOPT.checked==true)
{
document.thisform.HOPT.checked=true;
}
}

function setwatopt(){

if(document.thisform.HOPT.checked==false)
{
document.thisform.WATOPT.checked=false;
}
}

function xrange(val) {

if(val == "Fixed")
{
document.thisform.XMin.disabled=true;
document.thisform.XMax.disabled=true;
document.thisform.FIXED.disabled=false;
}
else if(val == "MinMax")
{
document.thisform.XMin.disabled=false;
document.thisform.XMax.disabled=false;
document.thisform.FIXED.disabled=true;
}
}

function OnSubmitForm()
{
	if(document.pressed == 'Link')
	{
		document.thisform.action ="lambda_TF_np_0.cgi";
	}
	else
	if(document.pressed == 'Compute')
	{
		document.thisform.action ="biofet-sim-1.0.cgi";
	}
	return true;
}

</script>

<h2>The BIOFET-SIM Web Interface 1.0 <img src="favicon.png" alt="BioFET-SIM" height="100"> </h2>
<p>Created by <a href="http://propka.ki.ku.dk/~luca/">Luca De Vico</a></p>

<FORM onSubmit="return OnSubmitForm();" METHOD="POST" ENCTYPE="multipart/form-data" name="thisform" action="">

<p>Follow this <input type="submit" value="Link" onClick="document.pressed=this.value">
 for help on the relationship between Thomas-Fermi length, effective charge carrier mass, and charge carrier density.</p>

<p>This web interface presents only a simplified version of BioFET-SIM.
Please check the <a href='http://propka.ki.ku.dk/~luca/biofet-sim'>
help page</a> for more information and to download the
interactive program.</p>

<p>BioFET-SIM is now also available as a free App on the App Store! 
<a href='http://itunes.apple.com/us/app/biofet-sim/id432519041?mt=8&ls=1' target="_blank">
<img src="App_Store_Badge.png" alt="BioFET-SIM Available on the App Store" height="50">
</a></p>

<blockquote>

<table style="width:800; border-top:solid 1px; border-bottom:solid 1px;">

<tr>
  <th colspan="3">Please enter or accept values</th>
  <th>Graph x</th>
  <th rowspan="10"><img src="system-1.0.png" alt="BioFET-SIM" height="200"></th>
</tr>

<!-- Nano wire properties -->
<tr>
  <td colspan="4" style="border-bottom:dashed 1px; height:35; vertical-align:bottom" align="center">Nano-wire properties</td>
</tr>

<tr>
  <td align="right">Nano-wire length (L): </td>
  <td><input type="text" name="Big_L" size=10 value="%.1f"></td>
  <td> nm</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Big_L">
</tr>

<tr>
  <td align="right">Nano-wire radius (R): </td>
  <td><input type="text" name="Big_R" size=10 value="%.1f"></td>
  <td> nm</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Big_R">
</tr>

<tr>
  <td align="right">Thomas-Fermi length (&lambda;<sub>TF</sub>): </td>
  <td><input type="text" name="Lambda_tf" size=10 value="%.1f"></td>
  <td> nm</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Lambda_tf">
</tr>

<tr>
  <td align="right">Nano-wire permittivity (&epsilon;<sub>1</sub>): </td>
  <td><input type="text" name="Epsilon_1" size=10 value="%.1f"></td>
  <td> &epsilon<sub>0</sub></td>
  <td align="center"><input type="RADIO" name="GraphX" value="Epsilon_1">
</tr>

<tr>
  <td align="right">Charge carrier mobility (&mu;): </td>
  <td><input type="text" name="mu" size=10 value="%.2f"></td>
  <td> m<sup>2</sup>V<sup>-1</sup>s<sup>-1</sup></td>
  <!--<td align="center"><input type="RADIO" name="GraphX" value="mu">-->
</tr>

<tr>
  <td align="right">Charge carrier density (n<sub>0</sub>/p<sub>0</sub>): </td>
  <td><input type="text" name="n_0" size=10 value="%.2e"></td>
  <td> m<sup>-3</sup></td>
  <!--<td align="center"><input type="RADIO" name="GraphX" value="n_0">-->
</tr>

<tr>
  <td align="right">Effective charge carrier mass m*: </td>
  <td><input type="text" name="ms" size=10 value="%.2f" READONLY></td>
</tr>

<tr>
  <td align="right">n-type </td>
  <td align="left"><input type="RADIO" name="TYPE" value="n" CHECKED>
</tr>

<tr>
  <td align="right">p-type </td>
  <td align="left"><input type="RADIO" name="TYPE" value="p">
</tr>

<!-- Oxide layer properties -->
<tr>
  <td colspan="4" style="border-bottom:dashed 1px; height:35; vertical-align:bottom" align="center">Oxide layer properties</td>
  <td rowspan="10"><img src="system-1.0.png" alt="BioFET-SIM" height="200"></td>
</tr>

<tr>
  <td align="right">Oxide layer thickness (&Delta;R): </td>
  <td><input type="text" name="Delta_R" size=10 value="%.1f"></td>
  <td> nm</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Delta_R">
</tr>

<tr>
  <td align="right">Oxide layer permittivity (&epsilon;<sub>2</sub>): </td>
  <td><input type="text" name="Epsilon_2" size=10 value="%.1f"></td>
  <td> &epsilon<sub>0</sub></td>
  <td align="center"><input type="RADIO" name="GraphX" value="Epsilon_2">
</tr>

<!-- Solvent properties -->
<tr>
  <td colspan="4" style="border-bottom:dashed 1px; height:35; vertical-align:bottom" align="center">Solvent properties</td>
</tr>

<tr>
  <td align="right">Solvent Debye length (&lambda;<sub>d</sub>): </td>
  <td><input type="text" name="Lambda_d" size=10 value="%.1f"></td>
  <td> nm</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Lambda_d" CHECKED>
</tr>

<tr>
  <td align="right">Solvent permittivity (&epsilon;<sub>3</sub>): </td>
  <td><input type="text" name="Epsilon_3" size=10 value="%.1f"></td>
  <td> &epsilon<sub>0</sub></td>
  <td align="center"><input type="RADIO" name="GraphX" value="Epsilon_3">
</tr>

<!-- charges on the wire -->
<tr>
  <td colspan="4" style="border-bottom:dashed 1px; height:35; vertical-align:bottom" align="center">Charges residing directly on the nano-wire (q)</td>
</tr>

<tr>
  <td align="right">Number of charges: </td>
  <td><input type="text" name="Small_N" size=10 value="%.0f"></td>
  <td></td>
  <td align="center"><input type="RADIO" name="GraphX" value="Small_N">
</tr>

<tr>
  <td align="right">Charge: </td>
  <td><input type="text" name="Small_Q" size=10 value="%.1f"></td>
  <td> Unitary charges</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Small_Q">
</tr>

<!-- charges immersed in the solvent -->
<tr>
  <td colspan="4" style="border-bottom:dashed 1px; height:35; vertical-align:bottom" align="center">Charges immersed in the solvent (Q)</td>
</tr>

<tr>
  <td align="right">Charges - Surface distance (l): </td>
  <td><input type="text" name="Small_l" size=10 value="%.1f"></td>
  <td> nm</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Small_l">
</tr>

<tr>
  <td align="right">Number of charges: </td>
  <td><input type="text" name="Big_N" size=10 value="%.0f"></td>
  <td></td>
  <td align="center"><input type="RADIO" name="GraphX" value="Big_N">
</tr>

<tr>
  <td align="right">Charge: </td>
  <td><input type="text" name="Big_Q" size=10 value="%.1f"></td>
  <td> Unitary charges</td>
  <td align="center"><input type="RADIO" name="GraphX" value="Big_Q">
</tr>

<!-- graph x -->
<tr>
  <td colspan="4" style="border-bottom:dashed 1px; height:35; vertical-align:bottom" align="center">Graph x range</td>
</tr>

<tr>
  <td align="left">Fixed +/- </td>
  <td><input type="text" name="FIXED" size=3 value="20">%%</td>
  <td align="left"><input type="RADIO" name="RANGE" value="Fixed" onClick="xrange(this.value)" CHECKED>
</tr>

<tr>
  <td align="left">Min - Max </td>
  <td><input type="text" name="XMin" size=4 value="0.01" DISABLED>-<input type="text" name="XMax" size=4 value="10.0" DISABLED></td>
  <td align="left"><input type="RADIO" name="RANGE" value="MinMax" onClick="xrange(this.value)">
</tr>

<tr>
  <td colspan="4" align="center" style="border-top:dashed 2px; height:50; vertical-align:bottom">
<!--    <table>
      <tr>
        <td>-->
	<input type="submit" value="Compute" onClick="document.pressed=this.value">
<!--	</td>
       <td><input type="reset" value="Clear Form"></td>
      </tr>
    </table> -->
  </td>
</tr>

</table>

</blockquote>

</form>

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

<p align=center><font size="-1"><I>Last Updated April 26th, 2011</I></font>

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


</body>
</html>
    """%(results['Big_L'], results['Big_R'], results['Lambda_tf'], results['Epsilon_1'], results['mu'], results['n_0'], results['ms'], results['Delta_R'], results['Epsilon_2'], results['Lambda_d'], results['Epsilon_3'], results['Small_N'], results['Small_Q'], results['Small_l'], results['Big_N'], results['Big_Q'])

    return out

go(form)
