(function() {
    function initChainedCategories() {
        const categorySelect = document.getElementById('id_new_category');
        const subcategorySelect = document.getElementById('id_subcategory');

        if (!categorySelect || !subcategorySelect) {
            return;
        }

        const initialSubcategoryId = subcategorySelect.value;
        let categoryMap = {};
        let isCategoriesFetched = false;

        // Fetch categories and subcategories
        const fetchUrl = '/api/categories/';

        fetch(fetchUrl)
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
                
                // Build the map
                data.forEach(category => {
                    categoryMap[category.id] = category.subcategories || [];
                });

                isCategoriesFetched = true;
                updateSubcategories(initialSubcategoryId);
            })
            .catch(error => {
                console.error('Error fetching categories for chained dropdown:', error);
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = 'Error: ' + error.message;
                subcategorySelect.innerHTML = '';
                subcategorySelect.appendChild(opt);
                triggerChange(subcategorySelect);
            });

        // Helper to trigger change on ALL jQuery instances + native DOM + Select2 re-init
        function triggerChange(element) {
            element.dispatchEvent(new Event('change', { bubbles: true }));
            
            if (window.django && window.django.jQuery) {
                const $el = window.django.jQuery(element);
                if ($el.data('select2')) {
                    $el.select2('destroy');
                    $el.select2({ width: 'element' });
                }
                window.django.jQuery(element).trigger('change');
            }
            if (window.jQuery) {
                const $el = window.jQuery(element);
                if ($el.data('select2') && (!window.django || $el.data('select2') !== window.django.jQuery(element).data('select2'))) {
                    $el.select2('destroy');
                    $el.select2({ width: 'element' });
                }
                window.jQuery(element).trigger('change');
            }
        }

        // Bind change listener on ALL jQuery instances + native DOM
        categorySelect.addEventListener('change', function () {
            if (isCategoriesFetched) {
                updateSubcategories();
            }
        });

        if (window.django && window.django.jQuery) {
            window.django.jQuery(categorySelect).on('change', function() {
                if (isCategoriesFetched) {
                    updateSubcategories();
                }
            });
        }

        if (window.jQuery) {
            window.jQuery(categorySelect).on('change', function() {
                if (isCategoriesFetched) {
                    updateSubcategories();
                }
            });
        }

        if (window.$ && window.$ !== window.jQuery && (!window.django || window.$ !== window.django.jQuery)) {
            window.$(categorySelect).on('change', function() {
                if (isCategoriesFetched) {
                    updateSubcategories();
                }
            });
        }

        function updateSubcategories(selectedId = null) {
            const categoryId = categorySelect.value;
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
