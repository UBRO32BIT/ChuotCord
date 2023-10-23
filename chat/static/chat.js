document.querySelector('emoji-picker')
  .addEventListener('emoji-click', event => {
    const messageInput = document.getElementById('text-input');
    messageInput.value += event.detail.unicode; 
});


let pickerVisibility = false; 
var messageBody = document.querySelector('#messages');
messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;

function scrollToBottom() {
    messageBody.scrollTop = messageBody.scrollHeight;
}

// Click anywhere except the emoji picker div to close the picker
document.body.onclick = (e) => {
    if (e.target.matches("#emoji-button, #emoji-button *")) {
        return;
    }
    if (pickerVisibility) {
        togglePicker();
    }
    console.log("body clicked!");
}
document.querySelector('#emoji-picker').onclick = (e) => {
    e.stopPropagation();
}

// Remove image review in file input
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
    // Clear input files container
    while (fileInput.files.length > 0) {
        fileInput.value = null;
    }
}
fileInput.onchange = () => {
    readURL();
}
function readURL() {
    if (fileInput.files && fileInput.files[0]) {
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
            reader.readAsDataURL(fileInput.files[0]);

            // Create and append the remove image link
            const removeLink = document.createElement('a');
            removeLink.className = 'fa fa-window-close';
            removeLink.setAttribute('aria-hidden', 'true');

            // Attach the removeImage() function to the link's click event
            removeLink.addEventListener('click', function() {
                removeImage();
            });

            // Append the link to the imageDiv
            imageDiv.appendChild(removeLink);
        }
    }
}

const userTypingList = new Set();
function setUserTyping() {
    if (userTypingList.size !== 0) {
        typingElement = document.querySelector('#user-typing');
        let users = '';
        for (const user of userTypingList) {
            users += user + ', ';
        }
        typingElement.textContent = users + 'is typing....';
    }
    else {
        typingElement.textContent = '';
    }
}

function togglePicker() {
    const imageDiv = document.getElementById('emoji-picker');
    if (pickerVisibility) {
        imageDiv.style.visibility = "hidden";
    } 
    else imageDiv.style.visibility = "visible";
    pickerVisibility = !pickerVisibility;
}