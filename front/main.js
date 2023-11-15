let currSelectedDocumentText;

const filePicker = document.getElementById('file-picker');
const helpButton = document.getElementById('help-button');
const commenceButton = document.getElementById('commence-button');
const kwRefTextContainer = document.getElementById('kw-ref-result');
const mlRefTextContainer = document.getElementById('ml-ref-result');
const serverAddress = "http://localhost:5000";

async function getKwRef(text) {
    return fetch(serverAddress + '/kwabstract', {
        method: 'POST',
        headers: new Headers({
            "Content-Type": "application/json"
        }),
        body: JSON.stringify({ text })
    })
        .then(response => response.text());
}

async function getMlRef(text) {
    return fetch(serverAddress + '/mlabstract', {
        method: 'POST',
        headers: new Headers({
            "Content-Type": "application/json"
        }),
        body: JSON.stringify({ text })
    })
        .then(response => response.text());
}

helpButton.addEventListener('click', () => {
    alert('Выберите файл, автоматическое реферирование которого нужно провести, и нажмите кнопку "Реферировать". ')
});

filePicker.addEventListener('change', function() {
    const fr = new FileReader();
    fr.onload = function() {
        currSelectedDocumentText = fr.result;
        commenceButton.disabled = false;
    }
    fr.readAsText(this.files[0], 'CP1251');
});

commenceButton.addEventListener('click', async () => {
    kwRefTextContainer.innerHTML = await getKwRef(currSelectedDocumentText);
    mlRefTextContainer.innerHTML = await getMlRef(currSelectedDocumentText);
});