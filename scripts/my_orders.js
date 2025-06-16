// === БЛОК: Преобразование даты заказа из UTC в локальный формат ===
document.querySelectorAll('.order-date').forEach(el => {
    const utcDate = new Date(el.dataset.datetime); // Получаем дату из data-атрибута элемента
    const localDate = utcDate.toLocaleDateString('ru-RU', { // Преобразуем дату в формат ДД.ММ.ГГГГ
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
    el.textContent = localDate; // Заменяем текст в элементе на локализованную дату
});

// === БЛОК: Инициализация после полной загрузки DOM ===
document.addEventListener('DOMContentLoaded', () => {
    // === БЛОК: Получение элементов интерфейса ===
    const menuItems = document.querySelectorAll('.menu-item');              // Пункты бокового меню
    const themeToggle = document.getElementById('theme-toggle');            // Иконка переключения темы
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');  // Иконка корзины
    const accountIcon = document.querySelector('.account-icon');           // Иконка аккаунта
    const body = document.body;

    // === БЛОК: Обновление всех иконок в зависимости от темы ===
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg';     // Иконка темы: солнце
            shoppingBagIcon.src = 'images/bag_1.svg';      // Тёмная корзина
            accountIcon.src = 'images/account_1.svg';      // Тёмный аккаунт
        } else {
            themeToggle.src = 'images/light_theme.svg';    // Иконка темы: луна
            shoppingBagIcon.src = 'images/bag.svg';        // Светлая корзина
            accountIcon.src = 'images/account.svg';        // Светлый аккаунт
        }
    }

    // === БЛОК: Применение сохранённой темы при загрузке ===
    const savedTheme = localStorage.getItem('theme');      // Получаем тему из localStorage
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');                  // Применяем тёмную тему
        updateIcons(true);                                 // Обновляем иконки для тёмной темы
    } else {
        updateIcons(false);                                // Обновляем иконки для светлой темы
    }

    // === БЛОК: Обработка кликов по пунктам меню ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active')); // Снимаем активность со всех
            item.classList.add('active');                         // Назначаем активным текущий
            const category = item.querySelector('span').textContent; // Получаем название категории
            console.log(`Выбрана категория: ${category}`);        // Логируем в консоль
        });
    });

    // === БЛОК: Обработка переключения темы ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');                  // Переключаем класс темы
        const isDark = body.classList.contains('dark-theme');// Проверяем текущую тему
        updateIcons(isDark);                                 // Обновляем иконки
        localStorage.setItem('theme', isDark ? 'dark' : 'light'); // Сохраняем тему
    });
});