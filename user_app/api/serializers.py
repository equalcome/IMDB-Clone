from django.contrib.auth.models import User 
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'} ,write_only=True) 
    class Meta:
        model = User
        fields = ['username', 'email', 'password' ,'password2']
        extra_kwargs = {
            'password' : {'write_only': True}
        }
    
    def save(self):      
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 must be the same!!!'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!!!'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(password)
        account.save()  #存到DB
        
        return account
        


        
# User.objects.filter(email='example@example.com')
# 表示從 User 表中篩選出 email 字段等於 'example@example.com' 的所有記錄。
            