// Ждем полной загрузки DOM, чтобы обращаться к элементам страницы
document.addEventListener('DOMContentLoaded', () => {
    
    // === ИНИЦИАЛИЗАЦИЯ ПЕРЕМЕННЫХ ===
    // Получаем все нужные элементы из DOM: меню, переключатель темы, иконки и body
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const body = document.body;

    // === ФУНКЦИЯ ОБНОВЛЕНИЯ ИКОНКИ ПРИ СМЕНЕ ТЕМЫ ===
    // В зависимости от текущей темы (isDark), подставляет соответствующие иконки
    function updateIcons(isDark) {
        if (isDark) {
            // Темная тема: иконки в темном стиле
            themeToggle.src = 'images/dark_theme.svg';
            shoppingBagIcon.src = 'images/bag_1.svg';
            accountIcon.src = 'images/account_1.svg';
        } else {
            // Светлая тема: иконки в светлом стиле
            themeToggle.src = 'images/light_theme.svg';
            shoppingBagIcon.src = 'images/bag.svg';
            accountIcon.src = 'images/account.svg';
        }
    }

    // === ЗАГРУЗКА СОХРАНЕННОЙ ТЕМЫ ПРИ ПЕРЕЗАГРУЗКЕ СТРАНИЦЫ ===
    // Проверяем, какая тема сохранена в localStorage, и применяем её
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // === НАСТРОЙКА ПОВЕДЕНИЯ ПУНКТОВ МЕНЮ ===
    // При клике на пункт меню:
    // - снимается активность со всех пунктов
    // - выделяется активный
    // - выводится название выбранной категории в консоль
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // === ОБРАБОТКА ПЕРЕКЛЮЧЕНИЯ ТЕМЫ ===
    // При клике на иконку темы:
    // - переключается класс на body (темная/светлая тема)
    // - обновляются иконки
    // - новое значение темы сохраняется в localStorage
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

});