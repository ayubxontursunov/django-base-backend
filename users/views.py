from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .serializers import (
    UserSerializer, RegisterSerializer, CheckEmailSerializer, LoginSerializer,
    VerifyOTPSerializer, ResendOTPSerializer, PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer, PasswordChangeSerializer
)
from .models import OTPCode
from .utils import send_otp_email

User = get_user_model()


class CheckEmailView(generics.GenericAPIView):
    """Check if email exists in database."""
    permission_classes = [AllowAny]
    serializer_class = CheckEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user_exists = User.objects.filter(email=email).exists()
        
        return Response({
            'exists': user_exists,
            'email': email
        })


class RegisterView(generics.CreateAPIView):
    """Register a new user."""
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User created successfully. Please verify your email.',
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)


class VerifyOTPView(generics.GenericAPIView):
    """Verify OTP code."""
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']
        purpose = serializer.validated_data['purpose']
        
        # If registration, mark email as verified and log user in
        if purpose == 'registration':
            # Mark OTP as used only for registration
            otp.is_used = True
            otp.save()
            
            user = User.objects.get(email=email)
            user.email_verified = True
            user.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_serializer.data,
                'message': 'Email verified successfully.'
            })
        
        # If password reset, just verify without marking as used
        # The OTP will be marked as used in password-reset-confirm
        return Response({
            'message': 'OTP verified successfully.',
            'verified': True,
            'code': otp.code  # Return code to use in next step
        })


class ResendOTPView(generics.GenericAPIView):
    """Resend OTP code."""
    permission_classes = [AllowAny]
    serializer_class = ResendOTPSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        purpose = serializer.validated_data['purpose']
        
        # Create new OTP
        otp = OTPCode.create_otp(email, purpose)
        send_otp_email(email, otp.code, purpose)
        
        return Response({
            'message': 'OTP code sent successfully.'
        })


class LoginView(generics.GenericAPIView):
    """Login user with email and password."""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Authenticate with username
        user = authenticate(username=user.username, password=password)

        if user is None:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_serializer.data
        })


class PasswordResetRequestView(generics.GenericAPIView):
    """Request password reset by email."""
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        # Create OTP for password reset
        otp = OTPCode.create_otp(email, 'password_reset')
        send_otp_email(email, otp.code, 'password_reset')
        
        return Response({
            'message': 'Password reset code sent to your email.',
            'email': email
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    """Confirm password reset with OTP and set new password."""
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        otp = serializer.validated_data['otp']
        
        # Mark OTP as used
        otp.is_used = True
        otp.save()
        
        # Update user password
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        
        return Response({
            'message': 'Password reset successfully. You can now login.'
        })


class ProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    """Change user password."""
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': ['Wrong password.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully.',
        })
