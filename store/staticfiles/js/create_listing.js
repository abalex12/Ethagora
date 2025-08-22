document.addEventListener('DOMContentLoaded', function() {
    // Add required CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .field-error {
            animation: shake 0.5s ease-in-out;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    `;
    document.head.appendChild(style);

    // Ethiopian cities data
    const cities = [
        "Addis Ababa", "Dire Dawa", "Mekelle", "Adama", "Hawassa",
        "Bahir Dar", "Gondar", "Dessie", "Jimma", "Bishoftu",
        "Kombolcha", "Harar", "Sodo", "Shashamene", "Hosaena",
        "Arba Minch", "Adigrat", "Debre Markos", "Debre Birhan", "Jijiga",
        "Ziway", "Dila", "Gambela", "Axum", "Waliso",
        "Yirga Alem", "Mojo", "Goba", "Shakiso", "Areka",
        "Boditi", "Debre Tabor", "Jinka", "Gimbi", "Asosa",
        "Butajira", "Metu", "Agaro", "Korem"
    ];

    // Initialize all functionality
    initCategorySubcategory();
    initImageUpload();
    initCityAutoComplete();
    initFormValidation();

    // Category → Subcategory AJAX functionality
    function initCategorySubcategory() {
        const categorySelect = document.getElementById('id_category');
        const subcategorySelect = document.getElementById('id_subcategory');
        
        if (!categorySelect || !subcategorySelect) return;

        categorySelect.addEventListener('change', function() {
            const categoryId = this.value;
            subcategorySelect.innerHTML = '<option value="">Loading...</option>';
            subcategorySelect.disabled = true;

            if (categoryId) {
                fetch(`/api/subcategories/?category_id=${categoryId}`)
                    .then(res => {
                        if (!res.ok) throw new Error('Network response was not ok');
                        return res.json();
                    })
                    .then(data => {
                        subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>';
                        data.forEach(sc => {
                            const opt = document.createElement('option');
                            opt.value = sc.id;
                            opt.textContent = sc.name;
                            subcategorySelect.appendChild(opt);
                        });
                        subcategorySelect.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error loading subcategories:', error);
                        subcategorySelect.innerHTML = '<option value="">Error loading subcategories</option>';
                        subcategorySelect.disabled = false;
                    });
            } else {
                subcategorySelect.innerHTML = '<option value="">Select Subcategory</option>';
                subcategorySelect.disabled = false;
            }
        });
    }

    // Image upload functionality
    function initImageUpload() {
        // Initialize existing image forms
        document.querySelectorAll('.image-form-group').forEach(initImageFormEvents);

        // Add new image form functionality
        const addImageBtn = document.getElementById('add-image-btn');
        const totalForms = document.getElementById('id_images-TOTAL_FORMS');
        const formContainer = document.getElementById('image-forms');
        const emptyFormTemplate = document.getElementById('empty-form-template');

        if (addImageBtn && totalForms && formContainer && emptyFormTemplate) {
            addImageBtn.addEventListener('click', function() {
                const formIndex = parseInt(totalForms.value);
                
                // Limit to 6 images
                if (formIndex >= 6) {
                    showNotification('Maximum 6 images allowed', 'warning');
                    return;
                }
                
                const newFormHtml = emptyFormTemplate.innerHTML.replace(/__prefix__/g, formIndex);
                formContainer.insertAdjacentHTML('beforeend', newFormHtml);
                totalForms.value = formIndex + 1;
                
                const newFormGroup = formContainer.lastElementChild;
                initImageFormEvents(newFormGroup);
                
                // Scroll to new form with animation
                newFormGroup.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                newFormGroup.style.animation = 'slideIn 0.5s ease-out';
                
                // Hide button if limit reached
                if (formIndex + 1 >= 6) {
                    addImageBtn.style.display = 'none';
                }
            });
        }

        // Primary image selection logic
        document.addEventListener('change', function(e) {
            if (e.target.name && e.target.name.includes('is_primary')) {
                // Uncheck other primary checkboxes
                document.querySelectorAll('input[name*="is_primary"]').forEach(checkbox => {
                    if (checkbox !== e.target) {
                        checkbox.checked = false;
                    }
                });
            }
        });
    }

    // Enhanced image form events
    function initImageFormEvents(formGroup) {
        const uploadBtn = formGroup.querySelector('.image-upload-btn');
        const fileInput = formGroup.querySelector('input[type=file]');
        const preview = formGroup.querySelector('.image-preview');

        if (!uploadBtn || !fileInput || !preview) return;

        uploadBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Validate file size (5MB limit)
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('File size must be less than 5MB', 'error');
                    this.value = '';
                    return;
                }
                
                // Validate file type
                if (!file.type.startsWith('image/')) {
                    showNotification('Please select a valid image file', 'error');
                    this.value = '';
                    return;
                }

                const reader = new FileReader();
                reader.onload = e => {
                    preview.innerHTML = `<img src="${e.target.result}" class="max-w-full max-h-full object-cover group-hover:scale-105 transition-transform duration-300" alt="Preview">`;
                    uploadBtn.innerHTML = '<i class="fas fa-sync-alt mr-2"></i>Change Photo';
                    
                    // Add success animation
                    preview.style.animation = 'pulse 0.5s ease-in-out';
                    setTimeout(() => preview.style.animation = '', 500);
                };
                reader.readAsDataURL(file);
            }
        });

        // Click on preview to change image
        preview.addEventListener('click', () => {
            if (preview.querySelector('img')) {
                fileInput.click();
            }
        });
    }

    // City autocomplete functionality
    function initCityAutoComplete() {
        const input = document.getElementById('cityInput');
        const suggestionsDiv = document.getElementById('suggestions');

        if (!input || !suggestionsDiv) return;

        input.addEventListener('input', function() {
            const query = this.value.toLowerCase().trim();
            suggestionsDiv.innerHTML = '';

            if (!query) {
                suggestionsDiv.classList.add('hidden');
                return;
            }

            const filtered = cities.filter(city => 
                city.toLowerCase().startsWith(query)
            ).slice(0, 8); // Limit to 8 suggestions for better UX

            if (filtered.length === 0) {
                suggestionsDiv.classList.add('hidden');
                return;
            }

            suggestionsDiv.classList.remove('hidden');

            filtered.forEach(city => {
                const div = document.createElement('div');
                div.className = "px-4 py-2 cursor-pointer hover:bg-blue-100 hover:text-blue-800 transition-colors rounded-lg";
                div.textContent = city;
                div.addEventListener('click', () => {
                    input.value = city;
                    suggestionsDiv.innerHTML = '';
                    suggestionsDiv.classList.add('hidden');
                });
                suggestionsDiv.appendChild(div);
            });
        });

        // Validate city on blur
        input.addEventListener('blur', function() {
            setTimeout(() => { // Delay to allow click events on suggestions
                if (this.value && !cities.includes(this.value)) {
                    showNotification('Please select a valid city from the list', 'warning');
                    this.value = '';
                }
                suggestionsDiv.classList.add('hidden');
            }, 150);
        });

        // Handle keyboard navigation
        input.addEventListener('keydown', function(e) {
            const suggestions = suggestionsDiv.querySelectorAll('div');
            const current = suggestionsDiv.querySelector('.bg-blue-100');
            let index = Array.from(suggestions).indexOf(current);

            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    index = Math.min(index + 1, suggestions.length - 1);
                    updateSelection(suggestions, index);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    index = Math.max(index - 1, 0);
                    updateSelection(suggestions, index);
                    break;
                case 'Enter':
                    if (current) {
                        e.preventDefault();
                        current.click();
                    }
                    break;
                case 'Escape':
                    suggestionsDiv.classList.add('hidden');
                    break;
            }
        });

        // Close suggestions when clicking outside
        document.addEventListener('click', e => {
            if (!input.contains(e.target) && !suggestionsDiv.contains(e.target)) {
                suggestionsDiv.classList.add('hidden');
            }
        });
    }

    // Update keyboard selection for autocomplete
    function updateSelection(suggestions, index) {
        suggestions.forEach((s, i) => {
            s.classList.toggle('bg-blue-100', i === index);
        });
    }

    // Form validation with improved UX
    function initFormValidation() {
        const form = document.querySelector('form');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
            let hasErrors = false;
            let firstError = null;

            requiredFields.forEach(field => {
                const value = field.value.trim();
                const isValid = field.type === 'email' ? isValidEmail(value) : !!value;

                if (!isValid) {
                    field.classList.add('field-error', 'border-red-300');
                    hasErrors = true;
                    
                    if (!firstError) firstError = field;
                    
                    setTimeout(() => {
                        field.classList.remove('field-error');
                    }, 500);
                } else {
                    field.classList.remove('border-red-300');
                }
            });

            if (hasErrors) {
                e.preventDefault();
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
                showNotification('Please fill in all required fields correctly', 'error');
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearErrors);
        });
    }

    // Field validation helper
    function validateField(e) {
        const field = e.target;
        if (!field.hasAttribute('required')) return;

        const value = field.value.trim();
        const isValid = field.type === 'email' ? isValidEmail(value) : !!value;

        field.classList.toggle('border-red-300', !isValid);
        field.classList.toggle('border-green-300', isValid && value);
    }

    // Clear field errors on input
    function clearErrors(e) {
        const field = e.target;
        field.classList.remove('border-red-300', 'field-error');
    }

    // Email validation helper
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Notification system
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existing = document.querySelector('.notification');
        if (existing) existing.remove();

        const notification = document.createElement('div');
        notification.className = `notification fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all duration-300 ${getNotificationClass(type)}`;
        notification.textContent = message;

        document.body.appendChild(notification);

        // Auto remove after 4 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => notification.remove(), 300);
            }
        }, 4000);

        // Click to dismiss
        notification.addEventListener('click', () => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => notification.remove(), 300);
        });
    }

    // Notification styling helper
    function getNotificationClass(type) {
        switch(type) {
            case 'success': return 'bg-green-500 text-white';
            case 'error': return 'bg-red-500 text-white';
            case 'warning': return 'bg-yellow-500 text-white';
            default: return 'bg-blue-500 text-white';
        }
    }
});