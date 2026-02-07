document.addEventListener("DOMContentLoaded", () => {

  const csrftoken = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  )?.value;

  /* ---------- ADD CATEGORY ---------- */
  const addBtn = document.getElementById("add-category-btn");
  const input = document.getElementById("new-category-name");
  const list = document.getElementById("category-list");

  if (addBtn && input && list) {
    addBtn.addEventListener("click", () => {
      const name = input.value.trim();
      if (!name) return;

      fetch(addBtn.dataset.addUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "X-Requested-With": "XMLHttpRequest",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name }),
      })
        .then(res => res.json())
        .then(data => {
          if (data.error) {
            alert(data.error);
            return;
          }

          const btn = document.createElement("button");
          btn.type = "button";
          btn.className = "category-tag removable";
          btn.dataset.deleteUrl = data.delete_url;
          btn.innerHTML = `${data.name} <span class="remove-x">✕</span>`;

          list.appendChild(btn);
          input.value = "";
        });
    });
  }

  /* ---------- DELETE CATEGORY ---------- */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".category-tag.removable");
    if (!btn) return;

    const url = btn.dataset.deleteUrl;
    if (!confirm("Delete this category?")) return;

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          btn.remove();
        }
      });
  });

});

/* ---------- IMAGE UPLOAD ---------- */
document.addEventListener("DOMContentLoaded", () => {
  const card = document.getElementById("image-card");
  const input = document.getElementById("image-input");
  const placeholder = document.getElementById("image-placeholder");

  if (!card || !input || !placeholder) return;

  // Клик по карточке → открыть диалог
  card.addEventListener("click", () => input.click());

  input.addEventListener("change", () => {
    const file = input.files[0];
    if (!file) return;

    // 🔒 ВАЛИДАЦИЯ
    if (!["image/jpeg", "image/jpg"].includes(file.type)) {
      alert("Only JPG / JPEG allowed");
      input.value = "";
      return;
    }

    if (file.size > 2 * 1024 * 1024) {
      alert("Image must be less than 2MB");
      input.value = "";
      return;
    }

    // 👁 PREVIEW
    const reader = new FileReader();
    reader.onload = () => {
      placeholder.innerHTML = "";
      const img = document.createElement("img");
      img.src = reader.result;
      img.style.width = "100%";
      img.style.borderRadius = "8px";
      placeholder.appendChild(img);
    };

    reader.readAsDataURL(file);
  });
});

// KATEGORIES

document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("category-select");
  const input = document.getElementById("category-input");
  const addBtn = document.getElementById("category-add-btn");
  const delBtn = document.getElementById("category-del-btn");

  const csrf = document.querySelector(
    'input[name="csrfmiddlewaretoken"]'
  ).value;

  // ➕ ADD
  addBtn.addEventListener("click", () => {
    const name = input.value.trim();
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
        if (data.error) return alert(data.error);
        location.reload();
      });
  });

  // ❌ DELETE
  delBtn.addEventListener("click", () => {
    const id = select.value;
    if (!id) return alert("Select category");

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
        if (data.error) alert(data.error);
        else location.reload();
      });
  });
});
