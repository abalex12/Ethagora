document.addEventListener("DOMContentLoaded", () => {
    let selectedCategory = window.LISTING_CONTEXT?.selectedCategory || "";
    let selectedSubcategory = window.LISTING_CONTEXT?.selectedSubcategory || "";

    // --- DOM helpers ---
    const $ = (id) => document.getElementById(id);

    // --- Filter toggle ---
    const filterToggle = $("filter-toggle");
    if (filterToggle) {
        filterToggle.addEventListener("click", () => {
            $("filters-section")?.classList.toggle("hidden");
        });
    }

    // --- Category buttons ---
    document.querySelectorAll(".category-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            selectedCategory = btn.dataset.category;
            selectedSubcategory = "";

            // Reset all
            document.querySelectorAll(".category-btn").forEach((b) =>
                b.classList.remove("active")
            );

            btn.classList.add("active");

            loadSubcategories(selectedCategory);
            updateActiveFilters();
            applyFilters();
        });
    });

    // --- Subcategory loader ---
    function loadSubcategories(categoryId) {
        const container = $("subcategory-chips");
        const section = $("subcategory-section");
        if (!container || !section) return;

        container.innerHTML = "";

        if (!categoryId) {
            section.classList.add("hidden");
            return;
        }

        section.classList.remove("hidden");

        container.innerHTML =
            '<div class="flex items-center space-x-2"><div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-400"></div><span class="text-xs text-gray-500">Loading...</span></div>';

        fetch(`/api/subcategories/?category_id=${categoryId}`)
            .then((res) => res.json())
            .then((data) => {
                container.innerHTML = "";
                data.forEach((sub) => {
                    const chip = document.createElement("button");
                    chip.type = "button";
                    chip.className = `subcategory-chip flex-shrink-0 flex items-center px-3 py-2 
                        rounded-xl border shadow-sm transition-all duration-200
                        ${
                            selectedSubcategory == sub.id
                                ? "bg-blue-500 text-white border-blue-500 shadow-md scale-105"
                                : "bg-white text-gray-700 border-gray-200 hover:bg-gray-50"
                        }`;

                    chip.innerHTML = `
                        <div class="flex items-center space-x-2">
                            <div class="w-7 h-7 flex items-center justify-center rounded-lg bg-gray-100 text-gray-500 
                                        transition-all group-hover:bg-blue-100 group-hover:text-blue-600">
                                <i class="fa-solid fa-${sub.icon}"></i>
                            </div>
                            <span class="text-sm font-medium">${sub.name}</span>
                        </div>
                    `;

                    chip.addEventListener("click", () => {
                        selectedSubcategory =
                            selectedSubcategory == sub.id ? "" : sub.id;
                        loadSubcategories(categoryId);
                        updateActiveFilters();
                        applyFilters();
                    });
                    container.appendChild(chip);
                });
            })
            .catch((error) => {
                console.error("Error loading subcategories:", error);
                container.innerHTML =
                    '<span class="text-xs text-red-500">Failed to load subcategories</span>';
            });
    }

    // --- Clear subcategory ---
    $("subcategory-clear")?.addEventListener("click", () => {
        selectedSubcategory = "";
        loadSubcategories(selectedCategory);
        updateActiveFilters();
        applyFilters();
    });

    // --- Filter form ---
    const filterForm = $("filter-form");
    if (filterForm) {
        filterForm.addEventListener("input", () => {
            updateActiveFilters();
            clearTimeout(window.filterTimeout);
            window.filterTimeout = setTimeout(applyFilters, 300);
        });
    }

    // --- Clear filters ---
    $("clear-filters")?.addEventListener("click", () => {
        if (!filterForm) return;
        const inputs = filterForm.querySelectorAll(
            "input[type='text'], input[type='number'], select"
        );
        inputs.forEach((input) => {
            if (input.name !== "search") {
                input.value = "";
            }
        });

        updateActiveFilters();
        applyFilters();
    });

    // --- Active filters display ---
    function updateActiveFilters() {
        const container = $("active-filters");
        if (!container || !filterForm) return;

        const formData = new FormData(filterForm);
        container.innerHTML = "";
        const filters = [];

        if (formData.get("condition"))
            filters.push(`Condition: ${formData.get("condition")}`);
        if (formData.get("min_price"))
            filters.push(`Min: $${formData.get("min_price")}`);
        if (formData.get("max_price"))
            filters.push(`Max: $${formData.get("max_price")}`);

        if (selectedCategory) {
            const categoryBtn = document.querySelector(
                `[data-category="${selectedCategory}"]`
            );
            if (categoryBtn) {
                const name = categoryBtn.querySelector("span")?.textContent;
                if (name) filters.push(`Category: ${name}`);
            }
        }

        filters.forEach((filter) => {
            const badge = document.createElement("span");
            badge.className = "filter-badge";
            badge.textContent = filter;
            container.appendChild(badge);
        });
    }

    // --- Apply filters ---
    function applyFilters() {
        if (!filterForm) return;

        const formData = new FormData(filterForm);
        if (selectedCategory) formData.set("category", selectedCategory);
        if (selectedSubcategory) formData.set("subcategory", selectedSubcategory);

        const params = new URLSearchParams(formData);
        const listingsContainer = $("listings-container");
        if (!listingsContainer) return;

        listingsContainer.classList.add("loading");
        listingsContainer.innerHTML = `
            <div class="flex items-center justify-center py-20">
                <div class="flex flex-col items-center space-y-3">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
                    <p class="text-sm text-gray-500">Loading products...</p>
                </div>
            </div>
        `;

        fetch(`/api/filter-listings/?${params}`)
            .then((res) => res.json())
            .then((data) => {
                listingsContainer.innerHTML = data.listings_html;
                listingsContainer.classList.remove("loading");

                const url = new URL(window.location);
                url.search = params.toString();
                window.history.replaceState({}, "", url);
            })
            .catch((error) => {
                console.error("Error filtering listings:", error);
                listingsContainer.classList.remove("loading");
                listingsContainer.innerHTML = `
                    <div class="text-center py-20">
                        <div class="text-gray-400 text-4xl mb-4">⚠️</div>
                        <h3 class="text-lg font-semibold text-gray-900 mb-2">Unable to load products</h3>
                        <p class="text-gray-500 mb-4">Please check your connection and try again</p>
                        <button onclick="location.reload()" class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                            Retry
                        </button>
                    </div>
                `;
            });
    }

    // --- Init on load ---
    if (selectedCategory) {
        loadSubcategories(selectedCategory);
        document.querySelectorAll(".category-btn").forEach((btn) => {
            if (btn.dataset.category === selectedCategory) {
                btn.classList.add("active");
            }
        });
    }
    updateActiveFilters();

    // --- Category scroll touch ---
    const categoriesContainer = $("categories-container");
    if (categoriesContainer) {
        let isScrolling = false;
        categoriesContainer.addEventListener("touchstart", () => {
            isScrolling = true;
        });
        categoriesContainer.addEventListener("touchend", () => {
            setTimeout(() => {
                isScrolling = false;
            }, 100);
        });
    }
});
