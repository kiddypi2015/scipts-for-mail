# project imports
from auth.main import get_creds
from resume_scripts.main import get_top_5_messages
from time import sleep


def main():
    creds = get_creds()
    while True:
        get_top_5_messages(creds=creds)
        # sleep(300)
        break


if __name__ == "__main__":
    main()
