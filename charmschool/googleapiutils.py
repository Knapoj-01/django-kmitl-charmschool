from io import BytesIO
from django.contrib.sites.shortcuts import get_current_site
from allauth.socialaccount.models import SocialToken
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials

def token_authentication(request):
    # Token auth
        socialaccount = request.user.socialaccount_set.first()
        socialapp = get_current_site(request).socialapp_set.first()
        socialtoken = SocialToken.objects.filter(
            account=socialaccount, app = socialapp
            ).first()
        creds = Credentials(
            token= socialtoken.token,
            refresh_token= socialtoken.token_secret,
            token_uri='https://oauth2.googleapis.com/token',
            client_id = socialapp.client_id, 
            client_secret=socialapp.secret
            )
        if not creds.valid:
            return False
        else:
            return build('drive', 'v3', credentials=creds), creds
def modify_permissions(service, file_id):
    domain_permission = {
        'type': 'domain',
        'role': 'reader',
        'domain': 'kmitl.ac.th'
    }
    service.permissions().create(
            fileId=file_id,
            body=domain_permission,
            fields='id',
    ).execute()
def create_folder_if_not_exists(service, folder_name: str, parent_folder_id = None):
    response = service.files().list(
            q="mimeType = 'application/vnd.google-apps.folder' and name = '%s'" % folder_name,
            spaces='drive', fields='files(id, name)').execute()
    folder = response.get('files', [])
    if not folder:
        file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        }
        if parent_folder_id:
            file_metadata.update({'parents' : [parent_folder_id]})
        folder = service.files().create(body=file_metadata, fields='id').execute()
    else: folder = folder[0]
    return folder

def upload_user_contents(service, files, request, parent_folder_id):
    id_list = []
    for file in files:
        filename = '{0}_{1}'.format(str(request.user.username), file.name)
        file_metadata = { 
                'name' : filename,
                'parents' : [parent_folder_id]
            }
        fh = BytesIO(file.read())
        media = MediaIoBaseUpload(fh, mimetype=file.content_type)
        gd_file = service.files().create(
            body=file_metadata, media_body=media, fields='id').execute()
        modify_permissions(service, gd_file.get('id'))
        id_list.append({'name': filename, 'id' : gd_file.get('id')})
    return id_list