from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .googleapiutils import *

class ListFilesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        service = token_authentication(request)
        if service:
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])
            return HttpResponse(items)
        else: return HttpResponse('Auth Error')
        
class CreateFolderView(View):
    def get(self, request, *args, **kwargs):
        service = token_authentication(request)
        folder = create_folder_if_not_exists(service, 'Charmschool')
        return HttpResponse('Folder ID: %s' % folder.get('id'))

class UploadFileView(TemplateView):
    template_name = 'charmschool/gdtesting/uploadfile.html'
    def post(self, request, *args, **kwargs):
        service = token_authentication(request)
        files = request.FILES.getlist('files')
        folder = create_folder_if_not_exists(service, 'Charmschool')
        id_list = upload_user_contents(service,files, request, folder.get('id'))
        print(id_list)
        return HttpResponse('Uploaded Successfully!!')


