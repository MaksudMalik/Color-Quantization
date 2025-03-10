document.addEventListener("DOMContentLoaded", function () {

    const uploadBox = document.getElementById("upload_box");
    const fileInput = document.getElementById("file_input");
    const error_text = document.getElementById("error_text");
    const before_upload_box = document.getElementById('empty_upload_box');
    const before_processed_box = document.getElementById('empty_processed_box');
    const uploadedContent = document.querySelectorAll('.original_image');
    const processedContent = document.querySelectorAll('.processed_image');
    const submit_button =  document.getElementById("submit_button")
    let original_file = null;

    function updateValue(id) {
        document.getElementById(id + "_value").textContent = document.getElementById(id).value;
    }
    document.getElementById("num_colors").addEventListener("input", function () {
        updateValue("num_colors");
    });
    document.getElementById("iterations").addEventListener("input", function () {
        updateValue("iterations");
    });


    uploadBox.addEventListener("click", function () {
        fileInput.click();
    });


    fileInput.addEventListener("change", async function () {
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });
        if (response.ok) {
            const data = await response.json();
            document.querySelector('img.original_image').src = `data:image/png;base64,${data.original_img_base64}`;
            original_file = data.original_img_base64;
            before_upload_box.style.display = 'none';
            before_processed_box.style.display = 'none';
            error_text.style.display="none";
            uploadedContent.forEach(function(element) {
                element.style.display = "flex";
            });
            submit_button.disabled = false;
        }
        else{
            uploadedContent.forEach(function(element) {
                element.style.display = "none";
            });
            processedContent.forEach(function(element) {
                element.style.display = "none";
            });
            before_processed_box.style.display = 'block';
            before_upload_box.style.display='none'
            error_text.style.display="block";
            submit_button.disabled = true;
        }
    });


    document.getElementById("submit_button").addEventListener("click", async function () {
        const numColors = document.getElementById("num_colors").value;
        const iterations = document.getElementById("iterations").value;
        const formData = new FormData();
        formData.append("num_colors", numColors);
        formData.append("iterations", iterations);
        formData.append("img_base64", original_file);
        const response = await fetch("/quantize", {
            method: "POST",
            body: formData
        });
        if (response.ok) {
            const data = await response.json();
            document.querySelector('img.processed_image').src = `data:image/png;base64,${data.processed_img_base64}`;
            uploadedContent[2].style.display = 'none';
            processedContent.forEach(function(element) {
                element.style.display = "flex";
            });
            
        } else {
            const data = await response.json();
            alert(data.error_message);
        }
    });

});
