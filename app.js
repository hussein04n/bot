const apiKey = 'b346d93b5409a568e0a1';  // استبدل بـ API Key الخاص بك من Pinata
const apiSecret = 'c2ce60ca37561f15d8b7b70faccd042a9d9bfb1d79ca87ff9855c0c7dc4bfeab';  // استبدل بـ Secret Key الخاص بك من Pinata

document.getElementById('uploadButton').addEventListener('click', function() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        uploadFileToIPFS(file);
    } else {
        alert('يرجى اختيار ملف!');
    }
});

function uploadFileToIPFS(file) {
    document.getElementById('statusMessage').textContent = 'جاري رفع الملف إلى IPFS...';

    const formData = new FormData();
    formData.append('file', file);

    const options = {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${apiKey}`,
        },
        body: formData,
    };

    // رفع الملف إلى Pinata (IPFS)
    fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', options)
        .then(response => response.json())
        .then(data => {
            console.log('تم رفع الملف بنجاح:', data);
            document.getElementById('statusMessage').textContent = `تم رفع الملف! الرابط: https://gateway.pinata.cloud/ipfs/${data.IpfsHash}`;
        })
        .catch(error => {
            console.error('فشل رفع الملف:', error);
            document.getElementById('statusMessage').textContent = 'فشل رفع الملف!';
        });
}
