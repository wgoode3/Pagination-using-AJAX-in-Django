from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.leads),
	url(r'^new$', views.new),
	url(r'^create$', views.create),
	url(r'^search/(?P<id>\d+)$', views.search),
]