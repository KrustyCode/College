<?php
$host = "localhost";
$user = "root";
$pass = "";
$db = "pancaran";

$koneksi = pg_connect("dbname=pancaran") or die("Koneksi gagal: ". pg_last_error());

$query = "INSERT INTO forum.posts (title, text, user_id, post_id) VALUES ('{$_POST['title']}', '{$_POST['text']}', 4, 1)";

$result = pg_query($koneksi, $query) or die("Gagal Add Post: ". pg_last_error());

header('Location: '. '/');
?>

