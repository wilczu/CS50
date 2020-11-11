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

function display_email(mailID, mailbox) {
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

  //Getting all information about this email and displaying them

  fetch(`emails/${mailID}`)
  .then(response => response.json())
  .then(email => {
    row_content.innerHTML = `
    <h1> <b>Subject:</b> ${email['subject']}</h1> 
    <br> <b>Sender:</b> ${email['sender']} 
    <br> <b>Recipients:</b> ${email['recipients'].toString()}
    <div class="alert alert-primary" role="alert">
      <b>Body:</b> <pre>${email['body']}</pre>
    </div>
    <b>Timestamp:</b> ${email['timestamp']}
    `;

    //Generating button only when the mailbox is not equal to sent view
    if(mailbox != 'sent') {
      //Generating archive button

      const archive_button = document.createElement('button');
      row_controls.append(archive_button);

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
    }

    //Generating reply button
    const reply_button = document.createElement('button');
    reply_button.className = 'btn btn-outline-success btn-block';
    reply_button.textContent = 'Reply to this email';
    row_controls.append(reply_button);

    reply_button.addEventListener('click', ()=> {
      reply_email(email);
    });

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

function reply_email(email) {
  compose_email();

  //Detecting 'Re:' in email and adding it if not found
  let subject = email['subject'];
  if(email['subject'].substring(0,3) != 'Re:') {
    subject = 'Re: ' + email['subject'];
  }

  const formatted_body = `\n\n\n\tOn ${email['timestamp']} ${email['sender']} wrote:\n\t${email['body']}`;

  //Prepopulating input forms from the compose view
  document.querySelector('#compose-body').value = formatted_body;
  document.querySelector('#compose-recipients').value = email['sender'];
  document.querySelector('#compose-subject').value = subject;
}

function archive_mail(mailID, action) {
  fetch(`/emails/${mailID}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: action
    })
  }).then(() => load_mailbox('inbox'));
}

function add_mail(content, status, mailID, mailbox) {
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
    display_email(mailID, mailbox);
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
     //Printing everything on the page     
     for (let i = 0; i < emails.length; i++) {
        add_mail(
          `<div class="row">
            <div class="col-md-4">
              <b>From:</b> ${emails[i]['sender']} 
            </div>
            <div class="col-md-4">
              <b>Subject:</b> ${emails[i]['subject']} 
            </div>
            <div class="col-md-4">
              <b>Date:</b> ${emails[i]['timestamp']} 
            </div>
          </div>`, 
          emails[i]['read'], emails[i]['id'], mailbox
        );
     }
  });


}