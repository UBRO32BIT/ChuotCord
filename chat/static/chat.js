var messageBody = document.querySelector('#messages');
messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

function scrollToBottom() {
    messageBody.scrollTop = messageBody.scrollHeight;
}

function removeImage() {
    const imageDiv = document.getElementById('image-append');
    const uploadedImage = document.getElementById('uploaded-image');
    const removeLink = imageDiv.querySelector('a'); // Get the remove link

    // Remove the uploaded image
    if (uploadedImage) {
        imageDiv.removeChild(uploadedImage);
    }

    // Remove the remove link
    if (removeLink) {
        imageDiv.removeChild(removeLink);
    }
}

function readURL(input) {
    if (input.files && input.files[0]) {
        const imageDiv = document.getElementById('image-append');
        const uploadedImage = imageDiv.querySelector('#uploaded-image');
        //console.log(uploadedImage == null);
        // Check if the imageDiv already has child elements
        if (!uploadedImage) {
            // Create an image element
            const imageElement = document.createElement('img');
            imageDiv.appendChild(imageElement);
            imageElement.setAttribute('id', 'uploaded-image');

            var reader = new FileReader();

            reader.onload = function (e) {
                // Set the 'src' attribute of the image element
                imageElement.src = e.target.result; 
            };
            reader.readAsDataURL(input.files[0]);

            // Create and append the remove image link
            const removeLink = document.createElement('a');
            removeLink.className = 'fa fa-window-close';
            removeLink.setAttribute('aria-hidden', 'true');

            // Attach the removeImage() function to the link's click event
            removeLink.addEventListener('click', removeImage);

            // Append the link to the imageDiv
            imageDiv.appendChild(removeLink);
        }
    }
}