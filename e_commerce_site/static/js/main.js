/* Aangan Living — main.js */
(function () {
  "use strict";

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return "";
  }
  window.getCookie = getCookie;

  function refreshIcons(root) {
    if (window.lucide) window.lucide.createIcons(root || document);
  }

  /* ---------- toast system ---------- */
  window.showToast = function (message, type = "success") {
    const root = document.getElementById("toast-root");
    if (!root) return;
    const toast = document.createElement("div");
    toast.className =
      "toast-enter pointer-events-auto flex w-full max-w-md items-center gap-3 border bg-paper px-5 py-4 text-sm text-bark shadow-[0_20px_50px_-20px_rgba(38,32,26,0.35)] " +
      (type === "error" ? "border-red-200" : "border-linen");
    const icon =
      type === "error" ? "circle-alert" : type === "info" ? "info" : "circle-check";
    const iconColor = type === "error" ? "text-red-500" : type === "info" ? "text-clay" : "text-moss";
    toast.innerHTML =
      `<i data-lucide="${icon}" class="h-5 w-5 shrink-0 ${iconColor}"></i>` +
      `<span>${message}</span>` +
      `<button type="button" class="ml-auto text-stone transition-colors hover:text-bark" aria-label="Dismiss"><i data-lucide="x" class="h-4 w-4"></i></button>`;
    root.appendChild(toast);
    refreshIcons(toast);
    const remove = () => {
      toast.style.transition = "opacity .3s ease, transform .3s ease";
      toast.style.opacity = "0";
      toast.style.transform = "translateY(8px)";
      setTimeout(() => toast.remove(), 300);
    };
    toast.querySelector("button").addEventListener("click", remove);
    setTimeout(remove, 5000);
  };

  /* ---------- hero slider ---------- */
  const heroSlider = document.querySelector("[data-hero-slider]");
  if (heroSlider) {
    const slides = Array.from(heroSlider.querySelectorAll(".hero-slide"));
    const dots = Array.from(heroSlider.querySelectorAll(".hero-dot"));
    const prevBtn = heroSlider.querySelector(".hero-prev");
    const nextBtn = heroSlider.querySelector(".hero-next");
    let current = 0;
    let timer = null;
    const go = (i) => {
      current = (i + slides.length) % slides.length;
      slides.forEach((s, idx) => s.classList.toggle("opacity-0", idx !== current));
      dots.forEach((d, idx) => d.classList.toggle("is-active", idx === current));
    };
    const restart = () => {
      clearInterval(timer);
      timer = setInterval(() => go(current + 1), 6000);
    };
    if (nextBtn) nextBtn.addEventListener("click", () => { go(current + 1); restart(); });
    if (prevBtn) prevBtn.addEventListener("click", () => { go(current - 1); restart(); });
    dots.forEach((d, idx) => d.addEventListener("click", () => { go(idx); restart(); }));
    heroSlider.addEventListener("mouseenter", () => clearInterval(timer));
    heroSlider.addEventListener("mouseleave", restart);
    if (slides.length > 1) restart();
  }

  /* ---------- variant selection ---------- */
  function formatPKR(value) {
    const n = Number(value);
    if (Number.isNaN(n)) return "";
    return "Rs " + n.toLocaleString("en-PK", { maximumFractionDigits: 0 });
  }

  function applyVariant(target) {
    if (!target) return;
    const priceEl = document.getElementById("variant-price");
    const compareEl = document.getElementById("variant-compare-price");
    const nameEl = document.getElementById("variant-name");
    const stockEl = document.getElementById("stock-text");
    if (priceEl && target.dataset.price) priceEl.textContent = formatPKR(target.dataset.price);
    if (compareEl) {
      const cp = parseFloat(target.dataset.comparePrice || "0");
      const p = parseFloat(target.dataset.price || "0");
      if (cp > p) {
        compareEl.textContent = formatPKR(cp);
        compareEl.classList.remove("hidden");
      } else {
        compareEl.classList.add("hidden");
      }
    }
    if (nameEl) nameEl.textContent = target.dataset.name || "";
    if (stockEl) {
      const inStock = parseInt(target.dataset.stock || "0", 10) > 0;
      stockEl.classList.toggle("text-moss", inStock);
      stockEl.classList.toggle("text-red-600", !inStock);
      stockEl.innerHTML =
        `<i data-lucide="${inStock ? "circle-check" : "circle-x"}" class="h-4 w-4"></i> ` +
        (inStock ? "In stock — ships in 3–5 days" : "Currently out of stock");
      refreshIcons(stockEl);
    }
    const addBtn = document.getElementById("add-to-cart-btn");
    const buyBtn = document.getElementById("buy-now-btn");
    const inStock = parseInt(target.dataset.stock || "0", 10) > 0;
    if (addBtn) addBtn.disabled = !inStock;
    if (buyBtn) buyBtn.disabled = !inStock;
  }

  const attrSelector = document.querySelector("[data-attribute-selector]");
  if (attrSelector) {
    const radios = Array.from(attrSelector.querySelectorAll("input[name=variant]"));
    const pills = Array.from(attrSelector.querySelectorAll(".attr-pill"));
    const selected = {};
    const sync = () => {
      const want = Object.values(selected);
      let target =
        radios.find((r) => {
          const vals = (r.dataset.values || "").split(",").filter(Boolean);
          return want.length && want.every((v) => vals.includes(String(v)));
        }) || radios.find((r) => r.checked) || radios[0];
      radios.forEach((r) => (r.checked = r === target));
      applyVariant(target);
    };
    pills.forEach((pill) => {
      pill.addEventListener("click", () => {
        const attrId = pill.closest("[data-attribute-id]").dataset.attributeId;
        if (selected[attrId] === pill.dataset.valueId) {
          delete selected[attrId];
          pill.classList.remove("attr-selected");
        } else {
          selected[attrId] = pill.dataset.valueId;
          pills.forEach((p) => {
            if (p.closest("[data-attribute-id]").dataset.attributeId === attrId) {
              p.classList.toggle("attr-selected", p === pill);
            }
          });
        }
        sync();
      });
    });
    const first = radios.find((r) => r.checked) || radios[0];
    if (first) {
      (first.dataset.values || "").split(",").filter(Boolean).forEach((vid) => {
        const pill = pills.find((p) => p.dataset.valueId === vid);
        if (pill) {
          selected[pill.closest("[data-attribute-id]").dataset.attributeId] = vid;
          pill.classList.add("attr-selected");
        }
      });
      applyVariant(first);
    }
  } else {
    document.addEventListener("change", (e) => {
      const radio = e.target.closest('input[name=variant]');
      if (radio && radio.checked) applyVariant(radio);
    });
  }

  /* ---------- header shadow on scroll ---------- */
  const header = document.getElementById("site-header");
  if (header) {
    const onScroll = () =>
      header.classList.toggle("shadow-[0_10px_30px_-18px_rgba(38,32,26,0.25)]", window.scrollY > 8);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* ---------- search overlay ---------- */
  const searchToggle = document.getElementById("search-toggle");
  const searchOverlay = document.getElementById("search-overlay");
  const searchClose = document.getElementById("search-close");
  const searchInput = document.getElementById("search-input");
  if (searchToggle && searchOverlay) {
    searchToggle.addEventListener("click", () => {
      const hidden = searchOverlay.classList.toggle("hidden");
      if (!hidden) setTimeout(() => searchInput && searchInput.focus(), 50);
    });
    if (searchClose)
      searchClose.addEventListener("click", () => searchOverlay.classList.add("hidden"));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") searchOverlay.classList.add("hidden");
    });
  }

  /* ---------- mobile menu ---------- */
  const mobileMenu = document.getElementById("mobile-menu");
  const openBtn = document.getElementById("mobile-menu-open");
  const closeBtn = document.getElementById("mobile-menu-close");
  const backdrop = document.getElementById("mobile-menu-backdrop");
  const panel = document.getElementById("mobile-menu-panel");
  if (mobileMenu) {
    const open = () => {
      mobileMenu.classList.remove("hidden");
      document.body.style.overflow = "hidden";
      requestAnimationFrame(() => {
        backdrop.classList.remove("opacity-0");
        panel.classList.remove("-translate-x-full");
      });
    };
    const close = () => {
      backdrop.classList.add("opacity-0");
      panel.classList.add("-translate-x-full");
      document.body.style.overflow = "";
      setTimeout(() => mobileMenu.classList.add("hidden"), 300);
    };
    openBtn && openBtn.addEventListener("click", open);
    closeBtn && closeBtn.addEventListener("click", close);
    backdrop && backdrop.addEventListener("click", close);
  }

  /* ---------- mobile menu accordion ---------- */
  document.addEventListener("click", (e) => {
    const toggle = e.target.closest(".mobile-accordion-toggle");
    if (!toggle) return;
    const body = toggle.nextElementSibling;
    const icon = toggle.querySelector("i");
    body.classList.toggle("hidden");
    icon && icon.classList.toggle("rotate-180");
  });

  /* ---------- product accordion ---------- */
  document.addEventListener("click", (e) => {
    const toggle = e.target.closest(".accordion-toggle");
    if (!toggle) return;
    const body = toggle.nextElementSibling;
    const icon = toggle.querySelector(".accordion-icon");
    body.classList.toggle("hidden");
    icon && icon.classList.toggle("rotate-45");
  });

  /* ---------- gallery thumbnails ---------- */
  document.addEventListener("click", (e) => {
    const thumb = e.target.closest(".gallery-thumb");
    if (!thumb) return;
    const main = document.getElementById("main-image");
    if (main) {
      main.style.opacity = "0";
      setTimeout(() => {
        main.src = thumb.dataset.src;
        main.style.opacity = "1";
      }, 150);
    }
    document.querySelectorAll(".gallery-thumb").forEach((t) =>
      t.classList.toggle("border-bark", t === thumb),
      t.classList.toggle("border-transparent", t !== thumb),
    );
  });

  /* ---------- quantity steppers ---------- */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".qty-btn");
    if (!btn) return;
    const delta = parseInt(btn.dataset.delta || "0", 10);

    const productForm = document.getElementById("product-form");
    if (productForm && productForm.contains(btn)) {
      const input = document.getElementById("qty-input");
      const display = document.getElementById("qty-display");
      let qty = parseInt(input.value || "1", 10) + delta;
      qty = Math.min(Math.max(qty, 1), 20);
      input.value = qty;
      if (display) display.textContent = qty;
      return;
    }

    const itemId = btn.dataset.item;
    if (itemId) {
      const display = document.querySelector(`.qty-display[data-item="${itemId}"]`);
      let qty = parseInt(display.textContent, 10) + delta;
      qty = Math.min(Math.max(qty, 1), 20);
      document.dispatchEvent(
        new CustomEvent("cart:update", { detail: { itemId, quantity: qty } }),
      );
    }
  });

  /* ---------- star rating input ---------- */
  function paintStars(container) {
    const inputs = Array.from(container.querySelectorAll("input[type=radio]"));
    const selected = inputs.findIndex((i) => i.checked);
    if (selected === -1) return;
    inputs.forEach((input, idx) => {
      const icon = input.parentElement.querySelector(".star-option");
      if (!icon) return;
      const active = idx <= selected;
      icon.classList.toggle("text-clay", active);
      icon.classList.toggle("fill-current", active);
      icon.classList.toggle("text-linen", !active);
    });
  }
  const starInput = document.getElementById("star-input");
  if (starInput) {
    paintStars(starInput);
    starInput.addEventListener("change", () => paintStars(starInput));
  }

  /* ---------- reveal on scroll ---------- */
  const revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 },
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- message toasts (server-rendered) ---------- */
  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".message-close");
    if (!btn) return;
    const toast = btn.closest(".message-toast");
    toast.style.transition = "opacity .3s ease, transform .3s ease";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(-8px)";
    setTimeout(() => toast.remove(), 300);
  });
  document.querySelectorAll(".message-toast[data-auto-dismiss]").forEach((t) => {
    setTimeout(() => {
      t.style.transition = "opacity .3s ease, transform .3s ease";
      t.style.opacity = "0";
      t.style.transform = "translateY(-8px)";
      setTimeout(() => t.remove(), 300);
    }, parseInt(t.dataset.autoDismiss, 10) || 6000);
  });

  /* ---------- icons ---------- */
  document.addEventListener("DOMContentLoaded", () => refreshIcons());
  refreshIcons();
})();
