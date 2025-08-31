const isWinter = () => {
    const today = new Date();
    const month = today.getMonth();
    const day = today.getDate();
    if (month === 11) {
        return day >= 20;
    } else if (month === 0) {
        return day <= 20;
    }
    return false;
};

const isValentine = () => {
    const today = new Date();
    return today.getMonth() === 1 && today.getDate() === 14;
};

const createFallingElement = (symbol) => {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = symbol;
    snowflake.style.left = Math.random() * window.innerWidth + 'px';
    snowflake.style.animationDuration = Math.random() * 3 + 1 + 's';
    snowflake.style.fontSize = Math.random() * 10 + 10 + 'px';
    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 5000);
};

let symbol = null;
if (isWinter()) {
    symbol = '❄';
} else if (isValentine()) {
    symbol = '❤️';
}

if (symbol) {
    setInterval(() => createFallingElement(symbol), 100);
}
