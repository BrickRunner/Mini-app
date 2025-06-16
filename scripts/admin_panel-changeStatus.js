// Запуск скрипта после полной загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    // Получаем все пункты меню
    const menuItems = document.querySelectorAll('.menu-item');

    // Получаем элементы иконок: переключение темы, корзина, профиль
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');

    // Получаем <body> — на него будет вешаться класс темы
    const body = document.body;

    // === Функция для обновления иконок в зависимости от темы ===
    function updateIcons(isDark) {
        if (isDark) {
            // Устанавливаем иконки для темной темы
            themeToggle.src = 'images/dark_theme.svg';      // Солнце (значок светлой темы)
            shoppingBagIcon.src = 'images/bag_1.svg';       // Темная иконка корзины
            accountIcon.src = 'images/account_1.svg';       // Темная иконка профиля
        } else {
            // Устанавливаем иконки для светлой темы
            themeToggle.src = 'images/light_theme.svg';     // Луна (значок темной темы)
            shoppingBagIcon.src = 'images/bag.svg';         // Светлая корзина
            accountIcon.src = 'images/account.svg';         // Светлый профиль
        }
    }

    // === Проверка сохранённой темы при загрузке страницы ===
    const savedTheme = localStorage.getItem('theme'); // Получаем тему из localStorage
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme'); // Применяем темную тему
        updateIcons(true);                // Обновляем иконки под темную тему
    } else {
        updateIcons(false);               // Обновляем иконки под светлую тему
    }

    // === Обработка кликов по пунктам меню ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Удаляем класс 'active' со всех пунктов
            menuItems.forEach(i => i.classList.remove('active'));

            // Добавляем класс 'active' к выбранному пункту
            item.classList.add('active');

            // Получаем текст категории и выводим в консоль
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // === Обработка клика по иконке темы ===
    themeToggle.addEventListener('click', () => {
        // Переключаем класс 'dark-theme' у <body>
        body.classList.toggle('dark-theme');

        // Определяем текущую тему
        const isDark = body.classList.contains('dark-theme');

        // Обновляем иконки в соответствии с темой
        updateIcons(isDark);

        // Сохраняем текущую тему в localStorage
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});