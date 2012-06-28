$(document).ready(function()
{ 
    var res_base_path = './bfs_res/';
    var cgi_base_path = './bfs_cgi/';
    var pdb_base_path = './bfs_pdb/';
    var ajax_loader   = "<img src='./bfs_jvs/ajax-loader.gif' alt='Loading...'>";

    // Check HTTP response.
    function cr(resp) { console.log(resp); }

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
    function resp()
    {

        function plot_pH_resp()
        {
            var d = new Date();
            $("#resPlot").attr("src", res_base_path + target + "-pH-reo.png?" + d.getTime());
        }

        function plot_bfs_resp()
        {
            var d = new Date();
            $("#resPlot").attr("src", res_base_path + target + "-reo.png?" + d.getTime());
        }

        // Jmol selectors
        var target   = $('#target').val();
        var atomInfo = jmolGetPropertyAsArray("atomInfo", "2.1"); 
        var form_bfs = $('#form_bfs').serialize();
        var pqr      = '';
        for(var i=0; i<atomInfo.length; i++)
        {
            // Prevent empty last line.
            if(i<atomInfo.length-1)
            {
                pqr += atomInfo[i].x + ' ' + atomInfo[i].y + ' ' + atomInfo[i].z + '\n';
            } else {
                pqr += atomInfo[i].x + ' ' + atomInfo[i].y + ' ' + atomInfo[i].z;
            }
        }

        /* 
        'tmp_pqr':  Coordinates of charges after move.
        'atomInfo': Does not provide access to charges.
                    Charges are added to BioFET-SIM input on server side.
        */
        form_bfs += '&tmp_pqr=' + pqr;

        // Get clicked button id.
        form_bfs += '&action=' + $(this).val(); 
        form_bfs += '&pH=' + $('#pH').val();
        if ($(this).val() == 'BioFET-SIM')
        {
            $.post(cgi_base_path + 'bio_run.cgi', form_bfs, cr);
        } else {
            $.post(cgi_base_path + 'bio_run.cgi', form_bfs, plot_pH_resp);
        }

        $('#status').html("Ready.");
    }

    $('#pHresp').click(resp);
    $('#bfs_signal').click(resp);
}); // End ready
