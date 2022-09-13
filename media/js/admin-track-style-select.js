window.addEventListener('load', () => {

    const selectGenre = document.getElementById('id_genre');
    const selectStyle = document.getElementById('id_style');

    const clearStyleSelect = () => {
        // clear selection first
        selectStyle.value = "";
        // and also delete all options except first one
        for (let i = 0; i < selectStyle.options.length; i++) {
            if (selectStyle.options[i].value) {
                selectStyle.removeChild(selectStyle.options[i]);
                i--;
            }
        }
    }

    selectGenre.addEventListener('change', e => {
        clearStyleSelect();
        if (!e.target.value) return false;
        // load options from the server...
        fetch(`/tracks/ajax/styles/?genre=${e.target.value}`)
            .then(response => response.json())
            .then(response => {
                if (response && response.results) {
                    response.results.forEach(item => {
                        const select = document.createElement('option');
                        select.value = item.id;
                        select.innerText = item.name;
                        selectStyle.appendChild(select);
                    });
                }
            })
            .catch(error => console.error(error))
    });

    if (!selectGenre.value) clearStyleSelect();
});