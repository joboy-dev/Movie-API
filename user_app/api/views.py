from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# from user_app import models

@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        # this is where we will store all our data including the token and this will be returned as a response instead of serializer.data
        data = {} 

        if serializer.is_valid():
            # store the data gotten from the return in the save function in the serializer in a variable so the value can be easily accessed
            account = serializer.save()

            # create custom json response data
            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email
            
            # token auth - creating token
            token = Token.objects.get(user=account).key  # returns the user token key
            data['token'] = token

            # jwt auth - creating token
            # refresh_token = RefreshToken.for_user(account)
            # data['token'] = {
            #     'refresh':str(refresh_token),
            #     'acess':str(refresh_token.access_token)
            # }

        else:
            data = serializer.errors
              
        return Response(data)
 

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        # access current user token
        current_user_token = request.user.auth_token
        # delete the token then the user will be logged out
        current_user_token.delete()
        return Response({'message':'Successfully logged out'})

