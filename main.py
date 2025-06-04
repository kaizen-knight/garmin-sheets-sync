import garminconnect
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


sheet_id = "1SmJwOTNGtnzTTc7w1LF3bRZC46l39nzjkFHd7oDjtdE"
SAMPLE_RANGE_NAME = "Activities!A2:E"

my_garmin = garminconnect.Garmin(email="Jamesknight66@hotmail.co.uk", password="9aBwqecfA5uEWDZ")
my_garmin.login()

few_activities = my_garmin.get_activities(start=0, limit=10)

challenges = my_garmin.get_adhoc_challenges(start=0, limit=1000)

class GoogleSheetsAPI:
    def __init__(self, creds=None):
        self.creds = creds
        self.service = self.authenticate_google_sheets(creds)

    def authenticate_google_sheets(self, creds=None):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/spreadsheets'])
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://www.googleapis.com/auth/spreadsheets'])
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('sheets', 'v4', credentials=creds)

    def write_data_to_sheet(self, data, range_name=SAMPLE_RANGE_NAME):
        try:
            sheet = self.service.spreadsheets()
            body = {
                'values': data
            }
            result = sheet.values().append(
                spreadsheetId=sheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            print(f"{result.get('updates').get('updatedCells')} cells updated.")
        except HttpError as err:
            print(f"An error occurred: {err}")

    def append_values(self, spreadsheet_id, range_name, value_input_option, _values):
      """
      Creates the batch_update the user has access to.
      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
      """
      # pylint: disable=maybe-no-member
      try:
        service = self.service

        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        body = {"values": values}
        result = (
            service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

      except HttpError as error:
        print(f"An error occurred: {error}")
        return error


