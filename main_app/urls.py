from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('sites', views.SitesListView.as_view(), name='viewsites'),
    path('sites/<int:pk>', views.SitesDetailView.as_view(), name='sitesdetail'),
    path('devices', views.SitesDetailView.as_view(), name='viewdevices'),

]
