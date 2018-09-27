from django.test import TestCase

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

def main(service=None):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])
    #
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print('{0} ({1})'.format(item['name'], item['id']))

    # file_metadata = {'name': 'photo.jpg',
    #                  'parents':['1e9akPcA1oNIq2en4dCGjg0MU9Dh1wydD']}
    # media = MediaFileUpload( 'image.jpeg',
    #                          )
    # file_x = service.files().create( body=file_metadata,
    #                                  media_body=media,
    #                                  fields='id' ).execute()
    # print('File ID: %s' % file_x.get( 'id' ))
    result = service.files().get(fileName="photo.jpg").execute()
    print(repr(result))

if __name__ == '__main__':
    main()