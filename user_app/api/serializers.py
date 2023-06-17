from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'},write_only= True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        estra_kwargs = {
            'password':{'write_only':True}
        }

    # overwriting the save method to perform checks
    def save(self):
        # get the validated data as this is the only way to get the data in a serializer
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error':'Your passwords do not match'})
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error':'Email already exists. Try another email'})
            
        account = User(email=email, username=username)
        # set password
        account.set_password(password)

        account.save()
        return account
  