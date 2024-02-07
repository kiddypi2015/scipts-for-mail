# project imports
from auth.main import get_creds
from resume_scripts.main import get_top_5_messages
from sheets_scripts.main import add_candidate_data_to_sheets


def main():
    creds = get_creds()
    # TODO: Anytime a new email gets into some label run get_top_candidate function
    # or get the id of the new gmail and send the id to the get email

    candidate_name, candidate_email, candidate_position, resume_link = get_top_5_messages(creds=creds)

    # TODO: The candidates should be added to the sheets using the sheets api
    add_candidate_data_to_sheets(
        creds=creds,
        candidate_name=candidate_name,
        candidate_email=candidate_email,
        position=candidate_position,
        resume_link=resume_link
    )


if __name__ == "__main__":
    main()
