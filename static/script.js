let editingProductId = null;


// Load products when page opens
document.addEventListener("DOMContentLoaded", () => {
    loadProducts();
    loadStats();
});


// Load products
async function loadProducts(search = "") {

    try {

        let url = "/api/products";

        if (search.trim() !== "") {
            url += "?search=" + encodeURIComponent(search);
        }

        const response = await fetch(url);

        const products = await response.json();

        displayProducts(products);

    } catch (error) {

        showToast("Unable to load products.");

        console.error(error);
    }
}


// Display products in table
function displayProducts(products) {

    const tableBody = document.getElementById("productTableBody");
    const emptyState = document.getElementById("emptyState");

    tableBody.innerHTML = "";

    if (products.length === 0) {

        emptyState.style.display = "block";

        return;

    }

    emptyState.style.display = "none";


    products.forEach(product => {

        let status = "";
        let statusClass = "";

        if (product.quantity === 0) {

            status = "Out of Stock";
            statusClass = "out-stock";

        } else if (product.quantity < 10) {

            status = "Low Stock";
            statusClass = "low-stock";

        } else {

            status = "In Stock";
            statusClass = "in-stock";

        }


        const row = document.createElement("tr");

        row.innerHTML = `

            <td>
                <span class="product-id">
                    ${escapeHtml(product.product_id)}
                </span>
            </td>

            <td>
                <strong>
                    ${escapeHtml(product.name)}
                </strong>
            </td>

            <td>
                ${escapeHtml(product.category)}
            </td>

            <td>
                ${product.quantity}
            </td>

            <td>
                ₹${Number(product.price).toLocaleString(
                    "en-IN",
                    {
                        minimumFractionDigits: 2
                    }
                )}
            </td>

            <td>
                <span class="status ${statusClass}">
                    ${status}
                </span>
            </td>

            <td>

                <button
                    class="action-btn edit-btn"
                    title="Edit"
                    onclick='editProduct(${JSON.stringify(product)})'
                >
                    ✏️
                </button>

                <button
                    class="action-btn delete-btn"
                    title="Delete"
                    onclick="deleteProduct(${product.id})"
                >
                    🗑️
                </button>

            </td>

        `;

        tableBody.appendChild(row);

    });
}


// Load dashboard statistics
async function loadStats() {

    try {

        const response = await fetch("/api/stats");

        const stats = await response.json();


        document.getElementById("totalProducts").textContent =
            stats.total_products;

        document.getElementById("totalStock").textContent =
            stats.total_stock;

        document.getElementById("lowStock").textContent =
            stats.low_stock;

        document.getElementById("inventoryValue").textContent =
            "₹" + Number(stats.inventory_value).toLocaleString(
                "en-IN",
                {
                    maximumFractionDigits: 2
                }
            );

    } catch (error) {

        console.error(error);

    }
}


// Search
function searchProducts() {

    const search = document.getElementById("searchInput").value;

    loadProducts(search);

}


// Open Add modal
function openAddModal() {

    editingProductId = null;

    document.getElementById("modalTitle").textContent =
        "Add Product";

    document.getElementById("productForm").reset();

    document.getElementById("editId").value = "";

    document.getElementById("productModal")
        .classList.add("active");

}


// Open Edit modal
function editProduct(product) {

    editingProductId = product.id;

    document.getElementById("modalTitle").textContent =
        "Edit Product";

    document.getElementById("editId").value =
        product.id;

    document.getElementById("productId").value =
        product.product_id;

    document.getElementById("productName").value =
        product.name;

    document.getElementById("category").value =
        product.category;

    document.getElementById("quantity").value =
        product.quantity;

    document.getElementById("price").value =
        product.price;

    document.getElementById("productModal")
        .classList.add("active");

}


// Close modal
function closeModal() {

    document.getElementById("productModal")
        .classList.remove("active");

}


// Form submission
document.getElementById("productForm")
    .addEventListener("submit", async function(event) {

        event.preventDefault();


        const product = {

            product_id:
                document.getElementById("productId").value.trim(),

            name:
                document.getElementById("productName").value.trim(),

            category:
                document.getElementById("category").value.trim(),

            quantity:
                Number(document.getElementById("quantity").value),

            price:
                Number(document.getElementById("price").value)

        };


        if (
            !product.product_id ||
            !product.name ||
            !product.category
        ) {

            showToast("Please fill all required fields.");

            return;

        }


        if (
            product.quantity < 0 ||
            product.price < 0
        ) {

            showToast("Quantity and price cannot be negative.");

            return;

        }


        try {

            let response;


            if (editingProductId) {

                response = await fetch(
                    `/api/products/${editingProductId}`,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify(product)
                    }
                );

            } else {

                response = await fetch(
                    "/api/products",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify(product)
                    }
                );

            }


            const result = await response.json();


            if (!response.ok) {

                showToast(result.error || "Something went wrong.");

                return;

            }


            showToast(result.message);

            closeModal();

            loadProducts();

            loadStats();


        } catch (error) {

            showToast("Server error. Please try again.");

            console.error(error);

        }

    });


// Delete product
async function deleteProduct(id) {

    const confirmed = confirm(
        "Are you sure you want to delete this product?"
    );

    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `/api/products/${id}`,
            {
                method: "DELETE"
            }
        );


        const result = await response.json();


        if (!response.ok) {

            showToast(result.error);

            return;

        }


        showToast(result.message);

        loadProducts();

        loadStats();


    } catch (error) {

        showToast("Unable to delete product.");

        console.error(error);

    }

}


// Scroll to products
function scrollToProducts() {

    document.getElementById("products")
        .scrollIntoView({
            behavior: "smooth"
        });

}


// Toast notification
function showToast(message) {

    const toast = document.getElementById("toast");

    toast.textContent = message;

    toast.classList.add("show");


    setTimeout(() => {

        toast.classList.remove("show");

    }, 3000);

}


// Basic HTML escaping
function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}
