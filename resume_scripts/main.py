import base64
import os.path
import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

candidate_name: str
candidate_email: str
position: str
candidate_resume_link: str


def get_top_5_messages(creds):
    global candidate_name, candidate_email, position, candidate_resume_link
    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(
            userId="me",
            includeSpamTrash=False,
            labelIds=["IMPORTANT"],
            maxResults=1
        ).execute()
        messages = results.get("messages")
        for message in messages:
            email_regex = r'<([^>]+)>'

            message_result = service.users().messages().get(
              userId="me",
              id=message.get("id"),
              format="full"
            ).execute()

            name_and_email = message_result.get('payload').get('headers')[16].get('value').split(" ")

            # values to be returned
            candidate_name = name_and_email[0] + name_and_email[1]
            candidate_email = re.search(email_regex, name_and_email[2]).group(1)
            position = message_result.get('payload').get('headers')[19].get('value')

            message_attachment_result = service.users().messages().attachments().get(
                userId='me',
                messageId=message_result.get('id'),
                id=message_result.get('payload').get('parts')[1].get('body').get('attachmentId')
            ).execute()

            # print(message_attachment_result)

            with open(f"../resume/{candidate_name}.pdf", "wb") as f:
                f.write(base64.urlsafe_b64decode(message_attachment_result.get('data').encode('utf-8')))
                f.close()

            # TODO: The file should be uploaded to the google drive and the url should be returned
            candidate_resume_link = upload_resume_to_drive(creds=creds,
                                   candidate_file_name=f"{candidate_name}",
                                   file_name=f"../resume/{candidate_name}.pdf"
                                   )

            if os.path.exists(f"../resume/{candidate_name}.pdf"):
                os.remove(f"../resume/{candidate_name}.pdf")
                print("File deleted!")
            else:
                print("File illa")

    except HttpError as e:
        print("Error", e)


    return (candidate_name,
            candidate_email,
            position,
            candidate_resume_link
            )


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