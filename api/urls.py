from django.conf.urls import url, include
from . import views


urlpatterns = [
	url(r'^$', views.ListPost.as_view()),
	# url(r'^user/$', views.UserListView.as_view()),
	url(r'^(?P<pk>[0-9]+)/$', views.DetailPost.as_view()),
	
	url(r'^rest-auth/$', include('rest_auth.urls')),
    url(r'^rest-auth/registration/$', include('rest_auth.registration.urls')),
]