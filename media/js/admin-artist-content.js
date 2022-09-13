window.addEventListener('load', () => {
    const handleCheckbox = status => {
        const box = document.querySelector('.field-voice_type');
        if (status) {
            box.classList.remove('hide');
        } else {
            box.classList.add('hide');
        }
    }

    const checkbox = document.getElementById('id_singer');
    checkbox.addEventListener('change', () => {
        handleCheckbox(!!checkbox.checked);
    });

    handleCheckbox(!!checkbox.checked);
});

window.addEventListener('load', () => {
    const handleCheckbox = status => {
        const box = document.querySelector('.field-wikipedia');
        if (status) {
            box.classList.remove('hide');
        } else {
            box.classList.add('hide');
        }
    }

    const checkbox = document.getElementById('id_is_wikipedia');
    checkbox.addEventListener('change', () => {
        handleCheckbox(!!checkbox.checked);
    });

    handleCheckbox(!!checkbox.checked);
});

window.addEventListener('load', () => {
    const handleCheckbox = status => {
        const box = document.querySelector('.field-daw');
        if (status) {
            box.classList.remove('hide');
        } else {
            box.classList.add('hide');
        }
    }

    const checkbox = document.getElementById('id_is_daw');
    checkbox.addEventListener('change', () => {
        handleCheckbox(!!checkbox.checked);
    });

    handleCheckbox(!!checkbox.checked);
});