let dropArea = document.getElementById('drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false)
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false)
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false)
});

function highlight(e) {
    dropArea.classList.add('border-solid')
    dropArea.classList.remove('border-dashed')
}

function unhighlight(e) {
    dropArea.classList.remove('border-solid')
    dropArea.classList.add('border-dashed')
}

dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {

    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);

}

function handleFiles(files) {
    ([...files]).forEach(uploadFile);
}

function uploadFile(file) {
    // Here you would write code to handle the file upload, like sending it to a server
    var newDiv = document.createElement("div");
    newDiv.innerHTML =  file.name
    dropArea.appendChild(newDiv)
    console.log('Uploading', file.name);
}
