(() => {
  const zoomItems = Array.from(document.querySelectorAll(".blog-zoom[data-full]"));
  if (!zoomItems.length) return;

  const lightbox = document.createElement("div");
  lightbox.className = "blog-lightbox";
  lightbox.setAttribute("role", "dialog");
  lightbox.setAttribute("aria-modal", "true");
  lightbox.setAttribute("aria-label", "Bildansicht");
  lightbox.innerHTML = `
    <div class="blog-lightbox-panel">
      <button class="blog-lightbox-close" type="button" aria-label="Bildansicht schliessen">&times;</button>
      <div class="blog-lightbox-stage">
        <img alt="" />
      </div>
      <p class="blog-lightbox-caption"></p>
    </div>`;
  document.body.appendChild(lightbox);

  const closeButton = lightbox.querySelector(".blog-lightbox-close");
  const image = lightbox.querySelector("img");
  const caption = lightbox.querySelector(".blog-lightbox-caption");
  let activeItem = null;

  const close = () => {
    lightbox.classList.remove("is-open");
    document.body.classList.remove("blog-lightbox-open");
    image.removeAttribute("src");
    caption.textContent = "";
    if (activeItem) activeItem.focus();
    activeItem = null;
  };

  const open = (item) => {
    const thumb = item.querySelector("img");
    activeItem = item;
    image.src = item.dataset.full;
    image.alt = thumb?.alt || "Vergroessertes Blogbild";
    caption.textContent = item.dataset.caption || thumb?.alt || "";
    lightbox.classList.add("is-open");
    document.body.classList.add("blog-lightbox-open");
    closeButton.focus();
  };

  zoomItems.forEach((item) => {
    item.tabIndex = 0;
    item.setAttribute("role", "button");
    item.setAttribute("aria-label", "Bild vergroessern");
    item.addEventListener("click", () => open(item));
    item.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open(item);
      }
    });
  });

  closeButton.addEventListener("click", close);
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) close();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && lightbox.classList.contains("is-open")) {
      close();
    }
  });
})();
