document.getElementById('fileInput').addEventListener('change', function(event) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = ''; // مسح المحتوى السابق

    Array.from(event.target.files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');

        let icon;
        if (file.name.endsWith('.pdf')) {
            icon = document.createElement('div');
            icon.classList.add('pdf-icon');
        } else {
            icon = document.createElement('div');
            icon.classList.add('folder-icon');
        }

        const fileName = document.createElement('div');
        fileName.classList.add('file-name');
        fileName.textContent = file.name;

        fileItem.appendChild(icon);
        fileItem.appendChild(fileName);
        fileList.appendChild(fileItem);
    });
});
