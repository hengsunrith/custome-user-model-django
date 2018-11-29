# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Posts.models import Post, Book
from .serializers import (PostSerializer, UpdateSerializer, BookSerializer)
from rest_framework import status
from django.http import Http404

class ListPost(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get(self, request, format=None):
        limit =10
        offset = limit * (int(request.data.get('page'))-1)
        print offset
        queryset = Post.objects.all()[offset:offset+limit]
        serializer = PostSerializer(queryset, many=True)
        return Response({"data": serializer.data})

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailPost(APIView):
    permission_classes = (IsAuthenticated,)
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

        return Response({"data": serializer.data})


    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = UpdateSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Test Book API
class BookViewAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get(self, request, format=None):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)

        return Response({"data": serializer.data})

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        # queryset = get_object_or_404(Post, pk=pk)
        book = self.get_object(pk)
        serializer = BookSerializer(book, many=False)

        return Response({"data": serializer.data})


    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)