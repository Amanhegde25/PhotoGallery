/* ================================
   Combined Scripts
   - Gallery (Lightbox) functionality
   - Upload (File handling) functionality
   ================================ */

document.addEventListener('DOMContentLoaded', function() {
    
    // =============================
    // Lightbox Functionality
    // =============================
    const lightbox = document.getElementById('lightbox');
    const lightboxImage = document.getElementById('lightboxImage');
    const lightboxTitle = document.getElementById('lightboxTitle');
    const lightboxCaption = document.getElementById('lightboxCaption');
    const lightboxMeta = document.getElementById('lightboxMeta');
    const lightboxClose = document.getElementById('lightboxClose');

    // Open lightbox when clicking on image card
    document.querySelectorAll('.image-card').forEach(card => {
        card.addEventListener('click', function() {
            const img = this.querySelector('.image-wrapper img');
            const title = this.querySelector('.image-title');
            const caption = this.querySelector('.image-caption');
            const metaItems = this.querySelectorAll('.meta-item');

            lightboxImage.src = img.src;
            lightboxImage.alt = img.alt;
            lightboxTitle.textContent = title ? title.textContent : '';
            lightboxCaption.textContent = caption ? caption.textContent : '';

            // Build meta info
            let metaHTML = '';
            metaItems.forEach(item => {
                metaHTML += '<span>' + item.textContent.trim() + '</span>';
            });
            lightboxMeta.innerHTML = metaHTML;

            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    // Close lightbox on button click
    if (lightboxClose) {
        lightboxClose.addEventListener('click', closeLightbox);
    }

    // Close lightbox on background click
    if (lightbox) {
        lightbox.addEventListener('click', function(e) {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }

    // Close lightbox on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeLightbox();
        }
    });

    function closeLightbox() {
        if (lightbox) {
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
        }
    }

    // =============================
    // Upload/File Functionality
    // =============================
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
