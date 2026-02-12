document.addEventListener("DOMContentLoaded", function () {
  // --- Login / Logout UI state ---
  const loginForm = document.getElementById("login-form");
  const logoutButton = document.getElementById("logout-button");

  function checkLoginStatus() {
    if (localStorage.getItem("isLoggedIn") === "true") {
      document.body.classList.add("user-logged-in");
    } else {
      document.body.classList.remove("user-logged-in");
    }
  }

  if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
      e.preventDefault();
      localStorage.setItem("isLoggedIn", "true");
      const nextUrl = new URLSearchParams(window.location.search).get("next");
      window.location.href = nextUrl || "/";
    });
  }

  if (logoutButton) {
    logoutButton.addEventListener("click", function () {
      localStorage.removeItem("isLoggedIn");
      window.location.href = "/";
    });
  }

  checkLoginStatus();

  // --- HOME PAGE LOGIC ---
  const homePageContent = document.querySelector(".main-content-grid");
  if (homePageContent) {
    // Sort buttons (UI only, backend does sorting)
    const sortButtons = document.querySelectorAll(".sort-options .sort-button");
    sortButtons.forEach((button) => {
      button.addEventListener("click", function () {
        sortButtons.forEach((btn) => btn.classList.remove("active-sort"));
        this.classList.add("active-sort");
      });
    });

    // ❗ ПАГИНАЦИЯ — НИКАКОГО JS
    // Django сам всё делает через <a href>
  }

  // --- PRODUCT PAGE ---
  const productPageContent = document.querySelector(".page-product");
  if (productPageContent) {
    const accordionTitle = document.querySelector(".accordion-title");
    if (accordionTitle) {
      accordionTitle.addEventListener("click", function () {
        this.closest(".accordion-item").classList.toggle("active");
      });
    }
  }

  // --- ACCOUNT / ADMIN ---
  const accountAdminWrapper = document.querySelector(
    ".account-page-wrapper, .admin-page-wrapper"
  );
  if (accountAdminWrapper) {
    const accountTabs = document.querySelectorAll(".account-tab");
    const tabPanes = document.querySelectorAll(".tab-pane");

    accountTabs.forEach((tab) => {
      tab.addEventListener("click", function () {
        accountTabs.forEach((t) => t.classList.remove("active"));
        tabPanes.forEach((p) => p.classList.remove("active"));

        tab.classList.add("active");
        const pane = document.querySelector(tab.dataset.tabTarget);
        if (pane) pane.classList.add("active");
      });
    });
  }
});
