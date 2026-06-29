(function() {
    let debugDiv = null;

    function logDebug(msg) {
        console.log(msg);
        if (!debugDiv) {
            debugDiv = document.getElementById('chained-debug-console');
            if (!debugDiv && document.body) {
                debugDiv = document.createElement('div');
                debugDiv.id = 'chained-debug-console';
                debugDiv.style.position = 'fixed';
                debugDiv.style.top = '60px';
                debugDiv.style.right = '20px';
                debugDiv.style.backgroundColor = 'rgba(0, 0, 0, 0.85)';
                debugDiv.style.color = '#00ff00';
                debugDiv.style.padding = '15px';
                debugDiv.style.borderRadius = '8px';
                debugDiv.style.zIndex = '999999';
                debugDiv.style.maxHeight = '300px';
                debugDiv.style.width = '350px';
                debugDiv.style.overflowY = 'auto';
                debugDiv.style.fontSize = '12px';
                debugDiv.style.fontFamily = 'monospace';
                debugDiv.style.boxShadow = '0 4px 15px rgba(0,0,0,0.5)';
                debugDiv.innerHTML = '<b>Category Dropdown Debug Console:</b><br><hr style="border-color:#555;">';
                document.body.appendChild(debugDiv);
            }
        }
        if (debugDiv) {
            const p = document.createElement('div');
            p.style.margin = '4px 0';
            p.style.borderBottom = '1px solid #333';
            p.style.paddingBottom = '4px';
            p.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
            debugDiv.appendChild(p);
            debugDiv.scrollTop = debugDiv.scrollHeight;
        }
    }

    function initChainedCategories() {
        logDebug('Script initChainedCategories started.');
        
        const categorySelect = document.getElementById('id_new_category');
        const subcategorySelect = document.getElementById('id_subcategory');

        if (!categorySelect) {
            logDebug('ERROR: Element id_new_category NOT found in DOM!');
        } else {
            logDebug('SUCCESS: Element id_new_category found.');
        }

        if (!subcategorySelect) {
            logDebug('ERROR: Element id_subcategory NOT found in DOM!');
        } else {
            logDebug('SUCCESS: Element id_subcategory found.');
        }

        if (!categorySelect || !subcategorySelect) {
            return;
        }

        const initialSubcategoryId = subcategorySelect.value;
        logDebug('Initial subcategory ID selected: ' + (initialSubcategoryId || 'None'));

        let categoryMap = {};
        let isCategoriesFetched = false;

        // Fetch categories and subcategories
        const fetchUrl = '/api/categories/';
        logDebug('Fetching categories from: ' + fetchUrl);

        fetch(fetchUrl)
            .then(response => {
                logDebug('Fetch response received. Status: ' + response.status);
                if (!response.ok) {
                    throw new Error('HTTP status ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (!Array.isArray(data)) {
                    throw new Error('Invalid API response format');
                }
                logDebug('Fetched ' + data.length + ' categories.');
                
                // Build the map
                data.forEach(category => {
                    categoryMap[category.id] = category.subcategories || [];
                    logDebug('Category: ' + category.name + ' (ID: ' + category.id + ') has ' + (category.subcategories ? category.subcategories.length : 0) + ' subcategories.');
                });

                isCategoriesFetched = true;
                updateSubcategories(initialSubcategoryId);
            })
            .catch(error => {
                logDebug('FETCH ERROR: ' + error.message);
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
                    logDebug('Re-initializing Select2 (django.jQuery) for: ' + element.id);
                    $el.select2('destroy');
                    $el.select2({ width: 'element' });
                }
                window.django.jQuery(element).trigger('change');
            }
            if (window.jQuery) {
                const $el = window.jQuery(element);
                if ($el.data('select2') && (!window.django || $el.data('select2') !== window.django.jQuery(element).data('select2'))) {
                    logDebug('Re-initializing Select2 (window.jQuery) for: ' + element.id);
                    $el.select2('destroy');
                    $el.select2({ width: 'element' });
                }
                window.jQuery(element).trigger('change');
            }
        }

        // Bind change listener on ALL jQuery instances + native DOM
        categorySelect.addEventListener('change', function () {
            logDebug('Native change event fired on new_category. Value chosen: ' + categorySelect.value);
            if (isCategoriesFetched) {
                updateSubcategories();
            } else {
                logDebug('Change ignored: Categories not fetched yet.');
            }
        });

        if (window.django && window.django.jQuery) {
            window.django.jQuery(categorySelect).on('change', function() {
                logDebug('django.jQuery change event fired on new_category. Value: ' + categorySelect.value);
                if (isCategoriesFetched) {
                    updateSubcategories();
                } else {
                    logDebug('django.jQuery change ignored: Categories not fetched yet.');
                }
            });
            logDebug('Bound django.jQuery change event listener.');
        }

        if (window.jQuery) {
            window.jQuery(categorySelect).on('change', function() {
                logDebug('window.jQuery change event fired on new_category. Value: ' + categorySelect.value);
                if (isCategoriesFetched) {
                    updateSubcategories();
                } else {
                    logDebug('window.jQuery change ignored: Categories not fetched yet.');
                }
            });
            logDebug('Bound window.jQuery change event listener.');
        }

        if (window.$ && window.$ !== window.jQuery && (!window.django || window.$ !== window.django.jQuery)) {
            window.$(categorySelect).on('change', function() {
                logDebug('window.$ change event fired on new_category. Value: ' + categorySelect.value);
                if (isCategoriesFetched) {
                    updateSubcategories();
                } else {
                    logDebug('window.$ change ignored: Categories not fetched yet.');
                }
            });
            logDebug('Bound window.$ change event listener.');
        }

        function updateSubcategories(selectedId = null) {
            const categoryId = categorySelect.value;
            logDebug('updateSubcategories called for Category ID: ' + (categoryId || 'None') + ', Selected Sub ID: ' + (selectedId || 'None'));
            
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
            logDebug('Found ' + subcategories.length + ' subcategories for this category.');

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
                    logDebug('Setting subcategory option to SELECTED: ' + sub.name + ' (ID: ' + sub.id + ')');
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
