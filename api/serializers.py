from rest_framework import serializers
from Posts.models import Post, Book


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('__all__')

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.auto_delete = validated_data.get('auto_delete', instance.auto_delete)
        instance.author = validated_data.get('author', instance.author)
        instance.save()

        return instance

# Test Book Serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('__all__')

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance