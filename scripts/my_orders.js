document.querySelectorAll('.order-date').forEach(el => {
    const utcDate = new Date(el.dataset.datetime);
    const localDate = utcDate.toLocaleDateString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
    el.textContent = localDate;
  });

  document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const body = document.body;

    // Функция для обновления всех иконок
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // Солнце
            shoppingBagIcon.src = 'images/bag_1.svg'; // Темная корзина
            accountIcon.src = 'images/account_1.svg'; // Темный профиль
        } else {
            themeToggle.src = 'images/light_theme.svg'; // Луна
            shoppingBagIcon.src = 'images/bag.svg'; // Светлая корзина
            accountIcon.src = 'images/account.svg'; // Светлый профиль
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
