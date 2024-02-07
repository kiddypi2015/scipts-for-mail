## Documentation
***
1. The application needs a json file from the Google that enables us to talk to the workspace APIs.
2. Follow the [steps](https://developers.google.com/gmail/api/quickstart/python) to create the account that will communicate to the APIs. 
3. Change the `.json` file name to `client-secret.json` and move the credential file to the root of the project.
4. Then install the requirements using
   ```bash
   pip install --upgrade -r requirements.txt
   ```
6. Then run the project in windows 
   ```powershell
   python main.py
   ```
   (or) In Linux
   ```bash
   python3 main.py
   ```
7. Run the main file in the root of the project. 
8. Approve the permissions for using the Google Workspace application for that account.