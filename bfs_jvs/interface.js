$('document').ready(function()
{
    $('#btn').click(function()
    {
        if($('#images').val() == '' || $('#images').val().split('.')[1] != 'pdb')
        {
            alert("Please provide a PDB file for upload.");
        } else {
            $('#uploadform').attr('action', 'upload.php');
        }
    }); // end upload click
}); // end ready

/* Fade out lower and upper limit text input of out of focus fields. */
/* Formatting stuff. */
function xLabel(n) {
    var lbls = document.getElementsByName("abs");
    for(var i=0; i<lbls.length; i++) {
        //alert(n);
        //alert(lbls[i].value + " " + n);
        if(lbls[i].value == n) {
            //alert(lbls[i] + " " + lbls[i].value);
            var tmpMinLbl = lbls[i].value+"_x_min"; 
            var tmpMaxLbl = lbls[i].value+"_x_max"; 
            document.getElementById(tmpMinLbl).disabled=false;
            document.getElementById(tmpMaxLbl).disabled=false;
            //continue;
        } else {
            var tmpMinLbl = lbls[i].value+"_x_min"; 
            var tmpMaxLbl = lbls[i].value+"_x_max"; 
            //alert(tmpMinLbl);
            //alert(tmpMaxLbl);
            document.getElementById(tmpMinLbl).disabled=true;
            document.getElementById(tmpMaxLbl).disabled=true;
        }
    }
} 

function fadeBox(c) {
    if(document.getElementById("overwrite").checked == false) {
        document.getElementById("num_prot").disabled=false;
    } else {
        document.getElementById("num_prot").disabled=true;
    }
}

$(document).ready(function()
{
    $('#uploaded').click(function()
    {
        var thisCheck = $(this);
        if (thisCheck.is(':checked'))
        {
            $('#overwriteLab').attr('style', 'visibility:visible');
            $('#overwriteLabExpl').attr('style', 'visibility:visible');
            $('#overwrite').attr('style', 'visibility:visible');
        } else {
            $('#overwrite').attr('checked', false);
            $('#overwriteLab').attr('style', 'visibility:hidden');
            $('#overwriteLabExpl').attr('style', 'visibility:hidden');
            $('#overwrite').attr('style', 'visibility:hidden');
        } 
    }); // end click
}); // end ready

/* Get coordinates of rotated charge distribution. */
/* Compute stuff. */
/* Out of use.
function onClickWrite() {
    jmolScript('select 1.1');
    document.getElementById("av_RQ").value = jmolEvaluate('write("PDB")');
    return true;
} 

// Writes atom coordinates on move.
function writeToId(applet, atms) {
    jmolScript("select 1.1 or 2.1");
    document.getElementById("writeHere").value = jmolEvaluate('write("PDB")');
}

function showCoordinates(applet, atms) {
    jmolScript("select 1.1");
    document.getElementById("writeHere").value =jmolEvaluate('write("PDB")');
}
*/ 
