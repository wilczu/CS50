document.addEventListener('DOMContentLoaded', function(){
    console.log('document loaded!'); //TESTING

    document.querySelectorAll('button').forEach(button => {

        let editButton = button.className == 'btn btn-light btn-edit';

        button.onclick = () => {
            if (editButton) {
                genEditing(button);
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

        if (editPost(textarea.value, button.dataset.postid)) {
            //Updating was succesfull
            contentElement.innerText = textarea.value;
        } else {
            //Error :c
            contentElement.style.color = 'red';
            contentElement.innerText = 'There is a problem with your request, please try again later';
        }

    }

}

function editPost(content, postID) {
    //All info to update this post
    console.log('New content for this post is: ' + content);
    console.log(postID);
    //Return true or false from API
    return true;
}