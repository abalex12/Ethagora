class ImageSlider {
    constructor() {
        this.currentSlide = 0;
        this.totalSlides = document.querySelectorAll('.slider-image').length;
        this.slider = document.getElementById('image-slider');
        this.counter = document.getElementById('image-counter');
        this.prevBtn = document.getElementById('prev-btn');
        this.nextBtn = document.getElementById('next-btn');
        
        this.init();
    }
    
    init() {
        if (this.totalSlides <= 1) return;
        
        // Event listeners for navigation buttons
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.prevSlide());
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.nextSlide());
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prevSlide();
            if (e.key === 'ArrowRight') this.nextSlide();
        });
        
        // Touch/swipe support
        let startX = 0;
        let endX = 0;
        
        this.slider.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });
        
        this.slider.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            this.handleSwipe();
        });
        
        // Auto-play (optional)
        // this.startAutoPlay();
        
        this.updateThumbnails();
    }
    
    goToSlide(index) {
        if (index < 0 || index >= this.totalSlides) return;
        
        this.currentSlide = index;
        this.updateSlider();
        this.updateCounter();
        this.updateThumbnails();
    }
    
    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % this.totalSlides;
        this.updateSlider();
        this.updateCounter();
        this.updateThumbnails();
    }
    
    prevSlide() {
        this.currentSlide = (this.currentSlide - 1 + this.totalSlides) % this.totalSlides;
        this.updateSlider();
        this.updateCounter();
        this.updateThumbnails();
    }
    
    updateSlider() {
        const translateX = -this.currentSlide * 100;
        this.slider.style.transform = `translateX(${translateX}%)`;
    }
    
    updateCounter() {
        if (this.counter) {
            this.counter.textContent = this.currentSlide + 1;
        }
    }
    
    updateThumbnails() {
        const thumbnails = document.querySelectorAll('.thumbnail-image');
        thumbnails.forEach((thumb, index) => {
            thumb.classList.remove('border-accent', 'scale-110');
            thumb.classList.add('border-transparent');
            
            if (index === this.currentSlide) {
                thumb.classList.remove('border-transparent');
                thumb.classList.add('border-accent', 'scale-110');
            }
        });
    }
    
    handleSwipe() {
        const swipeThreshold = 50;
        const diff = startX - endX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                this.nextSlide();
            } else {
                this.prevSlide();
            }
        }
    }
    
    startAutoPlay() {
        setInterval(() => {
            this.nextSlide();
        }, 5000); // Change slide every 5 seconds
    }
}

// Global function for thumbnail clicks
function goToSlide(index) {
    if (window.imageSlider) {
        window.imageSlider.goToSlide(index);
    }
}

// Modal functions
function openImageModal() {
    const currentImage = document.querySelector('.slider-image[data-index="' + (window.imageSlider ? window.imageSlider.currentSlide : 0) + '"]');
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    
    modalImage.src = currentImage.src;
    modalImage.alt = currentImage.alt;
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeImageModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.imageSlider = new ImageSlider();
    
    // Close modal on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeImageModal();
        }
    });
    
    // Close modal on background click
    document.getElementById('imageModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeImageModal();
        }
    });
    
    // Status dropdown behavior
    const statusDetails = document.querySelector('[data-status]');
    if (statusDetails) {
        statusDetails.addEventListener('toggle', function() {
            const chevron = this.querySelector('.chevron');
            if (this.open) {
                chevron.style.transform = 'rotate(180deg)';
            } else {
                chevron.style.transform = 'rotate(0deg)';
            }
        });
    }
});

class EnhancedImageSlider extends ImageSlider {
   constructor() {
       super();
       this.isPlaying = false;
       this.autoPlayInterval = null;
       this.touchStartX = 0;
       this.touchStartY = 0;
       this.isDragging = false;
   }
   
   // Preload images for better performance
   preloadImages() {
       const images = document.querySelectorAll('.slider-image');
       images.forEach(img => {
           const imageLoader = new Image();
           imageLoader.src = img.src;
       });
   }
   
   // Enhanced touch handling
   setupTouchEvents() {
       const slider = this.slider;
       let startTime = 0;
       
       slider.addEventListener('touchstart', (e) => {
           this.touchStartX = e.touches[0].clientX;
           this.touchStartY = e.touches[0].clientY;
           startTime = Date.now();
           this.isDragging = true;
           
           // Stop auto-play when user interacts
           this.pauseAutoPlay();
       }, { passive: true });
       
       slider.addEventListener('touchmove', (e) => {
           if (!this.isDragging) return;
           
           const deltaX = e.touches[0].clientX - this.touchStartX;
           const deltaY = e.touches[0].clientY - this.touchStartY;
           
           // Prevent vertical scrolling if horizontal swipe is detected
           if (Math.abs(deltaX) > Math.abs(deltaY)) {
               e.preventDefault();
           }
       }, { passive: false });
       
       slider.addEventListener('touchend', (e) => {
           if (!this.isDragging) return;
           
           const endX = e.changedTouches[0].clientX;
           const endTime = Date.now();
           const deltaX = this.touchStartX - endX;
           const deltaTime = endTime - startTime;
           const velocity = Math.abs(deltaX) / deltaTime;
           
           // Require minimum swipe distance and velocity
           if (Math.abs(deltaX) > 50 && velocity > 0.3) {
               if (deltaX > 0) {
                   this.nextSlide();
               } else {
                   this.prevSlide();
               }
           }
           
           this.isDragging = false;
           
           // Resume auto-play after interaction
           setTimeout(() => this.resumeAutoPlay(), 3000);
       }, { passive: true });
   }
   
