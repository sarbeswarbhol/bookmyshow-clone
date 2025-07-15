import urllib.parse
import requests
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'phone', 'location', 'date_of_birth',
            'gender', 'profile_picture', 'password', 'password2', 'role'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.pop('password2')
        password = validated_data.pop('password')
        profile_picture = validated_data.pop('profile_picture', None)
        username = validated_data.get('username')

        user = User(**validated_data)
        user.set_password(password)

        if profile_picture:
            user.profile_picture = profile_picture
        else:
            # Fetch default avatar from API
            encoded_name = urllib.parse.quote(username)
            avatar_url = f"https://avatar.arctixapis.workers.dev/?name={encoded_name}"
            try:
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    user.profile_picture.save(
                        f"{username.replace(' ', '_')}_avatar.svg",
                        ContentFile(response.content)
                    )
            except Exception as e:
                print(f"⚠️ Failed to fetch avatar: {e}")

        if user.role == "admin":
            user.is_staff = True
            user.is_superuser = True

        user.save()

        refresh = RefreshToken.for_user(user)
        # print(user.profile_picture.url if user.profile_picture else "No profile picture")
        # print(request.build_absolute_uri(user.profile_picture.url) if user.profile_picture and request else None)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "phone": user.phone,
                "location": user.location,
                "gender": user.gender,
                "date_of_birth": user.date_of_birth,
                "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture and request else None,
            }
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = serializers.JSONField(read_only=True)

    def validate(self, data):
        request = self.context.get("request")
        user = authenticate(username=data['username'], password=data['password'])

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "phone": user.phone,
                "location": user.location,
                "date_of_birth": user.date_of_birth,
                "gender": user.gender,
                "profile_picture": request.build_absolute_uri(user.profile_picture.url) if user.profile_picture and request else None,
            }
        }


class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'location',
            'date_of_birth', 'gender', 'profile_picture', 'role'
        ]
        read_only_fields = ['id', 'email', 'username', 'role']

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and request:
            return request.build_absolute_uri(obj.profile_picture.url)
        return None
