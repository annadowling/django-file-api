from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import File
import os


# Tests for file apis in views.py
class FileAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = 'personal'
        self.subject = 'python'
        self.file = open('files/test.pdf', 'w+')
        self.file2 = open('files/test.txt', 'w+')

    def test_upload_file_correct_format(self):
        self.client.force_authenticate(user=self.user)

        # Upload file with metadata
        url = reverse('upload_file')
        data = {'file': self.file, 'category': self.category, 'subject': self.subject}
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(File.objects.get().category, self.category)
        self.assertEqual(File.objects.get().subject, self.subject)

        # Retrieve file with id
        url = reverse('get_file') + '?id=' + str(File.objects.get().id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve file with metadata tags
        url = reverse('get_file') + '?tags={category:personal}'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_file_wrong_format(self):
        self.client.force_authenticate(user=self.user)

        # Upload file without metadata
        url = reverse('upload_file')
        data = {'file': self.file2}
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
