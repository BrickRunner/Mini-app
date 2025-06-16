// Ждём, пока DOM полностью загрузится, чтобы безопасно работать с элементами страницы
document.addEventListener('DOMContentLoaded', () => {
    // Получаем все пункты меню с классом .menu-item
    const menuItems = document.querySelectorAll('.menu-item');

    // Получаем иконки: переключатель темы, корзина, профиль и "все товары"
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const all_products = document.querySelector('.menu-text');

    // Получаем <body> для смены темы
    const body = document.body;

    // Функция для обновления иконок в зависимости от текущей темы
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg';      // Иконка солнца — для переключения на светлую тему
            shoppingBagIcon.src = 'images/bag_1.svg';       // Тёмная корзина
            accountIcon.src = 'images/account_1.svg';       // Тёмный профиль
            all_products.src = 'images/all_products_1.svg'; // Тёмная иконка "все товары"
        } else {
            themeToggle.src = 'images/light_theme.svg';     // Иконка луны — для переключения на тёмную тему
            shoppingBagIcon.src = 'images/bag.svg';         // Светлая корзина
            accountIcon.src = 'images/account.svg';         // Светлый профиль
            all_products.src = 'images/all_products.svg';   // Светлая иконка "все товары"
        }
    }

    // При загрузке страницы проверяем, есть ли сохранённая тема в localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        // Если сохранена тёмная — применяем её и обновляем иконки
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        // Иначе светлая тема (по умолчанию)
        updateIcons(false);
    }

    // Обработка кликов по пунктам меню
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            // Убираем класс активности у всех пунктов меню
            menuItems.forEach(i => i.classList.remove('active'));
            // Добавляем класс активности к текущему пункту
            item.classList.add('active');
            // Получаем текст категории из span внутри пункта меню и выводим в консоль
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // Обработка клика по переключателю темы
    themeToggle.addEventListener('click', () => {
        // Переключаем класс "dark-theme" у body
        body.classList.toggle('dark-theme');
        // Проверяем, какая тема сейчас активна
        const isDark = body.classList.contains('dark-theme');
        // Обновляем иконки под текущую тему
        updateIcons(isDark);
        // Сохраняем текущую тему в localStorage для последующих загрузок
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});


// Второй блок: обработка кликов по кнопкам "Избранное" у товаров
document.addEventListener('DOMContentLoaded', function () {
    // Получаем все формы с классом .favorite-form (каждая форма отвечает за один товар)
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        // В форме находим кнопку с классом .favorite-btn и иконку сердечка .heart-icon
        const button = form.querySelector('.favorite-btn');
        const icon = form.querySelector('.heart-icon');

        // Навешиваем обработчик нажатия на кнопку "избранное"
        button.addEventListener('click', function () {
            // Получаем id товара из data-атрибута формы
            const productId = form.dataset.productId;

            // Отправляем POST-запрос на сервер по адресу form.action с JSON-телом, содержащим product_id
            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',          // Указываем, что отправляем JSON
                    'X-Requested-With': 'XMLHttpRequest'          // Маркер AJAX-запроса
                },
                body: JSON.stringify({ product_id: productId })   // Отправляем id товара
            })
            .then(response => response.json())                    // Ждём JSON-ответ от сервера
            .then(data => {
                // Если сервер ответил, что товар добавлен в избранное
                if (data.status === 'added') {
                    icon.src = '/images/heart-filled.png';        // Меняем иконку на заполненное сердце
                    icon.dataset.favorite = 'true';                // Ставим флаг в data-атрибут
                }
                // Если сервер ответил, что товар удалён из избранного
                else if (data.status === 'removed') {
                    icon.src = '/images/heart.png';               // Меняем иконку на пустое сердце
                    icon.dataset.favorite = 'false';               // Снимаем флаг
                }
            })
            .catch(error => console.error('Ошибка:', error));    // Логируем ошибки, если что-то пошло не так
        });
    });
});