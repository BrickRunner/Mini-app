document.addEventListener('DOMContentLoaded', () => {
    // Получение элементов меню, кнопки переключения темы и иконок
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const shoes = document.querySelector('.menu-text');
    const body = document.body;

    // Функция для обновления иконок в зависимости от темы (светлая/темная)
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // Иконка солнца
            shoppingBagIcon.src = 'images/bag_1.svg'; // Темная корзина
            accountIcon.src = 'images/account_1.svg'; // Темный профиль
            shoes.src = 'images/shoe_1.svg'; // Темные кроссовки
        } else {
            themeToggle.src = 'images/light_theme.svg'; // Иконка луны
            shoppingBagIcon.src = 'images/bag.svg'; // Светлая корзина
            accountIcon.src = 'images/account.svg'; // Светлый профиль
            shoes.src = 'images/shoe.svg'; // Светлые кроссовки
        }
    }

    // Применение сохранённой в localStorage темы при загрузке страницы
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // Обработчик кликов по пунктам меню: переключение активного состояния и вывод выбранной категории в консоль
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // Переключение темы при клике на иконку переключателя, обновление иконок и сохранение выбора
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // Поиск всех форм добавления/удаления из избранного
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        const button = form.querySelector('.favorite-btn');
        const icon = form.querySelector('.heart-icon');

        // Обработчик клика по кнопке избранного: отправка POST-запроса на сервер
        button.addEventListener('click', function () {
            const productId = form.dataset.productId;

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                // Обновление иконки и состояния в зависимости от ответа сервера
                if (data.status === 'added') {
                    icon.src = '/images/heart-filled.png';
                    icon.dataset.favorite = 'true';
                } else if (data.status === 'removed') {
                    icon.src = '/images/heart.png';
                    icon.dataset.favorite = 'false';
                }
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });
});