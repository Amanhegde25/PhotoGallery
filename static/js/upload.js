// Upload page functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileUpload = document.getElementById('fileUpload');
    const fileName = document.getElementById('fileName');

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                fileName.textContent = this.files[0].name;
                fileName.style.display = 'block';
            }
        });
    }

    if (fileUpload) {
        fileUpload.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('dragover');
        });

        fileUpload.addEventListener('dragleave', function() {
            this.classList.remove('dragover');
        });

        fileUpload.addEventListener('drop', function() {
            this.classList.remove('dragover');
        });
    }
});
