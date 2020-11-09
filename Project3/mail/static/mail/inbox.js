document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //Sending email when button is pressed
    document.querySelector('#send-email').onclick = () => {
      const recipients = document.querySelector('#compose-recipients').value;
      const subject = document.querySelector('#compose-subject').value;
      const body = document.querySelector('#compose-body').value;

        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: recipients,
                subject: subject,
                body: body
            })
        })
        .then(response => {
          if(response.status == 201) { 
            return response.json()
          } else {
            throw Error(response.statusText);
          }
        }).then(result => {
          console.log(result);
          load_mailbox('sent');
        })

        return false;
    }

}

function display_email(mailID) {
  //Show simgle email views and hide other elements
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

  //Reseting content
  document.querySelector('#single-email-view').innerHTML = '';

  //generate bootstrap grid
  const row_div = document.createElement('div');
  row_div.className = 'row';

  const row_content = document.createElement('div');
  row_content.className = 'col-md-8';
  row_div.append(row_content);

  const row_controls = document.createElement('div');
  row_controls.className = 'col-md-4';
  row_div.append(row_controls);

  //Generating archive button

  const archive_button = document.createElement('button');
  row_controls.append(archive_button);

  //Getting all information about this email and displaying them

  fetch(`emails/${mailID}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    row_content.innerHTML = `<b>Sender:</b> ${email['sender']} 
    <br> <b>Subject:</b> ${email['subject']} 
    <br> <b>Recipients:</b> ${email['recipients'].toString()}
    <br> <b>Body:</b> ${email['body']}
    <br> <b>Timestamp:</b> ${email['timestamp']}
    `;

    //Check if email is archived and change content of a button

    if (email['archived']) {
      archive_button.className = 'btn btn-outline-light btn-block';
      archive_button.textContent = 'Unarchive it';

      archive_button.addEventListener('click', () => {
        archive_mail(mailID, false);
      });

    } else {
      archive_button.className = 'btn btn-outline-info btn-block';
      archive_button.textContent = 'Archive it';

      archive_button.addEventListener('click', () => {
        archive_mail(mailID, true);
      });

    }

    document.querySelector('#single-email-view').append(row_div);
  });

  //Changing the status of read to true for this mail
  
  fetch(`/emails/${mailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}

function archive_mail(mailID, action) {
  fetch(`/emails/${mailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: action
    })
  }).then(() => load_mailbox('inbox'));
}

function add_mail(content, status, mailID) {
  //Create new email div element
  const email = document.createElement('div');
  email.className = 'mail-compotent';
  email.innerHTML = content;

  //Change background of mail element
  if (status) {
    email.setAttribute("style", "background-color: #212121;");
  } else {
    email.setAttribute("style", "background-color: white;");
  }
  //Event listener to handle pressing on the email box
  email.addEventListener('click', () => {
    display_email(mailID);
  });
  //Adding this email to DOM
  document.querySelector('#emails-view').append(email);
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  //Talking to the API to get data to display

  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
     console.log(emails)
     //Printing everything on the page     
     for (let i = 0; i < emails.length; i++) {
        add_mail(
          `<b>From:</b> ${emails[i]['sender']} 
          <br> <b>Subject:</b> ${emails[i]['subject']} 
          <br> <b>Timestamp:</b> ${emails[i]['timestamp']} <br>
          `, emails[i]['read'], emails[i]['id']
        );
     }
  });


}