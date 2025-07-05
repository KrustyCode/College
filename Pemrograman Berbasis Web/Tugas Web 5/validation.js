document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", function (event) {
        const judul = form.querySelector("input[name='judul']").value.trim();
        const deskripsi = form.querySelector("textarea[name='deskripsi']").value.trim();
        const deadline = form.querySelector("input[name='deadline']").value;
        const prioritas = form.querySelector("select[name='prioritas']").value;
        const status = form.querySelector("select[name='status']").value;

        let errorMessages = [];

        if (judul.length < 1) {
            errorMessages.push("Judul harus isi.");
        }

        if (judul.length > 100) {
            errorMessages.push("Judul tidak boleh lebih dari 100 karakter.");
        }

        if (deskripsi.length > 500) {
            errorMessages.push("Deskripsi tidak boleh lebih dari 500 karakter.");
        }

        const validPrioritas = ["Rendah", "Sedang", "Tinggi"];
        const validStatus = ["Belum", "Sedang Dikerjakan", "Selesai"];

        if (!validPrioritas.includes(prioritas)) {
            errorMessages.push("Prioritas tidak valid.");
        }

        if (!validStatus.includes(status)) {
            errorMessages.push("Status tidak valid.");
        }

        if (errorMessages.length > 0) {
            event.preventDefault();
            alert(errorMessages.join("\n"));
        }
    });
});
