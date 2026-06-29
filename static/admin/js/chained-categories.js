(function() {
    function initChainedCategories() {
        console.log('Chained categories: Script initialized.');
        
        const categorySelect = document.getElementById('id_new_category');
        const subcategorySelect = document.getElementById('id_subcategory');

        if (!categorySelect || !subcategorySelect) {
            console.warn('Chained categories: Select elements not found.');
            return;
        }

        // Save the currently selected subcategory ID (if any)
        const initialSubcategoryId = subcategorySelect.value;

        // Store all subcategories by category ID
        let categoryMap = {};

        function displayError(message) {
            const opt = document.createElement('option');
            opt.value = '';
            opt.textContent = 'Error: ' + message;
            subcategorySelect.innerHTML = '';
            subcategorySelect.appendChild(opt);
            triggerChange(subcategorySelect);
        }

        // Fetch categories and subcategories
        fetch('/api/categories/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('HTTP status ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (!Array.isArray(data)) {
                    throw new Error('Invalid API response format');
                }
                console.log('Chained categories: Categories fetched successfully', data);
                
                // Build the map
                data.forEach(category => {
                    categoryMap[category.id] = category.subcategories || [];
                });

                // Update the subcategory dropdown based on selected category
                updateSubcategories(initialSubcategoryId);
            })
            .catch(error => {
                console.error('Error fetching categories for chained dropdown:', error);
                displayError(error.message);
            });

        // Helper to trigger change on ALL jQuery instances + native DOM + Select2 re-init
        function triggerChange(element) {
            // 1. Native DOM event
            element.dispatchEvent(new Event('change', { bubbles: true }));
            
            // 2. Destroy and re-initialize Select2 if it exists
            const $ = window.django ? django.jQuery : (window.jQuery || window.$);
            if ($) {
                const $el = $(element);
                if ($el.data('select2')) {
                    console.log('Chained categories: Re-initializing Select2 for', element.id);
                    $el.select2('destroy');
                    $el.select2({
                        width: 'element'
                    });
                }
                $el.trigger('change');
            }
        }

        // Bind change listener on ALL jQuery instances + native DOM
        categorySelect.addEventListener('change', function () {
            console.log('Chained categories: native change event fired on new_category');
            updateSubcategories();
        });

        const $ = window.django ? django.jQuery : (window.jQuery || window.$);
        if ($) {
            $(categorySelect).on('change', function() {
                console.log('Chained categories: jQuery change event fired on new_category');
                updateSubcategories();
            });
        }

        function updateSubcategories(selectedId = null) {
            const categoryId = categorySelect.value;
            console.log('Chained categories: Updating subcategories for category ID:', categoryId);
            
            // Clear current choices
            subcategorySelect.innerHTML = '';

            if (!categoryId) {
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = 'Select category first';
                subcategorySelect.appendChild(opt);

                triggerChange(subcategorySelect);
                return;
            }

            const subcategories = categoryMap[categoryId] || [];
            console.log('Chained categories: Found subcategories:', subcategories);

            // Django default empty option
            const emptyOpt = document.createElement('option');
            emptyOpt.value = '';
            emptyOpt.textContent = '---------';
            subcategorySelect.appendChild(emptyOpt);

            subcategories.forEach(sub => {
                const opt = document.createElement('option');
                opt.value = sub.id;
                opt.textContent = sub.name;
                if (selectedId && String(sub.id) === String(selectedId)) {
                    opt.selected = true;
                }
                subcategorySelect.appendChild(opt);
            });

            triggerChange(subcategorySelect);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChainedCategories);
    } else {
        initChainedCategories();
    }
})();
