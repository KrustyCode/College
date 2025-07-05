<?php
$host = "localhost";
$user = "root"; //Usernam DB
$pass = ""; //Password Akun DB
$db   = "todolist"; // Nama DB

$koneksi = new mysqli($host, $user, $pass, $db);

if ($koneksi->connect_error) {
    die("Koneksi gagal: " . $koneksi->connect_error);
}
?>
