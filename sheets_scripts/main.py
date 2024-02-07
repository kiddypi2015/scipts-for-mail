from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

spreadsheet_id = "1mWg4b7wVXRnIEGGsP1hvr9X9DV3dOmEr2lunqNtEoWI"
range_name = "Sheet1!A1:C1"


def add_candidate_data_to_sheets(creds, candidate_name, candidate_email, position, resume_link):
    try:
        service = build("sheets", "v4", credentials=creds)
        values = [
            [
                candidate_name,
                candidate_email,
                position,
                resume_link
            ],
        ]
        body = {"values": values}
        ((service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
        ).execute())

    except HttpError as error:
        print(f"An error occurred: {error}")
        print(error)
