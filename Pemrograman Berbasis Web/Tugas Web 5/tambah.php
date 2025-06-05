<?php
include 'db.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $judul     = $_POST['judul'];
    $deskripsi = $_POST['deskripsi'];
    $deadline  = $_POST['deadline'];
    $prioritas = $_POST['prioritas'];
    $status    = $_POST['status'];

    $koneksi->query("INSERT INTO tugas (judul, deskripsi, deadline, prioritas, status)
                     VALUES ('$judul', '$deskripsi', '$deadline', '$prioritas', '$status')");

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Tambah Tugas</title>
    <link rel="stylesheet" href="form.css">
</head>
<body>
    <div class="form-container">
        <h2>Tambah Tugas</h2>
        <form action="tambah.php" method="POST">
            <div class="form-group">
                <label for="judul">Judul</label>
                <input type="text" name="judul" required>
            </div>
            <div class="form-group">
                <label for="deskripsi">Deskripsi</label>
                <textarea name="deskripsi" rows="3"></textarea>
            </div>
            <div class="form-group">
                <label for="deadline">Deadline</label>
                <input type="date" name="deadline">
            </div>
            <div class="form-group">
                <label for="prioritas">Prioritas</label>
                <select name="prioritas">
                    <option value="Rendah">Rendah</option>
                    <option value="Sedang">Sedang</option>
                    <option value="Tinggi">Tinggi</option>
                </select>
            </div>
            <div class="form-group">
                <label for="status">Status</label>
                <select name="status">
                    <option value="Belum">Belum</option>
                    <option value="Sedang Dikerjakan">Sedang Dikerjakan</option>
                    <option value="Selesai">Selesai</option>
                </select>
            </div>
            <button type="submit">Simpan</button>
            <a href="index.php" class="back-button">Kembali</a>
        </form>
    </div>
    <script src="validation.js"></script>
</body>
</html>
