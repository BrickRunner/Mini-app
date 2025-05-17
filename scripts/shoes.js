document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const shoes = document.querySelector('.menu-text');
    const body = document.body;

    // Функция для обновления всех иконок
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // Солнце
            shoppingBagIcon.src = 'images/bag_1.svg'; // Темная корзина
            accountIcon.src = 'images/account_1.svg'; // Темный профиль
            shoes.src = 'images/shoe_1.svg'
        } else {
            themeToggle.src = 'images/light_theme.svg'; // Луна
            shoppingBagIcon.src = 'images/bag.svg'; // Светлая корзина
            accountIcon.src = 'images/account.svg'; // Светлый профиль
            shoes.src = 'images/shoe.svg'
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

async function toggleFavorite(button) {
    const productId = button.getAttribute('data-product-id');
    const img = button.querySelector('.heart-icon');
    const isFavorite = img.getAttribute('data-favorite') === 'true';
  
    try {
      const response = await fetch(`/toggle-favorite/${productId}`, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });
  
      if (response.ok) {
        const result = await response.json();
        const status = result.status;
  
        if (status === 'added') {
          img.src = '/images/heart-filled.png';
          img.setAttribute('data-favorite', 'true');
        } else if (status === 'removed') {
          img.src = '/images/heart.png';
          img.setAttribute('data-favorite', 'false');
        }
      } else {
        console.error('Ошибка при изменении избранного');
      }
    } catch (error) {
      console.error('Сервер не ответил:', error);
    }
  }
  