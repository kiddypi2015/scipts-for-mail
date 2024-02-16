import base64
import os.path
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from sheets_scripts.main import add_candidate_data_to_sheets
from phone_number_scripts.main import extract_phone_numbers_from_pdf

candidate_name: str
candidate_email: str
position: str
candidate_resume_link: str
candidate_phone_number: str


def get_labels(creds):
    service = build('gmail', 'v1', credentials=creds)

    # List all labels
    labels = service.users().labels().list(userId='me').execute()

    # Extract label names and IDs
    for label in labels['labels']:
        print(f"Label Name: {label['name']}")
        print(f"Label ID: {label['id']}")
        print('-' * 20)


def get_top_5_messages(creds):
    global candidate_name, candidate_email, position, candidate_resume_link, candidate_phone_number
    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(
            userId="me",
            includeSpamTrash=False,
            labelIds=["IMPORTANT"],
            maxResults=1
        ).execute()
        messages = results.get("messages")
        if len(messages) >= 1:
            for message in messages:
                email_regex = r'<([^>]+)>'

                message_result = service.users().messages().get(
                    userId="me",
                    id=message.get("id"),
                    format="full"
                ).execute()

                name_and_email = message_result.get('payload').get('headers')[16].get('value').split(" ")

                # values to be returned
                candidate_name = name_and_email[0] + " " + name_and_email[1]
                candidate_email = re.search(email_regex, name_and_email[-1]).group(1)
                position = message_result.get('payload').get('headers')[19].get('value')

                message_attachment_result = service.users().messages().attachments().get(
                    userId='me',
                    messageId=message_result.get('id'),
                    id=message_result.get('payload').get('parts')[1].get('body').get('attachmentId')
                ).execute()

                with open(f"../resume/{candidate_name}.pdf", "wb") as f:
                    f.write(base64.urlsafe_b64decode(message_attachment_result.get('data').encode('utf-8')))
                    candidate_phone_number = extract_phone_numbers_from_pdf(f"../resume/{candidate_name}.pdf")
                    f.close()

                candidate_resume_link = upload_resume_to_drive(
                    creds=creds,
                    candidate_file_name=f"{candidate_name}",
                    file_name=f"../resume/{candidate_name}.pdf"
                )

                if os.path.exists(f"../resume/{candidate_name}.pdf"):
                    os.remove(f"../resume/{candidate_name}.pdf")
                    print("File deleted!")
                else:
                    print("File not found")

                print("Adding data to sheets...")
                add_candidate_data_to_sheets(
                    creds,
                    candidate_name,
                    candidate_email,
                    position,
                    candidate_resume_link,
                    candidate_phone_number
                )
                print("Added data to sheets.")
                print("Modifying the labels...")
                service.users().messages().modify(
                    userId='me',
                    id=message_result.get('id'),
                    body={
                        'addLabelIds': ["Label_5074791744678395025"],
                        'removeLabelIds': message.get('labelIds')
                    }
                ).execute()
                print("Labels updated.")
        else:
            print("Waiting for more 300 seconds for enough length")
    except HttpError as e:
        print("Error", e)


def upload_resume_to_drive(creds, candidate_file_name, file_name):
    try:
        service = build('drive', 'v3', credentials=creds)
        file_metadata = {'name': candidate_file_name}
        media = MediaFileUpload(file_name, mimetype="application/pdf")
        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded_file.get('id')
        file_link = f'http://drive.google.com/file/d/{file_id}/view'
        return file_link

    except HttpError as e:
        print(e)
