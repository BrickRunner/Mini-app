// Ждём, пока DOM полностью загрузится, чтобы можно было работать с элементами страницы
document.addEventListener('DOMContentLoaded', () => {
    // Получаем список всех пунктов меню с классом .menu-item
    const menuItems = document.querySelectorAll('.menu-item');

    // Получаем элементы иконок: переключатель темы, корзина и профиль
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');

    // Получаем элемент <body>, чтобы менять у него класс темы
    const body = document.body;

    // Функция для обновления иконок в зависимости от текущей темы
    function updateIcons(isDark) {
        if (isDark) {
            // Если тёмная тема — ставим соответствующие иконки
            themeToggle.src = 'images/dark_theme.svg';      // Иконка "Солнце" — чтобы переключать на светлую
            shoppingBagIcon.src = 'images/bag_1.svg';       // Тёмная корзина
            accountIcon.src = 'images/account_1.svg';       // Тёмный профиль
        } else {
            // Если светлая тема — ставим светлые иконки
            themeToggle.src = 'images/light_theme.svg';     // Иконка "Луна" — чтобы переключать на тёмную
            shoppingBagIcon.src = 'images/bag.svg';         // Светлая корзина
            accountIcon.src = 'images/account.svg';         // Светлый профиль
        }
    }

    // Проверяем, сохранена ли тема в localStorage от предыдущих посещений
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        // Если была тёмная — применяем её и меняем иконки
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        // Если нет — оставляем светлую и обновляем иконки соответственно
        updateIcons(false);
    }

    // Обрабатываем клики по пунктам меню
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Убираем класс активности у всех пунктов меню
            menuItems.forEach(i => i.classList.remove('active'));
            // Добавляем класс активности к выбранному пункту
            item.classList.add('active');
            // Получаем текст категории внутри span и выводим в консоль
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // Обрабатываем клик по иконке переключения темы
    themeToggle.addEventListener('click', () => {
        // Переключаем класс "dark-theme" у body
        body.classList.toggle('dark-theme');
        // Проверяем, включена ли сейчас тёмная тема
        const isDark = body.classList.contains('dark-theme');
        // Обновляем иконки под текущую тему
        updateIcons(isDark);
        // Сохраняем выбранную тему в localStorage для будущих загрузок
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});