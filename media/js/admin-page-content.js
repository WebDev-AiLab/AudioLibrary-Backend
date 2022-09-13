window.addEventListener('load', () => {
    const changeVisibility = (solution, index) => {
        const section = document.querySelector(`#page_form > div > fieldset:nth-of-type(${index})`);
        if (!section) return console.error('Bug : section not found');

        if (solution) {
            section.classList.remove('hide');
        } else {
            section.classList.add('hide');
        }
    }
    // changes visibility
    const setState = type => {
        changeVisibility(type === 'Text' || type === 'Mixed', 2);
        changeVisibility(type === 'Frontend' || type === 'Mixed', 3);
    }
    // checks the type
    const solution = type => type === 'Text';

    const selector = document.getElementById('id_type');
    if (!selector) {
        return console.error('Bug : no type selector found');
    }

    selector.addEventListener('change', () => {
        setState(selector.value);
    });

    // and do the same by default
    setState(selector.value);
});