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

  /* 3. 小黄挂件：点击切换比心姿势并冒爱心 */
  function pet() {
    if (document.getElementById('xx-pet')) return;
    var d = document.createElement('div');
    d.id = 'xx-pet';
    d.title = '点点我~';
    d.innerHTML = '<img id="xx-pet-img" src="/img/pet-idle.png" alt="小黄">';
    document.body.appendChild(d);
    var img = document.getElementById('xx-pet-img');
    var heart = false;
    d.addEventListener('click', function () {
      heart = !heart;
      img.src = heart ? '/img/pet-heart.png' : '/img/pet-idle.png';
      if (heart) spawnHearts(d);
    });
  }

  function spawnHearts(container) {
    for (var i = 0; i < 5; i++) {
      var s = document.createElement('span');
      s.className = 'xx-float-heart';
      s.textContent = '❤';
      s.style.left = (15 + Math.random() * 65) + '%';
      s.style.animationDelay = i * 0.15 + 's';
      container.appendChild(s);
      (function (el, delay) {
        setTimeout(function () { el.remove(); }, 1600 + delay);
      })(s, i * 150);
    }
  }

  function init() {
    reveal();
    pet();
    poemRotate();
  }

  /* 4. 随机诗句轮换：110ms/字打完一整句后，自动换下一句（今日诗词 API） */
  function poemRotate() {
    var el = document.getElementById('site-subtitle');
    if (!el) return;

    function typeText(text, done) {
      el.textContent = '';
      var i = 0;
      var timer = setInterval(function () {
        el.textContent = text.slice(0, ++i);
        if (i >= text.length) {
          clearInterval(timer);
          done();
        }
      }, 110);
    }

    function next() {
      fetch('https://v1.jinrishici.com/all.json')
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d && d.content) {
            typeText(d.content + ' —— ' + d.author + '《' + d.origin + '》', function () {
              setTimeout(next, 800);
            });
          } else {
            setTimeout(next, 2000);
          }
        })
        .catch(function () { setTimeout(next, 2000); });
    }

    next();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
