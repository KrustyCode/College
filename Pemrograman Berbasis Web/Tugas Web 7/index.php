<?php
$host = "localhost";
$user = "root";
$pass = "";
$db = "pancaran";

$koneksi = pg_connect("dbname=pancaran") or die("Koneksi gagal: " . pg_last_error());

$query = "SELECT * from forum.posts WHERE parent_id IS NULL";

$posts = pg_query($koneksi, $query) or die("Gagal Ambil Post: " . pg_last_error());

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    POSTINGAN KOCAK
    <form method="post" action="add_post.php">
        <h1>Bikin Post</h1>
        JUDUL: <input type="text" name="title">
        <br>
        ISI: <input type="text" name="text">
        <br>
        <button type="submit">Submit</button>
    </form>

    <?php
    while ($post = pg_fetch_array($posts, null, PGSQL_ASSOC)) {
        foreach ($post as $title) {
            echo "\t\t<td>$title</td>\n";
        }
    }
    ?>

</body>

</html>