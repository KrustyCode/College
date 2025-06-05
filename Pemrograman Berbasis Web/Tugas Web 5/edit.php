<?php
include 'db.php';

$id = $_GET['id'];
$data = $koneksi->query("SELECT * FROM tugas WHERE id = $id")->fetch_assoc();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $judul     = $_POST['judul'];
    $deskripsi = $_POST['deskripsi'];
    $deadline  = $_POST['deadline'];
    $prioritas = $_POST['prioritas'];
    $status    = $_POST['status'];

    $koneksi->query("UPDATE tugas SET 
        judul = '$judul',
        deskripsi = '$deskripsi',
        deadline = '$deadline',
        prioritas = '$prioritas',
        status = '$status'
        WHERE id = $id");

    header("Location: index.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Tugas</title>
    <link rel="stylesheet" href="form.css">
</head>
<body>
    <div class="form-container">
        <h2>Edit Tugas</h2>
        <form method="POST">
            <div class="form-group">
                <label for="judul">Judul</label>
                <input type="text" name="judul" value="<?= htmlspecialchars($data['judul']) ?>" required>
            </div>
            <div class="form-group">
                <label for="deskripsi">Deskripsi</label>
                <textarea name="deskripsi" rows="3"><?= htmlspecialchars($data['deskripsi']) ?></textarea>
            </div>
            <div class="form-group">
                <label for="deadline">Deadline</label>
                <input type="date" name="deadline" value="<?= $data['deadline'] ?>">
            </div>
            <div class="form-group">
                <label for="prioritas">Prioritas</label>
                <select name="prioritas">
                    <option value="Rendah" <?= $data['prioritas'] === 'Rendah' ? 'selected' : '' ?>>Rendah</option>
                    <option value="Sedang" <?= $data['prioritas'] === 'Sedang' ? 'selected' : '' ?>>Sedang</option>
                    <option value="Tinggi" <?= $data['prioritas'] === 'Tinggi' ? 'selected' : '' ?>>Tinggi</option>
                </select>
            </div>
            <div class="form-group">
                <label for="status">Status</label>
                <select name="status">
                    <option value="Belum" <?= $data['status'] === 'Belum' ? 'selected' : '' ?>>Belum</option>
                    <option value="Sedang Dikerjakan" <?= $data['status'] === 'Sedang Dikerjakan' ? 'selected' : '' ?>>Sedang Dikerjakan</option>
                    <option value="Selesai" <?= $data['status'] === 'Selesai' ? 'selected' : '' ?>>Selesai</option>
                </select>
            </div>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <button type="submit">Simpan Perubahan</button>
                <a href="index.php" class="back-button">Kembali</a>
            </div>
        </form>
    </div>
    <script src="validation.js"></script>
</body>
</html>
