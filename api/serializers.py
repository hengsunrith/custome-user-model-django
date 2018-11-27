from rest_framework import serializers
from Posts.models import Post
from accounts.models import User



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'username', )