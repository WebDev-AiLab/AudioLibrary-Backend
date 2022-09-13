window.addEventListener('load', () => {
    const plays_label = document.querySelector('.field-plays_count div');
    if (plays_label) {
        const button = document.createElement('button');
        button.type = 'button';
        button.innerText = 'Clear';
        button.classList.add('asg__button-plays');

        button.addEventListener('click', () => {
            if (confirm('Warning! This action cannot be undone. Do you want to continue?')) {
                const url = window.location.pathname.split('/');
                const id = url[url.length - 3];
                fetch(`/tracks/${id}/plays/`, {
                    method: 'DELETE',
//                    headers: {
//                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
//                    }
                }).then(response => {
                    const _plays_label = plays_label.querySelector('div.readonly');
                    if (_plays_label) {
                        _plays_label.innerHTML = '0';
                    }
                }).catch(e => console.error(e))
            }
        });

        plays_label.appendChild(button);
    }
});