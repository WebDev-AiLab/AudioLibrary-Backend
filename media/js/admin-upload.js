window.$ = $ = django.jQuery;

window.addEventListener('load', () => {
    const link = document.querySelector('.addlink');
    link.classList.add('hide');
    document.title = "Upload a file | Django administration";

    /* import artsts */
    const uploadCSVInput = document.getElementById('file-0.3893264303699131');
    uploadCSVInput && uploadCSVInput.addEventListener('change', e => {
        const file = e.target.files[0];
        if (!file) {
            return console.warn('no files selected');
        }
        processCSV(file);
    });

    /* import tracks */
    const uploadMP3Input = document.getElementById('file-0.3893264303699132');
    uploadMP3Input && uploadMP3Input.addEventListener('change', e => {
        const files = e.target.files;
        if (!files || !files.length) {
            return console.warn('no files selected');
        }
        processMP3([...files]);
    });
});

const processMP3 = files => {

    const table = document.querySelector('.input-file__table').classList.remove('hide');
    const tbody = document.getElementById('js-mp3-tbody');
    const info = document.querySelector('.input-file__info');

    files.forEach(file => {
        const name = file.name.trim();
        const size = bytesToKMB(file.size);

        const td1 = document.createElement('td');
        td1.innerText = name;
        const td2 = document.createElement('td');
        td2.innerText = size;
        const td3 = document.createElement('td');
        td3.innerText = 'Processing...';
        td3.classList.add('js-status');
        const tr = document.createElement('tr');
        tr.id = slugify(name);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);

        tbody.appendChild(tr);
    });

    (async () => {
        const queueSize = 4;
        for (let i = 0; i < files.length; i = i + queueSize) {
            const promises = [];
            for (let j = i; j < i + queueSize; j++) {
                if (!files[j]) continue;
                promises.push(fetch('/tracks/', {
                    method: 'POST',
                    body: toFormData({file: files[j]})
                })
                .then(result => {
                    const tr = document.getElementById(slugify(files[j].name));
                    const td = tr.querySelector('.js-status');
                    if (result && result.status && (result.status === 201 || result.status === 200)) {
                        td.innerText = 'Done';
                    } else {
                        td.innerText = 'Error';
                    }
                    return true;
                }));
            }
            await Promise.all(promises);
            info.innerText = `${Math.min(i + queueSize, files.length)} of ${files.length} rows processed`;
        }

        alert('Completed');
    })();
}

const processCSV = file => {
    const reader = new FileReader();
    reader.onload = e => {
        const text = e.target.result;
        const body = text.split(/\r?\n/).slice(1);
        const artistList = [];
        const table = document.querySelector('.input-file__table').classList.remove('hide');
        const tbody = document.getElementById('js-csv-tbody');
        const info = document.querySelector('.input-file__info');
        for (let i = 0; i < body.length; i++) {
            let artistName = body[i].split(/[,;]+/)[1];
            if (!artistName) {
                continue;
            }
            artistName = artistName.trim();
            artistList.push(artistName);
            const tr = document.createElement('tr');
            tr.id = slugify(artistName);
            const td1 = document.createElement('td');
            td1.innerText = artistName;
            tr.appendChild(td1);
            const td2 = document.createElement('td');
            td2.innerText = "Processing...";
            td2.classList.add('js-status');
            tr.appendChild(td2);
            tbody.appendChild(tr);
        }

        let counter = 0;

       (async () => {
            for (let i = 0; i < artistList.length; i++) {
                const result = await fetch('/tracks/artists/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({artist: artistList[i]})
                }).catch(e => console.error);
                const tr = document.getElementById(slugify(artistList[i]));
                const td = tr.querySelector('.js-status');
                if (result && result.status && (result.status === 201)) {
                    td.innerText = 'Done';
                } else if (result && result.status && (result.status === 200)) {
                    td.innerText = 'Skipped';
                } else {
                    td.innerText = 'Error';
                }

                info.innerText = `${++counter} of ${artistList.length} rows processed`;
            }

            alert('Completed');
       })();
    }
    reader.readAsText(file);
}

const slugify = string => {
    return string.toLowerCase().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/^-+|-+$/g, '');
}

const bytesToKMB = bytes => {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if (bytes === 0) return 'n/a'
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)), 10)
    if (i === 0) return `${bytes} ${sizes[i]}`
    return `${(bytes / (1024 ** i)).toFixed(1)} ${sizes[i]}`
}

const toFormData = params => {
    const formData = new FormData();
    for (let i in params) {
        formData.append(i, params[i]);
    }
    return formData;
}