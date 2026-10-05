/* Aangan Living — cart.js (AJAX cart) */
(function () {
  "use strict";

  function csrfToken() {
    return window.getCookie ? window.getCookie("csrftoken") : "";
  }

  function formatPKR(value) {
    return "Rs " + Number(value).toLocaleString("en-PK", { maximumFractionDigits: 0 });
  }

  function updateBadges(payload) {
    if (!payload) return;
    const count = document.getElementById("cart-count");
    if (count) {
      count.textContent = payload.count;
      count.classList.toggle("hidden", payload.count === 0);
    }
  }

  async function postForm(form) {
    const res = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken(),
        "X-Requested-With": "XMLHttpRequest",
      },
      body: new FormData(form),
    });
    return res.json();
  }

  /* ---------- add to cart (product cards + detail page) ---------- */
  document.addEventListener("submit", async (e) => {
    const form = e.target.closest("[data-add-to-cart]");
    if (!form) return;
    e.preventDefault();

    const btn = form.querySelector("button[type=submit]:focus") || e.submitter;
    const isBuyNow = btn && btn.id === "buy-now-btn";

    const detailForm = form.closest("[data-product-form]");
    if (detailForm) {
      const selected = detailForm.querySelector("input[name=variant]:checked");
      if (selected) form.action = form.action.replace(/\/\d+\/$/, `/${selected.value}/`);
      const qtyInput = document.getElementById("qty-input");
      if (qtyInput) {
        let fd = new FormData(form);
        fd.set("quantity", qtyInput.value);
        const res = await fetch(form.action, {
          method: "POST",
          headers: { "X-CSRFToken": csrfToken(), "X-Requested-With": "XMLHttpRequest" },
          body: fd,
        });
        const data = await res.json();
        if (data.success) {
          updateBadges(data);
          window.showToast(data.message || "Added to your cart.");
          if (isBuyNow) window.location.href = "/checkout/";
        } else {
          window.showToast(data.message || "Could not add item.", "error");
        }
        return;
      }
    }

    try {
      const data = await postForm(form);
      if (data.success) {
        updateBadges(data);
        window.showToast(data.message || "Added to your cart.");
      } else {
        window.showToast(data.message || "Could not add item.", "error");
      }
    } catch (err) {
      window.showToast("Something went wrong. Please try again.", "error");
    }
  });

  /* ---------- cart page: quantity updates ---------- */
  const cartItems = document.getElementById("cart-items");
  if (cartItems) {
    const threshold = Number(cartItems.dataset.freeThreshold || 100000);
    const deliveryFee = Number(cartItems.dataset.deliveryFee || 1500);

    function refreshSummary(subtotal) {
      const subEl = document.getElementById("summary-subtotal");
      const delEl = document.getElementById("summary-delivery");
      const totalEl = document.getElementById("summary-total");
      if (subEl) subEl.textContent = formatPKR(subtotal);
      const free = subtotal >= threshold;
      if (totalEl) totalEl.textContent = formatPKR(free ? subtotal : subtotal + deliveryFee);
      if (delEl && !free) delEl.textContent = formatPKR(deliveryFee);
      const banner = document.getElementById("delivery-banner");
      if (banner) {
        if (free) {
          banner.innerHTML =
            '<p class="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.12em] text-moss">' +
            '<i data-lucide="circle-check" class="h-4 w-4"></i> You\'ve unlocked free delivery</p>';
        } else {
          const remaining = threshold - subtotal;
          banner.innerHTML =
            `<p class="text-xs text-cocoa">Add <strong>${formatPKR(remaining)}</strong> more for free delivery</p>` +
            `<div class="mt-2 h-1.5 w-full bg-linen"><div class="h-full bg-clay transition-all duration-500" style="width: ${Math.min(100, (subtotal / threshold) * 100)}%"></div></div>`;
        }
        if (window.lucide) window.lucide.createIcons(banner);
      }
    }

    document.addEventListener("cart:update", async (e) => {
      const { itemId, quantity } = e.detail;
      const line = document.querySelector(`.cart-line[data-item-id="${itemId}"]`);
      if (!line) return;
      try {
        const res = await fetch(`/cart/update/${itemId}/`, {
          method: "POST",
          headers: { "X-CSRFToken": csrfToken(), "X-Requested-With": "XMLHttpRequest" },
          body: new URLSearchParams({ quantity: String(quantity) }),
        });
        const data = await res.json();
        if (!data.success) return;
        line.querySelector(".qty-display").textContent = data.quantity;
        line.querySelector(".line-total").textContent = formatPKR(data.item_total);
        updateBadges(data);
        refreshSummary(data.subtotal);
      } catch (err) {
        window.showToast("Could not update the cart.", "error");
      }
    });

    document.addEventListener("submit", async (e) => {
      const form = e.target.closest("[data-cart-remove]");
      if (!form) return;
      e.preventDefault();
      const line = form.closest(".cart-line");
      try {
        const data = await postForm(form);
        if (!data.success) return;
        updateBadges(data);
        line.style.transition = "opacity .3s ease, transform .3s ease";
        line.style.opacity = "0";
        line.style.transform = "translateX(12px)";
        setTimeout(() => {
          line.remove();
          if (!document.querySelector(".cart-line")) {
            window.location.reload();
          }
        }, 300);
        refreshSummary(data.subtotal);
        window.showToast(data.message || "Item removed.");
      } catch (err) {
        window.showToast("Could not remove the item.", "error");
      }
    });
  }
})();
