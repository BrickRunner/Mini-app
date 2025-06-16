// === БЛОК: Основная инициализация после загрузки страницы ===
document.addEventListener('DOMContentLoaded', () => {
    // === БЛОК: Получение элементов интерфейса ===
    const menuItems = document.querySelectorAll('.menu-item');         // Пункты меню
    const themeToggle = document.getElementById('theme-toggle');       // Иконка переключения темы
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon'); // Иконка корзины
    const accountIcon = document.querySelector('.account-icon');       // Иконка профиля
    const heart = document.querySelector('.menu-text');                // Иконка избранного (предположительно)
    const bins = document.querySelectorAll('.trash-icon');             // Иконки удаления (мусорки)
    const body = document.body;

    // === БЛОК: Функция обновления иконок при смене темы ===
    function updateIcons(isDark) {
        if (isDark) {
            // Установка тёмных иконок
            themeToggle.src = 'images/dark_theme.svg';       // Солнце — тёмная тема активна
            shoppingBagIcon.src = 'images/bag_1.svg';        // Тёмная корзина
            accountIcon.src = 'images/account_1.svg';        // Тёмный профиль
            heart.src = 'images/heart_1.svg';                // Тёмное избранное
            bins.forEach(bin => bin.src = 'images/bin_1.svg'); // Тёмные иконки удаления
        } else {
            // Установка светлых иконок
            themeToggle.src = 'images/light_theme.svg';      // Луна — светлая тема активна
            shoppingBagIcon.src = 'images/bag.svg';          // Светлая корзина
            accountIcon.src = 'images/account.svg';          // Светлый профиль
            heart.src = 'images/heart.png';                  // Светлое избранное
            bins.forEach(bin => bin.src = 'images/bin.png'); // Светлые иконки удаления
        }
    }

    // === БЛОК: Установка сохранённой темы при загрузке ===
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme'); // Применяем тёмную тему к телу страницы
        updateIcons(true);                // Обновляем иконки под тёмную тему
    } else {
        updateIcons(false);              // Обновляем иконки под светлую тему
    }

    // === БЛОК: Обработка кликов по пунктам меню ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active')); // Убираем активность со всех пунктов
            item.classList.add('active');                         // Делаем текущий пункт активным
            const category = item.querySelector('span').textContent; // Получаем текст выбранной категории
            console.log(`Выбрана категория: ${category}`);            // Логируем выбор (можно заменить на другой функционал)
        });
    });

    // === БЛОК: Переключение темы при клике на иконку ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');                    // Переключаем класс темы у <body>
        const isDark = body.classList.contains('dark-theme');  // Проверяем, стала ли тема тёмной
        updateIcons(isDark);                                   // Обновляем иконки в зависимости от темы
        localStorage.setItem('theme', isDark ? 'dark' : 'light'); // Сохраняем текущую тему в localStorage
    });
});