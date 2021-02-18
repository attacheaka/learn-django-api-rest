import jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from .renderers import UserRenderer

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, EmailVerifySerializer, LogoutSerializer


# Register Api
class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        # enregistre dans la bd
        serializer.save()
        user_data = serializer.data
        # cherche l'utilisateur enregistre
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        # envoi d'email
        email_body = 'Salut ' + user.username + \
                     '\n Utilise le lien ci-dessous pour finaliser votre inscription \n' + absurl
        data = {'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Activation de votre compte par mail'}
        Util.send_email(data)
        return Response({
            "notification": "Email envoyé avec succès",
            "status": status.HTTP_201_CREATED
        })

# VeriyEmail Api
class VerifyEmailAPI(views.APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = EmailVerifySerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            # decode le token ( jwt : Json Web Token )
            payload = jwt.decode(jwt=token, algorithms=['HS256'], key=settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            print(payload)
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status= status.HTTP_400_BAD_REQUEST)

# Login Api
class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

# Get User API
class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
