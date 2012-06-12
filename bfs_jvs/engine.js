$(document).ready(function()
{ 
    var res_base_path = './bfs_res/';
    var cgi_base_path = './bfs_cgi/';
    var pdb_base_path = './bfs_pdb/';
    /* ------------------------------------------------------- */
    /* Get Jmol coordinates
    /* ------------------------------------------------------- */
    function getJmolCoordinates()
    {
        jmolScript("select 1.1"); 
        // Jmol selectors, 'atomInfo' for coordinates, 'fileInfo' for charges.
        var atomsInfo = jmolGetPropertyAsArray("atomInfo", "all"); 
        var fileInfo  = jmolGetPropertyAsArray("fileContents").split(" | "); 
        // Charge is provided starting from index 55, truncate
        // coordinates to 5 positions.
        var data = ''
        for(var i=0; i<fileInfo.length-1; i++) { 
            data += fileInfo[i].slice(0, 31) + ' ';
            data += atomsInfo[i].x.toPrecision(5) + ' '; 
            data += atomsInfo[i].y.toPrecision(5) + ' ';
            data += atomsInfo[i].z.toPrecision(5) + ' ';
            data += fileInfo[i].slice(55) + '\n';
        } 
        /* Select movable atoms. */
        jmolScript("select 1.1 or 2.1"); 
        return data;
    }

    /* -------------------------------------------------------
       Form submission.
       ------------------------------------------------------- */
    $("#form_bfs").submit(function()
    {
        // Submit event parameters.
        var target        = $('#target').val();
        var pH            = $('#pHLab').val();
        var d             = new Date();

        // Setting the coordinates of the charges.
        var data = getJmolCoordinates(); 
        $('#pqr').attr('value', data); 

        // Select movable atoms.
        jmolScript("select 1.1 or 2.1"); 

        // Serialize BFS parameter form data and submit AJAX call.
        var bfsForm = $("#form_bfs").serialize();
        $('#timestamp').attr('value', d.getTime()); 
        // Ajax BFS call.
        $.post(cgi_base_path + 'bio_sim.cgi', bfsForm, reload_plot);
        
        function reload_plot()
        { 
            $("#resPlot").attr("src", res_base_path + target + "-reo.svg?" + d.getTime());
        } 

        // Prevent default form submit.
        return false; 
    }); // End submit 

    /* -------------------------------------------------------
       pH response.
       ------------------------------------------------------- */
    //$('#pHresp').click(function()
    $('#pHresp').live('click', function()
    {
        // Jmol selectors
        var target   = $('#target').val();
        var atomInfo = jmolGetPropertyAsArray("atomInfo", "2.1"); 
        var bfsForm  = $('#form_bfs').serialize();
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
        // 'tmp_pqr' are coordinates after move.
        $('#tmp_pqr').attr('value', pqr);
        $.post(cgi_base_path + 'bio_run.cgi', bfsForm, plot_pH_resp);
        
        function plot_pH_resp()
        {
            var d = new Date();
            $("#resPlot").attr("src", res_base_path + target + "-pH-reo.svg?" + d.getTime());
        }

    }); // End pH response click event.

    // Check HTTP response.
    function cr(resp) { console.log(resp); }

}); // End ready
