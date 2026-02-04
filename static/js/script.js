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

    // =============================
    // Tag Section Functionality
    // =============================
    
    // Update tag counts and hide empty sections
    document.querySelectorAll('.tag-gallery').forEach(gallery => {
        const tag = gallery.id.replace('gallery-', '');
        const count = gallery.querySelectorAll('.image-card').length;
        const countEl = document.getElementById('count-' + tag);
        if (countEl) {
            countEl.textContent = `(${count} photos)`;
        }

        // Hide view more button if 3 or fewer images
        const btn = gallery.parentElement.querySelector('.view-more-btn');
        if (count <= 3 && btn) {
            btn.style.display = 'none';
        }

        // Hide entire section if no images
        if (count === 0) {
            gallery.parentElement.style.display = 'none';
            // Also hide the tab for this tag
            const tab = document.querySelector(`.tag-tab[data-tag="${tag}"]`);
            if (tab) {
                tab.style.display = 'none';
            }
        }
    });

    // Tab click handling - show/hide sections directly
    document.querySelectorAll('.tag-tab').forEach(tab => {
        tab.addEventListener('click', function () {
            const selectedTag = this.dataset.tag;

            // Update active tab
            document.querySelectorAll('.tag-tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            // Get all tag sections
            const allSections = document.querySelectorAll('.tag-section[data-section-tag]');

            if (selectedTag === 'all') {
                // Show all sections (collapsed)
                allSections.forEach(section => {
                    const sectionTag = section.dataset.sectionTag;
                    const gallery = document.getElementById('gallery-' + sectionTag);
                    const count = gallery ? gallery.querySelectorAll('.image-card').length : 0;

                    // Only show sections that have images
                    if (count > 0) {
                        section.style.display = 'block';
                        // Collapse the gallery
                        if (gallery) gallery.classList.add('collapsed');
                        // Reset view more button
                        const btn = section.querySelector('.view-more-btn');
                        if (btn && count > 3) {
                            btn.textContent = 'View More';
                            btn.classList.remove('view-less-btn');
                        }
                    }
                });
            } else {
                // Show only the selected tag section (expanded)
                allSections.forEach(section => {
                    const sectionTag = section.dataset.sectionTag;
                    if (sectionTag === selectedTag) {
                        section.style.display = 'block';
                        // Expand the gallery
                        const gallery = document.getElementById('gallery-' + sectionTag);
                        if (gallery) gallery.classList.remove('collapsed');
                        // Hide view more button when expanded
                        const btn = section.querySelector('.view-more-btn');
                        if (btn) {
                            btn.textContent = 'View Less';
                            btn.classList.add('view-less-btn');
                        }
                    } else {
                        section.style.display = 'none';
                    }
                });
            }
        });
    });
});

// =============================
// Tag Section Toggle Function
// =============================
function toggleTagSection(tag) {
    const gallery = document.getElementById('gallery-' + tag);
    if (!gallery) return;
    
    const btn = gallery.parentElement.querySelector('.view-more-btn');

    if (gallery.classList.contains('collapsed')) {
        gallery.classList.remove('collapsed');
        if (btn) {
            btn.textContent = 'View Less';
            btn.classList.add('view-less-btn');
        }
    } else {
        gallery.classList.add('collapsed');
        if (btn) {
            btn.textContent = 'View More';
            btn.classList.remove('view-less-btn');
        }
    }
}

// =============================
// Slideshow Functionality
// =============================
let currentSlide = 0;
let slideInterval;
const slides = document.querySelectorAll('.slide');
const slideshowNav = document.getElementById('slideshowNav');
const trendingSection = document.getElementById('trendingSection');

// Initialize slideshow
function initSlideshow() {
    if (slides.length === 0) {
        // Hide trending section if no slides
        if (trendingSection) {
            trendingSection.style.display = 'none';
        }
        return;
    }

    // Generate navigation dots
    if (slideshowNav) {
        slideshowNav.innerHTML = '';
        slides.forEach((_, index) => {
            const dot = document.createElement('button');
            dot.className = 'slide-dot' + (index === 0 ? ' active' : '');
            dot.onclick = () => goToSlide(index);
            slideshowNav.appendChild(dot);
        });
    }

    // Start auto-rotation
    startSlideshow();
}

function startSlideshow() {
    slideInterval = setInterval(() => {
        changeSlide(1);
    }, 5000); // Change slide every 5 seconds
}

function stopSlideshow() {
    clearInterval(slideInterval);
}

function changeSlide(direction) {
    stopSlideshow();
    currentSlide += direction;

    if (currentSlide >= slides.length) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }

    updateSlides();
    startSlideshow();
}

function goToSlide(index) {
    stopSlideshow();
    currentSlide = index;
    updateSlides();
    startSlideshow();
}

function updateSlides() {
    // Update slides
    slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
    });

    // Update dots
    const dots = document.querySelectorAll('.slide-dot');
    dots.forEach((dot, index) => {
        dot.classList.toggle('active', index === currentSlide);
    });
}

// Initialize slideshow on page load
if (slides.length > 0) {
    initSlideshow();
}
