<?php
foreach ($_FILES["images"]["error"] as $key => $error) {
    if ($error == UPLOAD_ERR_OK) {
        $name = $_FILES["images"]["name"][$key];
        move_uploaded_file( $_FILES["images"]["tmp_name"][$key], "./bfs_pdb/" . $_FILES['images']['name'][$key]);
        chmod("./bfs_pdb/" . $name, 0755);
    }
}

echo "<h2>Successfully uploaded file.</h2>";
echo "Return to <a href=\"http://www.biofetsim.org/ku_prototype.html\">BioFET-SIM Online</a>.<br />";
echo "Use " .basename($name, ".pdb") ." as input.";
?>
