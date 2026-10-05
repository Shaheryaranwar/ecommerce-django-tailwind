/* Aangan Living — wishlist.js */
(function () {
  "use strict";

  function csrfToken() {
    return window.getCookie ? window.getCookie("csrftoken") : "";
  }

  function updateCount(count) {
    const badge = document.getElementById("wishlist-count");
    if (!badge) return;
    badge.textContent = count;
    badge.classList.toggle("hidden", count === 0);
  }

  document.addEventListener("submit", async (e) => {
    const form = e.target.closest("[data-wishlist-toggle]");
    if (!form) return;
    e.preventDefault();

    try {
      const res = await fetch(form.action, {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken(), "X-Requested-With": "XMLHttpRequest" },
      });
      const data = await res.json();
      if (!data.success) return;

      updateCount(data.count);
      const icon = form.querySelector("i[data-lucide=heart]");
      if (icon) {
        icon.classList.toggle("fill-clay", data.added);
        icon.classList.toggle("text-clay", data.added);
      }
      const label = form.querySelector("[data-wishlist-label]");
      if (label) {
        label.textContent = data.added ? "Saved to wishlist" : "Save to wishlist";
      }
      window.showToast(data.added ? "Saved to your wishlist." : "Removed from your wishlist.");

      const onWishlistPage = document.body.dataset.page === "wishlist";
      if (onWishlistPage && !data.added) {
        const card = form.closest(".group.relative");
        if (card) {
          card.style.transition = "opacity .3s ease";
          card.style.opacity = "0";
          setTimeout(() => {
            card.remove();
            const remaining = document.querySelectorAll("[data-wishlist-toggle]").length;
            if (remaining === 0) window.location.reload();
          }, 300);
        }
      }
    } catch (err) {
      window.showToast("Something went wrong. Please try again.", "error");
    }
  });
})();
