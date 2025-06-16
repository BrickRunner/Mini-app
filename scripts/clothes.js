// === БЛОК: Инициализация темы и поведения меню ===
document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');           // Элементы меню категорий
    const themeToggle = document.getElementById('theme-toggle');         // Иконка переключения темы
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon'); // Иконка корзины
    const accountIcon = document.querySelector('.account-icon');         // Иконка профиля
    const tshirt = document.querySelector('.menu-text');                 // Иконка футболки (предположительно изображение)
    const body = document.body;

    // === БЛОК: Обновление иконок при смене темы ===
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg'; // Солнце — иконка тёмной темы
            shoppingBagIcon.src = 'images/bag_1.svg';  // Тёмная версия корзины
            accountIcon.src = 'images/account_1.svg';  // Тёмная версия профиля
            tshirt.src = 'images/shirt_1.svg';         // Тёмная версия иконки одежды
        } else {
            themeToggle.src = 'images/light_theme.svg'; // Луна — иконка светлой темы
            shoppingBagIcon.src = 'images/bag.svg';     // Светлая версия корзины
            accountIcon.src = 'images/account.svg';     // Светлая версия профиля
            tshirt.src = 'images/shirt.svg';            // Светлая версия иконки одежды
        }
    }

    // === БЛОК: Установка темы при загрузке страницы ===
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // === БЛОК: Обработка кликов по пунктам меню ===
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active')); // Снимаем активность со всех
            item.classList.add('active'); // Делаем активным текущий элемент
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // === БЛОК: Переключение темы при клике по иконке ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark); // Обновляем иконки в зависимости от темы
        localStorage.setItem('theme', isDark ? 'dark' : 'light'); // Сохраняем тему
    });
});


// === БЛОК: Обработка добавления и удаления товара в избранное ===
document.addEventListener('DOMContentLoaded', function () {
    const favoriteForms = document.querySelectorAll('.favorite-form'); // Все формы добавления в избранное

    favoriteForms.forEach(form => {
        const button = form.querySelector('.favorite-btn'); // Кнопка "лайка"
        const icon = form.querySelector('.heart-icon');     // Иконка сердечка

        // Обработка клика по кнопке избранного
        button.addEventListener('click', function () {
            const productId = form.dataset.productId; // Получаем ID товара из data-атрибута

            // Отправка запроса на добавление/удаление
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
                // Обновляем иконку в зависимости от результата
                if (data.status === 'added') {
                    icon.src = '/images/heart-filled.png';  // Товар добавлен в избранное
                    icon.dataset.favorite = 'true';
                } else if (data.status === 'removed') {
                    icon.src = '/images/heart.png';         // Товар удалён из избранного
                    icon.dataset.favorite = 'false';
                }
            })
            .catch(error => console.error('Ошибка:', error)); // Обработка ошибок
        });
    });
});