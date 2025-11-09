document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('id_category');
    const subcategorySelect = document.getElementById('id_subcategory');

    if (!categorySelect || !subcategorySelect) return;

    // store all subcategory options
    const allOptions = Array.from(subcategorySelect.options);

    function filterSubcategories() {
        const cat = categorySelect.value;

        // reset
        subcategorySelect.innerHTML = '';

        // map of allowed subcategories per category
        const map = {
            'accessories': ['handbags', 'sunglasses', 'watches', 'jewellery'],
            'men': ['men_shirts', 'men_jeans', 'men_jackets', 'men_shoes'],
            'women': ['women_dresses', 'women_tops', 'women_jeans', 'women_sarees'],
            'kids': ['kids_tshirts', 'kids_pants', 'kids_shoes', 'kids_toys']
        };

        const allowed = map[cat] || [];
        allOptions.forEach(opt => {
            if (allowed.includes(opt.value) || opt.value === '') {
                subcategorySelect.appendChild(opt);
            }
        });
    }

    categorySelect.addEventListener('change', filterSubcategories);
    filterSubcategories(); // run on load
});
