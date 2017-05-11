import csv
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from .process import SubConverter
from os import path

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def upload_file(request):
    errors = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            req_file = request.FILES['file']
            filesize = req_file.size
            if filesize > 300000:
                errors.append(sizeof_fmt(filesize) + ' is too big of a file')
            else:
                resultlines = SubConverter(req_file)
                if not resultlines:
                    errors.append('Failed to process the file. Wrong format?')
                if resultlines:
                    response_content = '\r\n'.join(resultlines)
                    response = HttpResponse(response_content, content_type='text/plain')
                    req_file_name = path.splitext(req_file.name)[0]
                    req_file_name = req_file_name.replace(' ', '_')
                    disp_str = 'attachment; filename="%s.srt"' % req_file_name
                    response['Content-Disposition'] = disp_str
                    return response
    else:
        form = UploadFileForm()
    return render(request, 'converter/upload.html', {'form': form, 'errors': errors})
