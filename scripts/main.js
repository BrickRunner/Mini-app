// === БЛОК: Выполнение после полной загрузки DOM ===
document.addEventListener('DOMContentLoaded', () => {
    // === БЛОК: Получение DOM-элементов интерфейса ===
    const menuItems = document.querySelectorAll('.menu-item');                 // Элементы бокового меню
    const themeToggle = document.getElementById('theme-toggle');              // Иконка переключения темы (луна/солнце)
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');     // Иконка корзины
    const accountIcon = document.querySelector('.account-icon');              // Иконка профиля
    const tshirtIcon = document.querySelector('.menu-icon-clothes');          // Иконка категории "Одежда"
    const shoesIcon = document.querySelector('.menu-icon-shoes');             // Иконка категории "Обувь"
    const accessoriesIcon = document.querySelector('.menu-icon-accessories'); // Иконка категории "Аксессуары"
    const allProductsIcon = document.querySelector('.menu-icon-allProducts'); // Иконка категории "Все товары"
    const body = document.body;

    // === БЛОК: Обновление всех иконок в зависимости от текущей темы ===
    function updateIcons(isDark) {
        if (isDark) {
            // Установка тёмных иконок
            themeToggle.src = 'images/dark_theme.svg';        // Солнце (иконка темной темы)
            shoppingBagIcon.src = 'images/bag_1.svg';         // Тёмная корзина
            accountIcon.src = 'images/account_1.svg';         // Тёмный профиль
            tshirtIcon.src = 'images/shirt_1.svg';            // Тёмная иконка одежды
            shoesIcon.src = 'images/shoe_1.svg';              // Тёмная иконка обуви
            accessoriesIcon.src = 'images/acsessories_1.svg'; // Тёмная иконка аксессуаров
            allProductsIcon.src = 'images/all_products_1.svg';// Тёмная иконка "все товары"
        } else {
            // Установка светлых иконок
            themeToggle.src = 'images/light_theme.svg';       // Луна (иконка светлой темы)
            shoppingBagIcon.src = 'images/bag.svg';           // Светлая корзина
            accountIcon.src = 'images/account.svg';           // Светлый профиль
            tshirtIcon.src = 'images/shirt.svg';              // Светлая иконка одежды
            shoesIcon.src = 'images/shoe.svg';                // Светлая иконка обуви
            accessoriesIcon.src = 'images/acessories.svg';    // Светлая иконка аксессуаров
            allProductsIcon.src = 'images/all_products.svg';  // Светлая иконка "все товары"
        }
    }

    // === БЛОК: Применение сохранённой темы при загрузке страницы ===
    const savedTheme = localStorage.getItem('theme');          // Получаем сохранённую тему из localStorage
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');                      // Применяем тёмную тему к телу страницы
        updateIcons(true);                                     // Обновляем иконки для тёмной темы
    } else {
        updateIcons(false);                                    // Обновляем иконки для светлой темы
    }

    // === БЛОК: Обработка кликов по пунктам меню ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active')); // Удаляем класс активности у всех пунктов меню
            item.classList.add('active');                          // Назначаем активный класс текущему элементу
            const category = item.querySelector('span').textContent; // Получаем текст названия категории
            console.log(`Выбрана категория: ${category}`);            // Выводим её в консоль
        });
    });

    // === БЛОК: Обработка переключения темы при клике по иконке ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');                      // Переключаем класс темы на body
        const isDark = body.classList.contains('dark-theme');    // Проверяем, активна ли тёмная тема
        updateIcons(isDark);                                     // Обновляем иконки соответствующим образом
        localStorage.setItem('theme', isDark ? 'dark' : 'light'); // Сохраняем выбранную тему в localStorage
    });
});