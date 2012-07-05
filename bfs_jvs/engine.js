$(document).ready(function()
{ 
    var res_base_path = './bfs_res/';
    var cgi_base_path = './bfs_cgi/';
    var pdb_base_path = './bfs_pdb/';
    var ajax_loader   = "<img src='./bfs_jvs/ajax-loader.gif' alt='Loading...'>";

    // Check HTTP response.
    function cr(resp)
    {
        if (typeof resp === "undefined")
        {
            $('#loader').css({"visibility":"hidden"});
            $('#status').html("Ready.");
            console.log("Response done.");
        } else {
            console.log(resp);
            /*
            Consider: using a JSON parse, separate parts of data are returned.
            var back = jQuery.parseJSON(resp);
            console.log(back[0]);
            */
            $('#loader').css({"visibility":"hidden"});
            //$('#status').html("Ready.");
            console.log("Response done.");
        }
    } 

    // Status update.
    function status_update(step) 
    {
        $('#loader').css({"visibility":"visible"});
        $('#status').html(step);
        console.log("Started: " + step);
    } 

    /* ------------------------------------------------------- */
    /* Response.                                               */
    /* ------------------------------------------------------- */
    function clickResp()
    {
        function plot_resp(resp)
        {
            var base_conductance = resp.split(';')[0].split('=')[1];
            var sensitivity = resp.split(';')[1].split('=')[1];
            $('#sensitivity').html('Sensitivity: ' + sensitivity);
            $('#base_conductance').html('Base conductance G<sub>0</sub>: ' + base_conductance);
            var d = new Date();
            if(action == 'BioFET-SIM')
            {
                $("#resPlot").attr("src", res_base_path + target + "-reo.png?" + d.getTime());
            } else {
                $("#resPlot").attr("src", res_base_path + target + "-pH-reo.png?" + d.getTime());
            } 
            // Clear loader.
            cr();
        }

        // Jmol selectors
        //'atomInfo' does not provide charges, they are added to input on server side.
        var target   = $('#target').val();
        var atomInfo = jmolGetPropertyAsArray("atomInfo", "2.1"); 
        var form_bfs = $('#form_bfs').serialize();
        var pdb      = '';
        for(var i=0; i<atomInfo.length; i++)
        {
            // Prevent empty last line.
            if(i<atomInfo.length-1)
            {
                pdb += atomInfo[i].x + ' ' + atomInfo[i].y + ' ' + atomInfo[i].z + '\n';
            } else {
                pdb += atomInfo[i].x + ' ' + atomInfo[i].y + ' ' + atomInfo[i].z;
            }
        }

        // Get clicked button id and build up form, CGI.
        var action = $(this).val()
        form_bfs += '&tmp_pdb=' + pdb; 
        form_bfs += '&action=' + action;
        form_bfs += '&pH=' + $('#pH').val();
        form_bfs += '&fileName=' + target + ".bfs";
        form_bfs += '&targetLab=' + target;

        //BFS Input comment section, visual.
        //$('#fileName').val(target+".bfs");
        $('#bfsInput').attr('href', res_base_path + target + ".bfs"); 
        var comment  = "# BioFET-SIM Calculation\n"
            //comment += "# Date of calculation:\n"
            comment += "# Calculation target: " + target + "\n"
            comment += "# pH: " + $('#pH').val() + "\n"
            comment += "# Description: "
        $('#comment').html(comment); 

        // Calculation.
        status_update("Calculation...");
        $.post(cgi_base_path + 'bio_run.cgi', form_bfs, plot_resp);

        // Download data files.
        $('#bfs_response').attr('href', res_base_path + target + "-reo.dat");
        $('#pH_response').attr('href', res_base_path + target + "-pH-reo.dat"); 
    } 

    // Click event handlers.
    $('#bfs_signal').click(clickResp);
    $('#pHresp').click(clickResp);
}); // End ready
