// === БЛОК: Запуск скрипта после полной загрузки DOM ===
document.addEventListener('DOMContentLoaded', () => {
    // === БЛОК: Получение элементов интерфейса ===
    const menuItems = document.querySelectorAll('.menu-item');              // Пункты навигационного меню
    const themeToggle = document.getElementById('theme-toggle');            // Кнопка переключения темы
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');  // Иконка корзины
    const accountIcon = document.querySelector('.account-icon');           // Иконка аккаунта
    const body = document.body;                                             // Тег <body> для применения темы

    // === БЛОК: Функция обновления иконок в зависимости от темы ===
    function updateIcons(isDark) {
        if (isDark) {
            // Иконки для тёмной темы
            themeToggle.src = 'images/dark_theme.svg';       // Иконка солнца (тёмная тема включена)
            shoppingBagIcon.src = 'images/bag_1.svg';         // Тёмная версия корзины
            accountIcon.src = 'images/account_1.svg';         // Тёмная версия профиля
        } else {
            // Иконки для светлой темы
            themeToggle.src = 'images/light_theme.svg';      // Иконка луны (светлая тема включена)
            shoppingBagIcon.src = 'images/bag.svg';           // Светлая корзина
            accountIcon.src = 'images/account.svg';           // Светлый профиль
        }
    }

    // === БЛОК: Применение сохранённой темы при загрузке страницы ===
    const savedTheme = localStorage.getItem('theme');         // Получаем сохранённую тему из localStorage
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');                     // Применяем тёмную тему
        updateIcons(true);                                    // Обновляем иконки под тёмную тему
    } else {
        updateIcons(false);                                   // Оставляем светлую тему и соответствующие иконки
    }

    // === БЛОК: Подсветка активного пункта меню при клике ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));  // Убираем активный класс со всех пунктов
            item.classList.add('active');                          // Добавляем активный класс текущему
            const category = item.querySelector('span').textContent; // Получаем название категории
            console.log(`Выбрана категория: ${category}`);         // Выводим в консоль выбранную категорию
        });
    });

    // === БЛОК: Обработка переключения темы по нажатию на иконку ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');                  // Переключаем класс темы на <body>
        const isDark = body.classList.contains('dark-theme');// Определяем текущую тему
        updateIcons(isDark);                                 // Обновляем иконки в соответствии с темой
        localStorage.setItem('theme', isDark ? 'dark' : 'light'); // Сохраняем выбранную тему в localStorage
    });
});