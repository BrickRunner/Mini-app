// === Запуск кода после полной загрузки DOM ===
document.addEventListener('DOMContentLoaded', () => {
    // Получаем все элементы меню навигации
    const menuItems = document.querySelectorAll('.menu-item');

    // Получаем элементы иконок
    const themeToggle = document.getElementById('theme-toggle'); // Кнопка переключения темы
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon'); // Иконка корзины
    const accountIcon = document.querySelector('.account-icon'); // Иконка аккаунта
    const acessories = document.querySelector('.menu-text'); // Иконка аксессуаров
    const body = document.body;

    // === Функция обновления иконок в зависимости от темы ===
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg';         // Солнце (тёмная тема)
            shoppingBagIcon.src = 'images/bag_1.svg';           // Тёмная корзина
            accountIcon.src = 'images/account_1.svg';           // Тёмный профиль
            acessories.src = 'images/acsessories_1.svg';        // Тёмные аксессуары
        } else {
            themeToggle.src = 'images/light_theme.svg';        // Луна (светлая тема)
            shoppingBagIcon.src = 'images/bag.svg';             // Светлая корзина
            accountIcon.src = 'images/account.svg';             // Светлый профиль
            acessories.src = 'images/acessories.svg';           // Светлые аксессуары
        }
    }

    // === Применение сохранённой темы из localStorage ===
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme'); // Применяем тёмную тему
        updateIcons(true);
    } else {
        updateIcons(false); // Оставляем светлую по умолчанию
    }

    // === Обработка кликов по пунктам меню ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Удаляем выделение со всех пунктов
            menuItems.forEach(i => i.classList.remove('active'));

            // Выделяем выбранный пункт
            item.classList.add('active');

            // Получаем текст выбранной категории и выводим в консоль
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // === Переключение темы при клике ===
    themeToggle.addEventListener('click', () => {
        // Меняем тему на противоположную
        body.classList.toggle('dark-theme');

        // Проверяем текущую тему
        const isDark = body.classList.contains('dark-theme');

        // Обновляем иконки
        updateIcons(isDark);

        // Сохраняем текущую тему в localStorage
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});


// === Обработка кликов по кнопкам "Избранное" ===
document.addEventListener('DOMContentLoaded', function () {
    // Получаем все формы добавления в избранное
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        const button = form.querySelector('.favorite-btn'); // Кнопка (обычно span или div)
        const icon = form.querySelector('.heart-icon');     // Иконка сердца

        // Добавляем обработчик клика
        button.addEventListener('click', function () {
            const productId = form.dataset.productId; // Получаем ID продукта из data-атрибута

            // Отправляем POST-запрос на сервер
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ product_id: productId }) // Отправляем ID продукта
            })
            .then(response => response.json())
            .then(data => {
                // Обработка ответа от сервера
                if (data.status === 'added') {
                    // Продукт добавлен в избранное — меняем иконку на "заполненное сердце"
                    icon.src = '/images/heart-filled.png';
                    icon.dataset.favorite = 'true';
                } else if (data.status === 'removed') {
                    // Продукт удалён из избранного — возвращаем пустую иконку
                    icon.src = '/images/heart.png';
                    icon.dataset.favorite = 'false';
                }
            })
            .catch(error => console.error('Ошибка:', error)); // Обработка ошибок
        });
    });
});