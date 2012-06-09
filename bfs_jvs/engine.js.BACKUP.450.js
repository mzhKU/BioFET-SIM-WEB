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
        /* Select movable atoms. */
        jmolScript("select 1.1 or 2.1"); 
        return data;
    }

    /* -------------------------------------------------------
       Form submission.
       ------------------------------------------------------- */
    $("#form_bfs").submit(function()
    {
<<<<<<< HEAD
        var res_base_path = './bfs_res/';
        var cgi_base_path = './bfs_cgi/';
        var target        = $('#target').val();
        var d             = new Date();

        var data = getJmolCoordinates();
        $('#pqr').attr("value", data); 
=======
        // Submit event parameters.
        var target        = $('#target').val();
        var pH            = $('#pHLab').val();
        var d             = new Date();

        // Setting the coordinates of the charges.
        var data = getJmolCoordinates(); 
        $('#pqr').attr('value', data); 
>>>>>>> dev_pH

        // Select movable atoms.
        jmolScript("select 1.1 or 2.1"); 

        // Serialize BFS parameter form data and submit AJAX call.
        var bfsForm = $("#form_bfs").serialize();
<<<<<<< HEAD
        //bfsForm += '&timestamp=' + d.getTime();
        $('#timestamp').attr('value', d.getTime());

        // Ajax BFS call.
=======
        $('#timestamp').attr('value', d.getTime()); 
>>>>>>> dev_pH
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
    $('#pHresp').click(function()
    {
        // Jmol selectors
        var target        = $('#target').val();
        var atomInfo      = jmolGetPropertyAsArray("atomInfo", "all");
        var fileInfo      = jmolGetPropertyAsArray("fileContents", pdb_base_path+target+"-reo.pdb").split(" | ");
        var bfsForm       = $('#form_bfs').serialize();
        var pdb           = '';
        for(var i=0; i<fileInfo.length-1; i++)
        {
            var pdbi=''
            pdbi += fileInfo[i].slice(0, 31) + '';
            pdbi += atomInfo[i].x.toPrecision(3) + ' '; 
            pdbi += atomInfo[i].y.toPrecision(3) + ' '; 
            pdbi += atomInfo[i].z.toPrecision(3) + ' '; 
            pdbi += fileInfo[i].slice(55)+'\n';
            //console.log(pdbi);
            pdb+=pdbi;
        }
        console.log(pdb);
        $('#tmp_pdb').attr('value', pdb);
        $.post(cgi_base_path + 'bio_run.cgi', bfsForm, cr);
    }); // End pH response click event.

    function pH_response()
    { 
        for (var i=0; i<15; i++)
        {
            $.post(cgi_base_path + 'bio_sim.cgi', bfsForm, pH_plot);
        }
    } // End pH response.

    function pH_plot(result)
    {
        console.log(result);
    }

    // Check HTTP response.
    function cr(resp) { console.log(resp); }

}); // End ready
