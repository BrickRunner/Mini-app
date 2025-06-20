document.addEventListener('DOMContentLoaded', () => {
    // --- Инициализация элементов страницы ---
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const favoriteIcons = document.querySelectorAll('.favorite-btn img');
    const body = document.body;

    // --- Функция обновления иконок в зависимости от темы ---
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // иконка солнца для темной темы
            shoppingBagIcon.src = 'images/bag_1.svg';
            accountIcon.src = 'images/account_1.svg';

            favoriteIcons.forEach(icon => {
                if (icon.src.includes('heart-filled')) {
                    icon.src = 'images/heart-filled.png';
                } else {
                    icon.src = 'images/heart_1.svg';
                }
            });

        } else {
            themeToggle.src = 'images/light_theme.svg'; // иконка луны для светлой темы
            shoppingBagIcon.src = 'images/bag.svg';
            accountIcon.src = 'images/account.svg';

            favoriteIcons.forEach(icon => {
                if (icon.src.includes('heart-filled')) {
                    icon.src = 'images/heart-filled.png';
                } else {
                    icon.src = 'images/heart.png';
                }
            });
        }
    }

    // --- Загрузка сохранённой темы при загрузке страницы ---
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // --- Обработка кликов по пунктам меню ---
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // --- Переключение темы по клику ---
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // --- Обработка кнопок избранного ---
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        const button = form.querySelector('.favorite-btn');
        const icon = form.querySelector('.heart-icon');

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