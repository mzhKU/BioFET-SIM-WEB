$(document).ready(function()
{ 
    /* ------------------------------------------------------- */
    /* Get Jmol coordinates
    /* ------------------------------------------------------- */
    function getJmolCoordinates()
    {
        jmolScript("select 1.1"); 
        // Jmol selectors
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
        return data;
    }

    /* ------------------------------------------------------- */
    /* Two events assigned to form submission:
    - text area write
    - BFS cgi script
    /* ------------------------------------------------------- */
    $("#form_bfs").submit(function()
    {
        // Submit event parameters.
        var res_base_path = './bfs_res/';
        var cgi_base_path = './bfs_cgi/';
        var target        = $('#target').val();
        var pH            = $('#pHLab').val();
        var d             = new Date();

        // Setting the coordinates of the charges.
        var data = getJmolCoordinates(); 
        $('#pqr').attr('value', data); 

        // Select again PQR and PDB data
        jmolScript("select 1.1 or 2.1"); 

        // Serialize BFS parameter form data.
        var bfsForm = $("#form_bfs").serialize();
        $('#timestamp').attr('value', d.getTime());

        // Ajax BFS call.
        $.post(cgi_base_path + 'bio_sim.cgi', bfsForm, reload_plot);

        function reload_plot()
        { 
            $("#resPlot").attr("src", res_base_path + target + "-reo.svg?" + d.getTime());
        } 

        // Prevent default form submit
        return false; 
    }); // End submit 

    $('#pHresp').click(function()
    {
        var res_base_path = './bfs_res/';
        var cgi_base_path = './bfs_cgi/';
        var target        = $('#target').val();
        var data          = getJmolCoordinates();
        var bfsForm       = $('#form_bfs').serialize();
        var d             = new Date();
        $('#timestamp').attr('value', d.getTime());
        console.log("pH response click event."); 
        $.post(cgi_base_path + 'bio_run.cgi', bfsForm, cr);
    }); // End pH response click event.

    function rho()
    { 
        status_update('Charge distribution...');
        $.get(cgi_base_path + 'bio_rho.cgi', formData, build_interface);
        console.log("Charge distribution calculation request sent, waiting for response...");
    } 

    // Check HTTP response.
    function cr(resp) { console.log(resp); }

}); // End ready
