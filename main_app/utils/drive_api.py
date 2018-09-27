#!/usr/bin/python
# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload, MediaUpload
from httplib2 import Http
from oauth2client import file, client, tools
from resume_parser.settings import BASE_DIR
import io

# If modifying these scopes, delete the file token.json.

SCOPES = 'https://www.googleapis.com/auth/drive'


class GoogleDrive:
    """

    """

    def __init__(self):
        store = file.Storage(BASE_DIR
                              + '/main_app/Constants/drive_config.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(BASE_DIR
                                                  + '/main_app/Constants/credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        self.service = build('drive', 'v3',
                             http=creds.authorize(Http()))

    def create_folder(self):
        file_metadata = {'name': 'Invoices',
                         'mimeType': 'application/vnd.google-apps.folder'}

        folder = self.service.files().create(body=file_metadata,
                                             fields='id').execute()

        print('Folder ID: %s' % folder.get('id'))
        return folder.get('id')

    def upload_file(self, file_name, media, folder_id=None):
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        fd = media.file
        media = MediaIoBaseUpload(fd, mimetype=media.content_type)
        file_x = self.service.files().create(body=file_metadata,
                                             media_body=media,
                                             fields='id').execute()
        file_id = file_x.get('id')
        print('File ID: {file_id}'.format(file_id=file_id))
        file_url = "https://drive.google.com/file/d/" + file_id + '/view'
        return file_id, file_url

    def get_fileslist(self):

        # Call the Drive v3 API

        results = \
            self.service.files().list(fields='nextPageToken, files(id, name, url)'
                                      ).execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print('{0} ({1})'.format(item['name'], item['id']))

        return items

    def get_file(self, file_id):
        result = self.service.files().get(fileId=file_id).execute()
        print(repr(result))
        return result

    def download_file(self, file_id):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            (status, done) = downloader.next_chunk()
            print('Download %d%%.' % int(status.progress() * 100))

        return True