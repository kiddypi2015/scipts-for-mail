# project imports
from auth.main import get_creds
from resume_scripts.main import get_top_5_messages
from time import sleep


def main():
    creds = get_creds()
    # TODO: Anytime a new email gets into some label run get_top_candidate function
    # or get the id of the new gmail and send the id to the get email
    while True:
        get_top_5_messages(creds=creds)
        sleep(50000)


if __name__ == "__main__":
    main()
