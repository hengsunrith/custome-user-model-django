# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from Posts.models import Post
from accounts.models import User
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from django.http import Http404


# Create your views here.
class ListPost(APIView):
	permission_classes = (IsAuthenticated, )
	serializer_class = PostSerializer

	def get(self, request, format=None):
		queryset = Post.objects.all()
		serializer = PostSerializer(queryset, many=True)

		return Response({"data":serializer.data})

	def post(self, request, format=None):

		serializer = PostSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailPost(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer

    def get_object(self, pk):
	try:
	 return Post.objects.get(pk=pk)
	except Post.DoesNotExist:
	 raise Http404
			

    def get(self, request, pk, format=None):
	# queryset = get_object_or_404(Post, pk=pk)
	 post = self.get_object(pk)
	 serializer = PostSerializer(post, many=False)
	return Response({"data":serializer.data})


	def put(self, request, pk, format=None):
     post = self.get_object(pk)
     serializer = PostSerializer(post, data=request.data)
     if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DetailPost(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class UserListView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer