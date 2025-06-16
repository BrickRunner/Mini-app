document.addEventListener('DOMContentLoaded', () => {
    // Получаем все элементы меню с классом .menu-item
    const menuItems = document.querySelectorAll('.menu-item');
    // Получаем иконки переключателя темы, корзины и аккаунта
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    // Ссылка на элемент body для переключения темы
    const body = document.body;

    // Функция для обновления иконок в зависимости от темы
    function updateIcons(isDark) {
        if (isDark) {
            // Тёмная тема — меняем иконки на "тёмные" версии
            themeToggle.src = 'images/dark_theme.svg'; // Иконка "солнце" — для переключения обратно на светлую тему
            shoppingBagIcon.src = 'images/bag_1.svg'; // Тёмная корзина
            accountIcon.src = 'images/account_1.svg'; // Тёмный профиль
        } else {
            // Светлая тема — ставим "светлые" иконки
            themeToggle.src = 'images/light_theme.svg'; // Иконка "луна" — для переключения на тёмную тему
            shoppingBagIcon.src = 'images/bag.svg';     // Светлая корзина
            accountIcon.src = 'images/account.svg';     // Светлый профиль
        }
    }

    // При загрузке страницы проверяем, сохранена ли тема в localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        // Если тёмная тема — добавляем класс и обновляем иконки
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        // Иначе — светлая тема и светлые иконки
        updateIcons(false);
    }

    // Добавляем обработчик клика для каждого пункта меню
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Сначала убираем класс активности у всех пунктов меню
            menuItems.forEach(i => i.classList.remove('active'));
            // Добавляем активный класс к тому пункту, по которому кликнули
            item.classList.add('active');
            // Получаем текст из вложенного span и выводим в консоль
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // Обработчик клика по иконке переключения темы
    themeToggle.addEventListener('click', () => {
        // Переключаем класс dark-theme у body
        body.classList.toggle('dark-theme');
        // Проверяем, какая тема активна сейчас
        const isDark = body.classList.contains('dark-theme');
        // Обновляем иконки под текущую тему
        updateIcons(isDark);
        // Сохраняем выбор темы в localStorage для будущих загрузок страницы
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});