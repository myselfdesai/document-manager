from django.shortcuts import render

from rest_framework import viewsets,status, decorators
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from cryptography.hazmat.primitives import hashes

from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from ..models import FileVersion
from .serializers import FileVersionSerializer, FileUploadSerializer, UserSerializer

import base64
import os

class FileUploadViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        user = request.user

        # Calculate hash using cryptography
        digest = hashes.Hash(hashes.SHA256())
        for chunk in file.chunks():
            digest.update(chunk)
        hashed_content = base64.b64encode(digest.finalize()).decode()


        # Check if a file with the same hash already exists for the user
        existing_file = FileVersion.objects.filter(
            content_hash=hashed_content, user=user
        ).first()

        if existing_file:
            # Create a new version
            new_version = FileVersion.objects.create(
                content_hash=hashed_content,
                file_name=file.name,
                version_number=existing_file.version_number + 1,
                user=user,
            )
        else:
            # Create a new file record and first version
            new_file = FileVersion.objects.create(
                content_hash=hashed_content,
                file_name=file.name,
                version_number=1,
                user=user,
            )

            # Store actual file content based on your storage solution (local filesystem)
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/', hashed_content)
           
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads/', os.path.basename(hashed_content))
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

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
