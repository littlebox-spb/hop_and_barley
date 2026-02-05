// =====================================
// CSRF
// =====================================
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// =====================================
// GLOBAL CART STATE
// =====================================
const CartState = {
  items: {}, // { productId: quantity }
};

// =====================================
// UI HELPERS
// =====================================
function updateHeaderBadge(count) {
  const badge = document.getElementById("cart-badge");
  if (!badge) return;

  badge.textContent = count;
  badge.classList.toggle("is-hidden", count === 0);
}

function updateProductCard(productId, quantity) {
  const wrapper = document.querySelector(
    `.cart-controls[data-product-id="${productId}"]`,
  );
  if (!wrapper) return;

  const addBtn = wrapper.querySelector(".add-to-cart-button");
  const counter = wrapper.querySelector(".quantity-counter");
  const value = wrapper.querySelector(".quantity-value");

  if (quantity > 0) {
    addBtn.classList.add("is-hidden");
    counter.classList.remove("is-hidden");
    value.textContent = `${quantity} in cart`;
    value.dataset.qty = String(quantity);
  } else {
    addBtn.classList.remove("is-hidden");
    counter.classList.add("is-hidden");
    value.dataset.qty = "0";
  }
}

function syncFromResponse(data) {
  CartState.items[data.product_id] = data.quantity;
  updateHeaderBadge(data.cart_items_count);
  updateProductCard(data.product_id, data.quantity);
}

// =====================================
// MAIN
// =====================================
document.addEventListener("DOMContentLoaded", function () {
  const csrftoken = getCookie("csrftoken");

  // =====================================
  // 1. ADD TO CART
  // =====================================
  document.addEventListener("click", function (e) {
    const btn = e.target.closest(".add-to-cart-button");
    if (!btn || btn.dataset.loading === "true") return;

    const wrapper = btn.closest(".cart-controls");
    if (!wrapper) return;

    const productId = btn.dataset.productId;
    btn.dataset.loading = "true";

    fetch(`/cart/add/${productId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: new URLSearchParams({ quantity: 1 }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          syncFromResponse(data);
        }
      })
      .finally(() => {
        btn.dataset.loading = "false";
      });
  });

  // =====================================
  // 2. + / − НА КАРТОЧКЕ ТОВАРА
  // =====================================
  document.addEventListener("click", function (e) {
    const btn = e.target.closest(".quantity-btn");
    if (!btn || btn.dataset.loading === "true") return;

    const wrapper = btn.closest(".cart-controls");
    if (!wrapper) return;

    const productId = wrapper.dataset.productId;
    const valueEl = wrapper.querySelector(".quantity-value");

    let currentQty = parseInt(valueEl.dataset.qty, 10);
    if (isNaN(currentQty)) return;

    let newQty =
      btn.dataset.action === "increase" ? currentQty + 1 : currentQty - 1;

    if (newQty < 1) return;

    btn.dataset.loading = "true";

    fetch(`/cart/update/${productId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
      body: new URLSearchParams({ quantity: newQty }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "success") {
          syncFromResponse(data);
          valueEl.dataset.qty = data.quantity;
          valueEl.textContent = `${data.quantity} in cart`;
        } else {
          return;
        }
      })
      .finally(() => {
        btn.dataset.loading = "false";
      });
  });

  // =====================================
  // 3. CART PAGE (/cart/)
  // =====================================
  const cartList = document.getElementById("cart-items-list");

  if (cartList) {
    cartList.addEventListener("click", function (e) {
      const btn = e.target.closest("button");
      if (!btn) return;

      const productId = btn.dataset.productId;
      const action = btn.dataset.action;
      const itemRow = btn.closest(".cart-item");

      // REMOVE
      if (action === "remove") {
        fetch(`/cart/remove/${productId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((res) => res.json())
          .then((data) => {
            if (data.status !== "success") return;

            // 🔥 удаляем карточку товара из DOM
            itemRow.remove();

            // 🔢 обновляем бейдж
            updateHeaderBadge(data.cart_items_count);

            // 💰 обновляем total
            const totalEl = document.getElementById("cart-total-price");
            if (totalEl) {
              totalEl.textContent = `$${data.cart_total}`;
            }

            // 🧼 если корзина пуста — перезагружаем (один раз)
            if (data.cart_items_count === 0) {
              location.reload();
            }
          });
      }

      // + / -
      if (action === "increase" || action === "decrease") {
        const qtySpan = itemRow.querySelector(".quantity-value-cart");
        let currentQty = parseInt(qtySpan.textContent, 10);
        let newQty = action === "increase" ? currentQty + 1 : currentQty - 1;

        if (newQty < 1) return;

        fetch(`/cart/update/${productId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest",
          },
          body: new URLSearchParams({ quantity: newQty }),
        }).then(() => location.reload());
      }
    });
  }
});
