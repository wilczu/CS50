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

}