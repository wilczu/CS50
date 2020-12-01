document.addEventListener('DOMContentLoaded', function(){
    console.log('document loaded!'); //TESTING

    document.querySelectorAll('button').forEach(button => {

        let editButton = button.className == 'btn btn-light btn-edit';
        let likeButton = button.className == 'btn btn-primary like';

        button.onclick = () => {
            if (editButton) {
                genEditing(button);
            } else if (likeButton) {
                like();
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
            if (response.status == 201) {
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

function like() {
    console.log('Like button pressed!'); //DEBUG
    fetch('/post', {
        method: 'PUT',
        body: JSON.stringify({action: 'like' })
    }).then(response => {
        if (response.status == 201) {
            console.log('Post liked!'); //DEBUG
        }
        return response.json();
    }).then(result => {
        if(typeof result['error'] == 'undefined') {
            //Everything went fine, post liked!
            console.log('Everything is okay!');
            console.log('Message: ' + result['message']);
        } else {
            console.log('Error: ' + result['error']);
        }
    });
}