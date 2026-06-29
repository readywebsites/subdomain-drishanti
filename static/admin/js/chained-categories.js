document.addEventListener('DOMContentLoaded', function () {
    const categorySelect = document.getElementById('id_new_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    if (!categorySelect || !subcategorySelect) {
        return;
    }

    // Save the currently selected subcategory ID (if any)
    const initialSubcategoryId = subcategorySelect.value;

    // Store all subcategories by category ID
    let categoryMap = {};

    // Fetch categories and subcategories
    fetch('/api/categories/')
        .then(response => response.json())
        .then(data => {
            // Build the map
            data.forEach(category => {
                categoryMap[category.id] = category.subcategories || [];
            });

            // Update the subcategory dropdown based on selected category
            updateSubcategories(initialSubcategoryId);
        })
        .catch(error => {
            console.error('Error fetching categories for chained dropdown:', error);
        });

    categorySelect.addEventListener('change', function () {
        updateSubcategories();
    });

    function updateSubcategories(selectedId = null) {
        const categoryId = categorySelect.value;
        
        // Clear current choices
        subcategorySelect.innerHTML = '';

        if (!categoryId) {
            const opt = document.createElement('option');
            opt.value = '';
            opt.textContent = 'Select category first';
            subcategorySelect.appendChild(opt);

            // Trigger change events for Select2 UI compatibility
            subcategorySelect.dispatchEvent(new Event('change'));
            if (window.jQuery && window.jQuery(subcategorySelect).data('select2')) {
                window.jQuery(subcategorySelect).trigger('change');
            }
            return;
        }

        const subcategories = categoryMap[categoryId] || [];

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

        // Trigger change events for Select2 UI compatibility
        subcategorySelect.dispatchEvent(new Event('change'));
        if (window.jQuery && window.jQuery(subcategorySelect).data('select2')) {
            window.jQuery(subcategorySelect).trigger('change');
        }
    }
});
