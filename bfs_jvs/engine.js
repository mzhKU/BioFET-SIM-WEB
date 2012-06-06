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
    /* Show coordinate update.
    /* ------------------------------------------------------- */
    $("#update").click(function()
    {
        console.log(-123.23.toPrecision(6));
        console.log(-123.23.toPrecision(3));
        console.log(-123.23.toPrecision(1));
        console.log(-123.23.toPrecision(8));
        console.log(123.23.toPrecision(8));
        var data = getJmolCoordinates();
        console.log(data);
        jmolScript("select 1.1 or 2.1"); 
    });

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
        var target = $('#target').val();
        var pH     = $('#pHLab').val();
        var d      = new Date();

        var data = getJmolCoordinates();
        $('#pqr').attr("value", data); 

        // Select again PQR and PDB data
        jmolScript("select 1.1 or 2.1"); 

        // Serialize BFS parameter form data.
        var bfsForm = $("#form_bfs").serialize();
        //bfsForm += '&timestamp=' + d.getTime();
        $('#timestamp').attr('value', d);

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
        var data = getJmolCoordinates();
        var form = $('#form_bfs').serialize();
        console.log("pH response click event."); 
        $.post(cgi_base_path + 'bio_run.cgi', bfsForm, cr);
    }); // End pH response click event.

    // Check HTTP response.
    function cr(resp) { console.log(resp); }

}); // End ready
