from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from file_app.models import File
import os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    file = request.FILES['file']
    if file.content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
        return Response({'error': 'File type not supported'}, status=400)
    category = request.POST.get('category')
    subject = request.POST.get('subject')
    uploaded_file = File.objects.create(file=file, category=category, subject=subject)
    return Response({'id': uploaded_file.id})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request):
    file_id = request.GET.get('id')
    file = get_object_or_404(File, id=file_id)
    filepath = file.file.url.lstrip('/')
    file.delete()
    if os.path.isfile(filepath):
        os.remove(filepath)
    return HttpResponse(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_file(request):
    file_id = request.GET.get('id')
    if file_id:
        file = get_object_or_404(File, id=file_id)
        return Response({'file': file.file.url, 'category': file.category, 'subject': file.subject})
    else:
        tags = request.GET.get('tags')
        if tags:
            tags_dict = dict(tag.strip().split(':') for tag in tags.strip('{}').split(','))
            files = File.objects.filter(**tags_dict)
        else:
            files = File.objects.all()
        files_data = [{'id': f.id, 'file': f.file.url, 'category': f.category, 'subject': f.subject} for f in files]
        return Response(files_data)

