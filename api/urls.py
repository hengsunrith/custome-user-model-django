from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^page/(?P<page>\d+)/', views.ListPost.as_view()), # url pagination to list objects of posts
	url(r'^create-post/', views.CreatePostAPI.as_view()),
	url(r'^(?P<pk>[0-9]+)/', views.DetailPost.as_view()),

	#all-auth url
	url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),

	# Test Book API url
	url(r'^book/', views.BookViewAPI.as_view()),
	url(r'^book/(?P<pk>[0-9]+)/', views.BookDetail.as_view())
]