var messageBody = document.querySelector('#messages');
messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

function scrollToBottom() {
    messageBody.scrollTop = messageBody.scrollHeight;
}

function removeImage() {
    const uploadedImage = document.getElementById('uploaded-image');
    
    if (uploadedImage) {
        uploadedImage.remove();
    }
}

function readURL(input) {

    if (input.files && input.files[0]) {
        const imageDiv = document.getElementById('image-append');
        // Create an image element
        const imageElement = document.createElement('img');
        imageDiv.appendChild(imageElement);
        // Set an id for the image element
        imageElement.setAttribute('id', 'uploaded-image');

        var reader = new FileReader();

        reader.onload = function (e) {
            // Set the 'src' attribute of the image element
            imageElement.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}