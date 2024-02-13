from rest_framework import serializers

from ..models import FileVersion, User


from rest_framework import serializers
from ..models import FileVersion

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        return FileVersion.objects.create(
            user=self.context['request'].user,
            file=validated_data['file']
        )

class FileVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVersion
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
        return user