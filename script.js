document.getElementById('fileInput').addEventListener('change', function(event) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = ''; // مسح المحتوى السابق

    Array.from(event.target.files).forEach(file => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');

        let icon;
        const fileName = document.createElement('div');
        fileName.classList.add('file-name');
        fileName.textContent = file.name;

        if (file.name.endsWith('.pdf')) {
            icon = document.createElement('div');
            icon.classList.add('pdf-icon');
            icon.textContent = "📄"; // أيقونة PDF
        } else {
            icon = document.createElement('div');
            icon.classList.add('folder-icon');
            icon.textContent = "📂"; // أيقونة مجلد
        }

        fileItem.appendChild(icon);
        fileItem.appendChild(fileName);
        fileList.appendChild(fileItem);
    });
});
