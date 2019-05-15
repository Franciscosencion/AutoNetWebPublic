from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('sites', views.SitesListView.as_view(), name='viewsites'),
    path('sites/<int:pk>', views.SitesDetailView.as_view(), name='sitesdetail'),
    path('updatesite/<int:pk>', views.SiteUpdateView.as_view(), name='updatesite'),
    path('deletesite/<int:pk>', views.SiteDeleteView.as_view(), name='deletesite'),
    path('devices', views.DeviceListView.as_view(), name='viewdevices'),
    path('create/', views.SiteCreateView.as_view(), name='createsite'),
    path('create_device/', views.DeviceCreateView.as_view(), name='createdevice'),
    path('devices/<int:pk>', views.DeviceDetailView.as_view(), name='devicedetail'),
    path('devices/<int:pk>/config/', views.DeviceConfigDetailView.as_view(), name='deviceconfig'),
    path('updatedevice/<int:pk>', views.DeviceUpdateView.as_view(), name='updatedevice'),
    path('deletedevice/<int:pk>', views.DeviceDeleteView.as_view(), name='deletedevice'),

]
