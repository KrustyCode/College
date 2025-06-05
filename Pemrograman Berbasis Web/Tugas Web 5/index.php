<?php
include 'db.php';

// Hapus jika ada POST
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST['id'])) {
    $id = (int)$_POST['id'];
    $koneksi->query("DELETE FROM tugas WHERE id = $id");  
    header("Location: index.php");
    exit;
}

// Ambil semua data
$result = $koneksi->query("SELECT * FROM tugas ORDER BY deadline ASC");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Daftar Tugas</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

<div class="table-container">
    <div class="table-header">
        <h2>Daftar Tugas</h2>
        <a href="tambah.php" class="add-button">+ Tambah</a>
    </div>

    <table>
        <thead>
            <tr>
                <th>Judul</th>
                <th>Deskripsi</th>
                <th>Deadline</th>
                <th>Prioritas</th>
                <th>Status</th>
                <th>Aksi</th>
            </tr>
        </thead>
        <tbody>
            <?php while($row = mysqli_fetch_assoc($result)): ?>
                <tr>
                    <td><?= htmlspecialchars($row['judul']) ?></td>
                    <td><?= htmlspecialchars($row['deskripsi']) ?></td>
                    <td><?= htmlspecialchars($row['deadline']) ?></td>
                    <td><?= htmlspecialchars($row['prioritas']) ?></td>
                    <td><?= htmlspecialchars($row['status']) ?></td>
                    <td>
                        <div class="action-button-container">
                            <a href="edit.php?id=<?= $row['id'] ?>">
                                <button class="edit-button">Edit</button>
                            </a>
                            <form action="hapus.php" method="POST" onsubmit="return confirm('Yakin ingin menghapus?')">
                                <input type="hidden" name="id" value="<?= $row['id'] ?>">
                                <button type="submit" class="delete-button">Hapus</button>
                            </form>
                        </div>
                    </td>
                </tr>
            <?php endwhile; ?>
        </tbody>
    </table>
</div>

</body>
</html>