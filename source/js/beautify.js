/* 站点美化脚本：昼夜自动切换 + 卡片滚动浮现 */
(function () {
  /* 1. 昼夜自动切换：18 点后或 6 点前进暗色；用户手动切换过则以手动为准 */
  try {
    var h = new Date().getHours();
    var saved = localStorage.getItem('theme');
    if (!saved && (h >= 18 || h < 6)) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    }
  } catch (e) {}

  /* 2. 首页卡片与侧栏卡片滚动浮现 */
  function reveal() {
    if (!('IntersectionObserver' in window)) return;
    var items = document.querySelectorAll('.recent-post-item, .card-widget');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('reveal-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.1 });
    items.forEach(function (el) {
      if (!el.classList.contains('reveal')) {
        el.classList.add('reveal');
        io.observe(el);
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', reveal);
  } else {
    reveal();
  }
})();