   // Auto-play functionality
   startAutoPlay(interval = 5000) {
       if (this.totalSlides <= 1) return;
       
       this.autoPlayInterval = setInterval(() => {
           this.nextSlide();
       }, interval);
       this.isPlaying = true;
   }
   
   pauseAutoPlay() {
       if (this.autoPlayInterval) {
           clearInterval(this.autoPlayInterval);
           this.autoPlayInterval = null;
       }
       this.isPlaying = false;
   }
   
   resumeAutoPlay() {
       if (!this.isPlaying && this.totalSlides > 1) {
           this.startAutoPlay();
       }
   }
   
   // Lazy loading for better performance
   setupLazyLoading() {
       const images = document.querySelectorAll('.slider-image[data-src]');
       const imageObserver = new IntersectionObserver((entries, observer) => {
           entries.forEach(entry => {
               if (entry.isIntersecting) {
                   const img = entry.target;
                   img.src = img.dataset.src;
                   img.classList.remove('lazy');
                   observer.unobserve(img);
               }
           });
       });
       
       images.forEach(img => imageObserver.observe(img));
   }
   
   // Initialize all enhanced features
   init() {
       super.init();
       this.preloadImages();
       this.setupTouchEvents();
       this.setupLazyLoading();
       
       // Optional: Start auto-play (uncomment if desired)
       // this.startAutoPlay();
   }
}

// Status dropdown enhancement
class StatusDropdown {
   constructor() {
       this.dropdown = document.querySelector('[data-status]');
       this.init();
   }
   
   init() {
       if (!this.dropdown) return;
       
       // Close dropdown when clicking outside
       document.addEventListener('click', (e) => {
           if (!this.dropdown.contains(e.target)) {
               this.dropdown.removeAttribute('open');
           }
       });
       
       // Handle status changes with loading states
       const statusLinks = this.dropdown.querySelectorAll('.status-menu a');
       statusLinks.forEach(link => {
           link.addEventListener('click', (e) => {
               e.preventDefault();
               this.handleStatusChange(link);
           });
       });
   }
   
   async handleStatusChange(link) {
       const url = link.href;
       const icon = link.querySelector('i');
       const originalIcon = icon.className;
       
       // Show loading state
       icon.className = 'fas fa-spinner fa-spin mr-2';
       link.style.opacity = '0.7';
       
       try {
           const response = await fetch(url, {
               method: 'POST',
               headers: {
                   'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
               },
           });
           
           if (response.ok) {
               // Reload page to reflect changes
               window.location.reload();
           } else {
               throw new Error('Network response was not ok');
           }
       } catch (error) {
           console.error('Error updating status:', error);
           // Restore original state
           icon.className = originalIcon;
           link.style.opacity = '1';
           
           // Show error message (you can customize this)
           alert('Error updating status. Please try again.');
       }
   }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
   // Use enhanced slider instead of basic one
   window.imageSlider = new EnhancedImageSlider();
   window.statusDropdown = new StatusDropdown();
   
   // Initialize modal functionality
   initializeModal();
   
   // Add smooth scrolling to thumbnail gallery
   const thumbnailGallery = document.querySelector('.thumbnail-gallery');
   if (thumbnailGallery) {
       thumbnailGallery.classList.add('scroll-smooth');
   }
});

// Modal functionality
function initializeModal() {
   const modal = document.getElementById('imageModal');
   
   // Keyboard navigation in modal
   document.addEventListener('keydown', function(e) {
       if (!modal.classList.contains('hidden')) {
           switch(e.key) {
               case 'Escape':
                   closeImageModal();
                   break;
               case 'ArrowLeft':
                   if (window.imageSlider) window.imageSlider.prevSlide();
                   updateModalImage();
                   break;
               case 'ArrowRight':
                   if (window.imageSlider) window.imageSlider.nextSlide();
                   updateModalImage();
                   break;
           }
       }
   });
   
   // Update modal image when slider changes
   function updateModalImage() {
       const modalImage = document.getElementById('modalImage');
       const currentSlide = window.imageSlider ? window.imageSlider.currentSlide : 0;
       const currentImage = document.querySelector(`.slider-image[data-index="${currentSlide}"]`);
       
       if (currentImage && modalImage) {
           modalImage.src = currentImage.src;
       }
   }
}

// Utility functions for better UX
function showToast(message, type = 'info') {
   // Create toast notification (you can style this as needed)
   const toast = document.createElement('div');
   toast.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 transition-all duration-300 ${
       type === 'error' ? 'bg-red-500 text-white' : 'bg-blue-500 text-white'
   }`;
   toast.textContent = message;
   
   document.body.appendChild(toast);
   
   setTimeout(() => {
       toast.remove();
   }, 3000);
}

// Performance optimization: Debounce resize events
function debounce(func, wait) {
   let timeout;
   return function executedFunction(...args) {
       const later = () => {
           clearTimeout(timeout);
           func(...args);
       };
       clearTimeout(timeout);
       timeout = setTimeout(later, wait);
   };
}

// Handle responsive image sizing
window.addEventListener('resize', debounce(() => {
   if (window.imageSlider) {
       window.imageSlider.updateSlider();
   }
}, 250));
