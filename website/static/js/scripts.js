// Progressive enhancement only: the shop and product pages work without JavaScript.
document.addEventListener('DOMContentLoaded', () => {
  // Shop category filters
  const filters = document.querySelectorAll('.filter');
  const cards = document.querySelectorAll('.product-grid--shop .product-card');
  const count = document.getElementById('shopCount');
  filters.forEach((button) => button.addEventListener('click', () => {
    const category = button.dataset.filter;
    filters.forEach((b) => b.classList.toggle('is-active', b === button));
    let shown = 0;
    cards.forEach((card) => {
      const match = category === 'all' || card.dataset.category === category;
      card.hidden = !match;
      if (match) shown += 1;
    });
    if (count) count.textContent = shown;
  }));

  // Product gallery thumbnails
  const main = document.getElementById('galleryMain');
  const thumbs = document.querySelectorAll('.thumb');
  thumbs.forEach((thumb) => thumb.addEventListener('click', () => {
    main.src = thumb.dataset.src;
    thumbs.forEach((t) => t.classList.toggle('is-active', t === thumb));
  }));

  // Pocket embroidery add-on: update the total and send custom orders to the contact form
  const addon = document.getElementById('addonCustom');
  const total = document.getElementById('orderTotal');
  const order = document.getElementById('orderButton');
  if (addon && total && order) {
    const update = () => {
      const custom = addon.checked;
      total.textContent = '£' + (Number(total.dataset.base) + (custom ? Number(total.dataset.addon) : 0));
      order.href = custom ? order.dataset.custom : order.dataset.plain;
      order.querySelector('.order-label').textContent = custom ? 'Order with embroidery' : order.dataset.plainLabel;
    };
    addon.addEventListener('change', update);
    update();
  }
});
