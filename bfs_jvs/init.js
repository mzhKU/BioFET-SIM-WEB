// Assigning event handlers to initialization of interface.
$('document').ready(function()
{
    $('#setup').submit(function()
    {
        // Assemble BFS initialization form data, CGI directory base path
        // and Ajax loader HTML substitute.
        var formData      = $(this).serialize(); 
        var target        = $('#target').val();
        var pH            = $('#pH').val();
        var cgi_base_path = './bfs_cgi/';
        var pdb_base_path = './bfs_pdb/';
        var res_base_path = './bfs_res/';
        var ajax_loader   = "<img src='./bfs_jvs/ajax-loader.gif' alt='Loading...'>";
        var pHPad;

        // Fill in target name and pH. Q_tot only after PROPKA job finished.
        $('#targetLab').html("Structure: " + target);
        $('#targetLabHid').attr('value', target);
        $('#QLab').html("Q<sub>tot</sub>at pH " + pH + ": 0.0");
        $('#fileName').attr('value', target+".bfs");
        $('#bfsInput').attr('href', pdb_base_path + target + ".bfs");

        //BFS Input comment section.
        var comment  = "# BioFET-SIM Calculation\n"
            //comment += "# Date of calculation:\n"
            comment += "# Calculation target: " + target + "\n"
            comment += "# pH: " + pH + "\n"
            comment += "# Description: "
        $('#comment').html(comment);

        // Initialize BFS interface.
        status_update('Downloading...');
        $.get(cgi_base_path + 'bio_dwn.cgi', formData, rechain);
        $("#resPlot").attr("src", res_base_path + "result_default.png");
        console.log("Download request sent, waiting for response...");

        function def()
        {
            $.get(cgi_base_path + 'bio_def.cgi', formData, cr);
        }

        function rechain()
        { 
            status_update('Rechaining...');
            $.get(cgi_base_path + 'bio_rec.cgi', formData, fix);
            console.log("Rechain request sent, waiting for response...");
        } 

        function fix()
        {
            status_update('Fixing...');
            $.get(cgi_base_path + 'bio_fix.cgi', formData, reo);
            console.log("PDB fix request sent, waiting for response...");
        }

        function reo()
        {
            status_update('Reorienting...');
            $.get(cgi_base_path + 'bio_reo.cgi', formData, pka);
            console.log("Reorientation request sent, waiting for response...");
        }

        function pka()
        {
            status_update('pKa calculation...');
            $.get(cgi_base_path + 'bio_pka.cgi', formData, rho);
            console.log("pKa calculation request sent, waiting for response...");
        } 

        function rho(resp)
        { 
            status_update('Charge distribution...');
            pHPad = resp.split('=')[1];
            $.get(cgi_base_path + 'bio_rho.cgi', formData, build_interface);
            console.log("Charge distribution calculation request sent, waiting for response...");
        } 

        function build_interface(resp)
        {
            /* 
               Handling of Q_tot coming from bio_rho.cgi.
               Json does not work right now, probably problem on
               CGI side:
               var q_tot = jQuery.parseJSON(resp);
            */ 
            // Q_tot evaluation.
            var q_tot = resp.split(';')[0].split('=')[1];
            $('#QLab').html("Q<sub>tot</sub>at pH " + pH + ": " + q_tot);

            // Charge distribution evaluation.
            //var pqr = resp.split(';')[1].split('=')[1];
            //$('#pqr').attr("value", pqr); 

            // Charge distribution.
            jmolScript('load pqr::'+pdb_base_path+'%s-reo.pqr'.replace('%s', target+'-'+pHPad.split('\n')[0]));
            jmolScript('select 1.1');
            jmolScript('set propertycolorscheme "rwb"');
            jmolScript('color property partialcharge'); 
            jmolScript('spacefill 100%');
            // Protein representation.
            jmolScript('load APPEND '+pdb_base_path+'%s-reo.pdb'.replace('%s', target));
            jmolScript('select 2.1');
            jmolScript('ribbons only');
            // NW representation.
            jmolScript('load APPEND '+pdb_base_path+'nw_%s.xyz'.replace('%s', target));
            jmolScript('select 3.1');
            jmolScript('spacefill 20%');
            // Display configuration. 
            jmolScript('select 1.1 or 2.1');
            jmolScript('set allowRotateSelected');
            jmolScript('set dragSelected');
            jmolScript('frame *');
            // Report Jmol setup finished.
            cr();
        }

        // Status update.
        function status_update(step) 
        {
            $('#loader').css({"visibility":"visible"});
            $('#status').html("Done.<br />");
            $('#status').html(step);
            console.log("Started: " + step);
        }

        // Print response to console.
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
                //$('#status').html("Done.<br />");
                console.log("Response done.");
            }
        } 
        return false; // Prevent default submit behavior.
    }); // end submit
    $('#target').focus();
});//end ready
