# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from Posts.models import Post
from . import serializers

# Create your views here.

class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer