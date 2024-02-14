from django.shortcuts import render
from django.http import FileResponse

from rest_framework import viewsets,status, decorators
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from ..models import FileVersion
from .serializers import FileVersionSerializer, FileUploadSerializer, UserSerializer

import os
import hashlib

class FileUploadViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        user = request.user

        # Initialize the hash object (SHA-256 in this case)
        hasher = hashlib.sha256()

        file_content = b""
        with file.open('rb') as f:
            # Read the file in chunks to avoid loading the entire file into memory
            for chunk in iter(lambda: f.read(4096), b""):
                file_content += chunk
                # Update the hash with the current chunk
                hasher.update(chunk)

        # Calculate the final hash value
        hashed_content = hasher.hexdigest()

        # Check if a file with the same filename and hash already exists for the user
        existing_file = FileVersion.objects.filter(
            content_hash=hashed_content, user=user, file_name=file.name
        ).first()
        if existing_file:
            return Response({'message': 'File already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a file with the same filename but different hash exists for the user with max version
        existing_file_different_hash = FileVersion.objects.filter(
            user=user, file_name=file.name
        ).exclude(content_hash=hashed_content).order_by('-version_number').first()

        if existing_file_different_hash:
            # File with same filename but different hash exists, create new version
            new_version_number = existing_file_different_hash.version_number + 1
        else:
            # No file with same filename and hash exists, create new file record and first version
            new_version_number = 1

        new_version = FileVersion.objects.create(
            content_hash=hashed_content,
            file_name=file.name,
            version_number=new_version_number,
            user=user,
        )
        # Get the file extension
        _, file_extension = os.path.splitext(file.name)

        # Construct the new filename using the hashed content and the original file extension
        new_filename = hashed_content + file_extension.lower()

        # Store actual file content
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/', new_filename)
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as destination:
                destination.write(file_content)

        return Response({'message': 'File uploaded and stored successfully'}, status=status.HTTP_201_CREATED)


class FileVersionsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        file_versions = FileVersion.objects.filter(user=request.user)
        serializer = FileVersionSerializer(file_versions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            file_version = FileVersion.objects.get(pk=pk, user=request.user)
            serializer = FileVersionSerializer(file_version)
            return Response(serializer.data)
        except FileVersion.DoesNotExist:
            return Response({'message': 'File version not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def download(self, request, pk=None):
        user = request.user
        try:
            file_version = FileVersion.objects.get(pk=pk, user=user)

            # Construct the media path using file_name and content_hash
            file_extension = os.path.splitext(file_version.file_name)[-1].lower()
            media_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f'{file_version.content_hash}{file_extension}')

            if not os.path.exists(media_path):
                return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

            return FileResponse(open(media_path, 'rb'), as_attachment=True, filename=file_version.file_name)

        except FileVersion.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
