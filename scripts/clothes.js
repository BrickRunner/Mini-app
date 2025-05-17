document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const tshirt = document.querySelector('.menu-text');
    const body = document.body;

    // Функция для обновления всех иконок
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // Солнце
            shoppingBagIcon.src = 'images/bag_1.svg'; // Темная корзина
            accountIcon.src = 'images/account_1.svg'; // Темный профиль
            tshirt.src = 'images/shirt_1.svg'
        } else {
            themeToggle.src = 'images/light_theme.svg'; // Луна
            shoppingBagIcon.src = 'images/bag.svg'; // Светлая корзина
            accountIcon.src = 'images/account.svg'; // Светлый профиль
            tshirt.src = 'images/shirt.svg'
        }
    }

    // Проверка сохранённой темы при загрузке
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // Обработка кликов по меню
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // Переключение темы
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});

document.querySelectorAll('.favorite-icon').forEach(icon => {
  icon.addEventListener('click', () => {
      const productId = icon.dataset.productId;

      fetch('/toggle_favorite', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ product_id: productId })
      })
      .then(response => response.json())
      .then(data => {
          document.querySelectorAll(`.favorite-icon[data-product-id="${productId}"]`)
              .forEach(el => {
                  el.innerHTML = (data.status === 'added') ? '❤️' : '♡';
              });
      });
  });
});