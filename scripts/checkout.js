// === БЛОК: Инициализация страницы и темы ===
document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu-item');
    const themeToggle = document.getElementById('theme-toggle');
    const shoppingBagIcon = document.querySelector('.shopping-bag-icon');
    const accountIcon = document.querySelector('.account-icon');
    const body = document.body;

    // Функция обновления иконок в зависимости от темы
    function updateIcons(isDark) {
        if (isDark) {
            themeToggle.src = 'images/dark_theme.svg';
            shoppingBagIcon.src = 'images/bag_1.svg';
            accountIcon.src = 'images/account_1.svg';
        } else {
            themeToggle.src = 'images/light_theme.svg';
            shoppingBagIcon.src = 'images/bag.svg';
            accountIcon.src = 'images/account.svg';
        }
    }

    // Загрузка сохраненной темы и установка соответствующего состояния
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
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const category = item.querySelector('span').textContent;
            console.log(`Выбрана категория: ${category}`);
        });
    });

    // === БЛОК: Переключение темы при клике на иконку ===
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-theme');
        const isDark = body.classList.contains('dark-theme');
        updateIcons(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
});


// === БЛОК: Обработка отправки формы заказа ===
function handleOrderSubmit(event) {
    event.preventDefault(); // Предотвращаем перезагрузку страницы
    const form = document.getElementById('order-form');
    const message = document.getElementById('success-message');
    form.style.display = 'none';
    message.style.display = 'block';
}


// === БЛОК: Маска ввода номера телефона ===
const phoneInput = document.getElementById("phone");

phoneInput.addEventListener("input", function (e) {
    let value = e.target.value.replace(/\D/g, "");

    if (value.startsWith("8")) {
        value = "7" + value.slice(1);
    }

    if (value.length > 11) value = value.slice(0, 11);

    let formatted = "+7 ";
    if (value.length > 1) formatted += "(" + value.slice(1, 4);
    if (value.length >= 4) formatted += ") " + value.slice(4, 7);
    if (value.length >= 7) formatted += "-" + value.slice(7, 9);
    if (value.length >= 9) formatted += "-" + value.slice(9, 11);

    e.target.value = formatted;
});

// === БЛОК: Очистка номера перед отправкой формы ===
document.querySelector("form").addEventListener("submit", function(e) {
    let raw = phoneInput.value.replace(/\D/g, '');
    phoneInput.value = '+7' + raw.slice(1);
});


// === БЛОК: Всплывающие подсказки при выборе доставки и оплаты ===
document.addEventListener('DOMContentLoaded', function () {
    const deliverySelect = document.getElementById('delivery-method');
    const tooltip = document.getElementById('pickup-tooltip');
    const paymentTooltip = document.getElementById('pickup');

    // Подсказка при выборе самовывоза
    if (deliverySelect && tooltip) {
        deliverySelect.addEventListener('mouseover', function () {
            if (deliverySelect.value === 'pickup') {
                tooltip.style.display = 'block';
            }
        });

        deliverySelect.addEventListener('mouseout', function () {
            tooltip.style.display = 'none';
        });

        deliverySelect.addEventListener('change', function () {
            tooltip.style.display = 'none';
        });
    } else {
        console.error('Элемент deliverySelect или tooltip не найден в DOM!');
    }

    // Подсказка при выборе СДЭК ПВЗ
    if (deliverySelect && paymentTooltip) {
        deliverySelect.addEventListener('mouseover', function () {
            if (deliverySelect.value === 'cdek_pvz') {
                paymentTooltip.style.display = 'block';
            }
        });

        deliverySelect.addEventListener('mouseout', function () {
            paymentTooltip.style.display = 'none';
        });

        deliverySelect.addEventListener('change', function () {
            paymentTooltip.style.display = 'none';
        });
    } else {
        console.error('Элемент paymentSelect или paymentTooltip не найден в DOM!');
    }
});