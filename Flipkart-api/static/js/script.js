// Add event listener to filter form
document.querySelector(".filter-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const category = document.getElementById("category").value;
    const priceMin = document.getElementById("price_min").value;
    const priceMax = document.getElementById("price_max").value;
    fetch(`/products/filter?category=${category}&price_min=${priceMin}&price_max=${priceMax}`)
        .then(response => response.json())
        .then(data => {
            const productList = document.querySelector(".product-list");
            productList.innerHTML = "";
            data.forEach(product => {
                const productListItem = document.createElement("li");
                productListItem.textContent = `${product.name} - ${product.price}`;
                productList.appendChild(productListItem);
            });
        });
});

// Add event listener to order filter form
document.querySelector(".order-filter-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const status = document.getElementById("status").value;
    const dateFrom = document.getElementById("date_from").value;
    const dateTo = document.getElementById("date_to").value;
    fetch(`/orders/filter?status=${status}&date_from=${dateFrom}&date_to=${dateTo}`)
        .then(response => response.json())
        .then(data => {
            const orderList = document.querySelector(".order-list");
            orderList.innerHTML = "";
            data.forEach(order => {
                const orderListItem = document.createElement("li");
                orderListItem.textContent = `Order ID: ${order.order_id} - Status: ${order.status}`;
                orderList.appendChild(orderListItem);
            });
        });
});