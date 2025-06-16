document.addEventListener('DOMContentLoaded', () => {
    // === Блок инициализации элементов и функций для переключения темы и меню ===
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const favorite = document.querySelector('.icon');
    const body = document.body;

    // Функция для смены иконок в зависимости от выбранной темы
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = staticPaths.darkTheme;
            shoppingBagIcon.src = staticPaths.darkBag;
            accountIcon.src = staticPaths.darkAccount;
            favorite.src = staticPaths.darkIcon;
        } else {
            themeToggle.src = staticPaths.lightTheme;
            shoppingBagIcon.src = staticPaths.lightBag;
            accountIcon.src = staticPaths.lightAccount;
            favorite.src = staticPaths.lightIcon;
        }
    }

    // Применение сохранённой темы из localStorage при загрузке страницы
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        updateIcons(true);
    } else {
        updateIcons(false);
    }

    // Добавление обработчиков клика к пунктам меню для переключения активного состояния
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
        });
    });

    // Обработчик переключения темы по клику на кнопку переключателя
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // === Блок обработки форм добавления/удаления товара в избранное ===
    const favoriteForms = document.querySelectorAll('.favorite-form');

    favoriteForms.forEach(form => {
        const button = form.querySelector('.favorite-btn');
        const icon = form.querySelector('.heart-icon');

        button.addEventListener('click', function () {
            const productId = form.dataset.productId;

            // Отправка POST-запроса для изменения статуса избранного товара
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
                // Обновление иконки и атрибутов в зависимости от ответа сервера
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