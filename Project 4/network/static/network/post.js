document.addEventListener('DOMContentLoaded', function(){
    document.querySelectorAll('button').forEach(button => {
        button.onclick = () => {
            //Execute genEdit function when edit button pressed
            if (button.className == 'btn btn-light btn-edit') {
                genEditing(button);
            //Execute like function when like button pressed
            } else if (button.className == 'btn btn-primary like') {
                like(button);
            }
        }
    });
});

function genEditing(button) {
    let parentElement = button.parentElement;
    let contentElement = parentElement.querySelector('p');

    //MAKE EDIT BUTTON AND TEXT INVISIBLE 
    button.style.display = 'none';
    contentElement.style.display = 'none';

    //CREATING AND ASSIGNING VALUES TO THE TEXTAREA ELEMENT
    let textarea = document.createElement("textarea");
    textarea.rows = 4;
    textarea.className = 'form-control';
    textarea.value = contentElement.innerText;
    parentElement.append(textarea);

    //CREATE SAVE BUTTON AND DISPALY IT

    let saveButton = document.createElement("button");
    saveButton.type = 'button';
    saveButton.className = 'btn btn-info btn-save';
    saveButton.innerText = 'Save';
    parentElement.append(saveButton);

    //TRIGGERING EDITPOST FUNCTION WHEN BUTTON PRESSED

    saveButton.onclick = () => {
        //SETTING APPEARING OF ELEMENTS
        textarea.style.display = 'none';
        saveButton.style.display = 'none';
        contentElement.style.display = 'block';
        contentElement.style.display = 'block';
        button.style.display = 'block';

        let post_content = textarea.value;
        let post_id = button.dataset.postid;

        fetch('/post', {
            method: 'PUT',
            body: JSON.stringify({ post_content, post_id, action: 'edit' })
        }).then(response => {
            if (response.status == 200) {
                //Updating was succesfull
                contentElement.innerText = textarea.value;
            } 
            return response.json();
        }).then(result => {
            if (typeof result['error'] !== 'undefined') {
                contentElement.style.color = 'red';
                contentElement.innerText = result['error'];
            } else {
                console.log('Message: ' + result['message']);
            }
        });

    }

}

function like(button) {
    let post_id = button.dataset.postid;
    fetch('/post', {
        method: 'PUT',
        body: JSON.stringify({post_id, action: 'like' })
    }).then(response => {
        if (response.status == 201) {
            changeLikeContent(button, true);
        } else if (response.status == 200){
            changeLikeContent(button, false);
        }
        return response.json();
    }).then(result => {
        console.log(result);
    });
}

function changeLikeContent(button, action) {
    let span = button.querySelector('span');
    let likes = button.getElementsByClassName('badge badge-light')[0];
    let numerOfLikes = parseInt(likes.innerText);
    if (action) {
        span.classList.add('liked');
        numerOfLikes++;
    } else {
        span.classList.remove('liked');
        numerOfLikes--;
    }
    likes.innerText = numerOfLikes;
}