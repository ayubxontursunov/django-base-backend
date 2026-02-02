from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import OTPCode
from .utils import send_otp_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'phone_number', 'avatar', 'language', 'is_staff', 'is_active', 'email_verified', 'date_joined']
        read_only_fields = ['id', 'username', 'is_staff', 'is_active', 'email_verified', 'date_joined']


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number', 'password', 'password2']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        email = validated_data['email']
        
        # Generate username from email
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        validated_data['username'] = username
        validated_data['email_verified'] = False
        
        user = User.objects.create_user(**validated_data)
        
        # Create OTP for email verification
        otp = OTPCode.create_otp(email, 'registration')
        send_otp_email(email, otp.code, 'registration')
        
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    purpose = serializers.ChoiceField(choices=['registration', 'password_reset'])

    def validate(self, attrs):
        email = attrs['email']
        code = attrs['code']
        purpose = attrs['purpose']

        try:
            otp = OTPCode.objects.filter(
                email=email,
                code=code,
                purpose=purpose,
                is_used=False
            ).latest('created_at')
            
            if not otp.is_valid():
                raise serializers.ValidationError("OTP code has expired.")
            
            attrs['otp'] = otp
        except OTPCode.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP code.")
        
        return attrs


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.ChoiceField(choices=['registration', 'password_reset'])


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6, min_length=6)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Verify OTP
        email = attrs['email']
        code = attrs['code']
        
        try:
            otp = OTPCode.objects.filter(
                email=email,
                code=code,
                purpose='password_reset',
                is_used=False
            ).latest('created_at')
            
            if not otp.is_valid():
                raise serializers.ValidationError("OTP code has expired.")
            
            attrs['otp'] = otp
        except OTPCode.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP code.")
        
        return attrs
