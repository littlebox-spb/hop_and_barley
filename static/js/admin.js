document.addEventListener("DOMContentLoaded", () => {
  const showToast = (message, type = "success") => {
  const toast = document.getElementById("toast");
  if (!toast) return;

  toast.textContent = message;
  toast.className = `toast toast--show toast--${type}`;

  // Скрываем через 3 секунды
  setTimeout(() => {
    toast.className = "toast";
  }, 3000);
};

  const csrf = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  )?.value;

  /* ================================
     CATEGORIES (ADMIN, NOT PRODUCT)
     ================================ */

  const categorySelect = document.getElementById("category-select"); // слева
  const categoryInput = document.getElementById("category-input");
  const addBtn = document.getElementById("category-add-btn");
  const delBtn = document.getElementById("category-del-btn");

  const productCategorySelect =
    document.querySelector('select[name="category"]'); // справа

  if (addBtn && categoryInput && categorySelect) {
    addBtn.addEventListener("click", () => {
      const name = categoryInput.value.trim();
      if (!name) return;

      fetch(addBtn.dataset.addUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf,
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify({ name }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.error) {
            showToast(data.error, "danger");
            return;
          }

          // ⬅ левый select
          const optLeft = document.createElement("option");
          optLeft.value = data.id;
          optLeft.textContent = data.name;
          categorySelect.appendChild(optLeft);
          categorySelect.value = data.id;

          // ➡ правый select (product.category)
          if (productCategorySelect) {
            const optRight = document.createElement("option");
            optRight.value = data.id;
            optRight.textContent = data.name;
            productCategorySelect.appendChild(optRight);
          }

          categoryInput.value = "";
        })
        .catch(err => {
          console.error(err);
          showToast("Category add failed", "danger");
        });
    });
  }

  if (delBtn && categorySelect) {
    delBtn.addEventListener("click", () => {
      const id = categorySelect.value;
      if (!id) {
        showToast("Select category", "danger");
        return;
      }

      const url = delBtn.dataset.delUrlTemplate.replace("0", id);

      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf,
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then(res => res.json())
        .then(data => {
          if (data.error) {
            showToast(data.error, "danger");
            return;
          }

          // ❌ удалить из левого
          categorySelect
            .querySelector(`option[value="${id}"]`)
            ?.remove();

          // ❌ удалить из правого
          productCategorySelect
            ?.querySelector(`option[value="${id}"]`)
            ?.remove();

          categorySelect.value = "";
        })
        .catch(err => {
          console.error(err);
          showToast("Category delete failed", "danger");
        });
    });
  }

  /* ================================
     IMAGE UPLOAD (НЕ ТРОГАЕМ)
     ================================ */

  const imageInput = document.getElementById("image-input");
  const imagePlaceholder = document.getElementById("image-placeholder");

  if (imageInput && imagePlaceholder) {
    imagePlaceholder.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      imageInput.click();
    });

    imageInput.addEventListener("change", () => {
      const file = imageInput.files[0];
      if (!file) return;

      if (!["image/jpeg", "image/jpg"].includes(file.type)) {
        showToast("Only JPG / JPEG allowed", "danger");
        imageInput.value = "";
        return;
      }

      if (file.size > 2 * 1024 * 1024) {
        showToast("Image must be less than 2MB", "danger");
        imageInput.value = "";
        return;
      }

      const reader = new FileReader();
      reader.onload = () => {
        imagePlaceholder.innerHTML = "";
        const img = document.createElement("img");
        img.src = reader.result;
        img.style.width = "100%";
        img.style.borderRadius = "8px";
        img.style.pointerEvents = "none";
        imagePlaceholder.appendChild(img);
      };

      reader.readAsDataURL(file);
    });
  }
});
