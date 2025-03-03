document.addEventListener("DOMContentLoaded", function () {
    function updateValue(id) {
        document.getElementById(id + "_value").textContent = document.getElementById(id).value;
    }
    document.getElementById("num_colors").addEventListener("input", function () {
        updateValue("num_colors");
    });
    document.getElementById("iterations").addEventListener("input", function () {
        updateValue("iterations");
    });

    const uploadBox = document.getElementById("upload_box");
    const fileInput = document.getElementById("file_input");

    if (uploadBox && fileInput) {
        uploadBox.addEventListener("click", function () {
            fileInput.click();
        });

        fileInput.addEventListener("change", function () {
            fileInput.form.submit();
        });
    }
});

