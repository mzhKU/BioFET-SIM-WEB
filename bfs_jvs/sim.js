// Assigning event handler to reload result image.
$('document').ready(function()
{
    //$('#dasfdsf').submit(function()
    $('#form_bfs').submit(function()
    {
        // Assemble BFS initialization form data, CGI directory base path
        // and Ajax loader HTML substitute.
        var formData      = $(this).serialize()
        var target        = $('#target').val();
        var pH            = $('#pHLab').val();
        //var pH            = $('#pHLab').html().split(':')[1];
        var cgi_base_path = './bfs_cgi/';
        var res_base_path = './bfs_res/';
        var ajax_loader   = "<img src='./bfs_jvs/ajax-loader.gif' alt='Loading...'>";

        // Report.
        //status_update('Calculating...');
        console.log(res_base_path + target + "-reo.png");
        console.log("Calculating sensitivity, waiting for response..."); 
        $.get(cgi_base_path + "bio_sim.cgi", formData, cr);

        function update_sens(resp)
        {
            $('#sens').html("Sensitivity: " + resp);
        }


        // Status update.
        //function status_update(step) 
        //{
        //    $('#loader').css({"visibility":"visible"});
        //    $('#status').html("Done.<br />");
        //    $('#status').html(step);
        //    console.log("Started: " + step);
        //}

        //// Print response to console.
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
                Consider using a JSON parse, separate parts of data are returned.
                var back = jQuery.parseJSON(resp);
                console.log(back[0]);
                */
                $('#loader').css({"visibility":"hidden"});
                $('#status').html("Done.<br />");
                console.log("Response done.");
            }
        } 
        return false; // Prevent default submit behavior.
    }); // end submit
});//end ready
