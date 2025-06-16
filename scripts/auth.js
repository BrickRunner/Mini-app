document.addEventListener('DOMContentLoaded', () => {
    // Переключение темы и активный пункт меню
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const body = document.body;

    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // Иконка "Солнце"
            shoppingBagIcon.src = 'images/bag_1.svg'; // Тёмная корзина
            accountIcon.src = 'images/account_1.svg'; // Тёмный профиль
        } else {
            themeToggle.src = 'images/light_theme.svg'; // Иконка "Луна"
            shoppingBagIcon.src = 'images/bag.svg'; // Светлая корзина
            accountIcon.src = 'images/account.svg'; // Светлый профиль
        }
    }

    // Применяем сохранённую тему при загрузке страницы
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // Обработка кликов по пунктам меню для выделения активного
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // Переключение темы по клику на иконку
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    // Маска ввода для телефона
    const phoneInput = document.getElementById("phone");

    phoneInput.addEventListener("input", function (e) {
        let value = e.target.value.replace(/\D/g, ""); // Убираем всё, кроме цифр

        // Если начинается с 8, заменяем на 7 (российский код)
        if (value.startsWith("8")) {
            value = "7" + value.slice(1);
        }

        // Ограничиваем длину до 11 цифр (например: 7XXXXXXXXXX)
        if (value.length > 11) value = value.slice(0, 11);

        // Форматируем строку для отображения
        let formatted = "+7 ";
        if (value.length > 1) formatted += "(" + value.slice(1, 4);
        if (value.length >= 4) formatted += ") " + value.slice(4, 7);
        if (value.length >= 7) formatted += "-" + value.slice(7, 9);
        if (value.length >= 9) formatted += "-" + value.slice(9, 11);

        e.target.value = formatted;
    });

    // Обработка отправки формы — очищаем телефон от лишних символов, оставляем +7XXXXXXXXXX
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", function(e) {
            let raw = phoneInput.value.replace(/\D/g, '');
            phoneInput.value = '+7' + raw.slice(1);
        });
    }
});