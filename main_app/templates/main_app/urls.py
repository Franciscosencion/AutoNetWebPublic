from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('sites', views.SitesListView.as_view(), name='viewsites'),
    path('sites/<int:pk>', views.SitesDetailView.as_view(), name='sitesdetail'),
    path('updatesite/<int:pk>', views.SiteUpdateView.as_view(), name='updatesite'),
    path('devices', views.DeviceListView.as_view(), name='viewdevices'),
    path('create/', views.SiteCreateView.as_view(), name='createsite'),
    path('create_device/', views.DeviceCreateView.as_view(), name='createdevice'),
    path('devices/<int:pk>', views.DeviceDetailView.as_view(), name='devicedetail'),

]
