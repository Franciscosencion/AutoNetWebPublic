from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views
from .api import views as api_views

app_name = 'main_app'
urlpatterns = [
    path('api/sites/', api_views.SitesListCreateAPIView.as_view(), name='sites_rest_api'),
    path('api/sites/<uuid>', view=api_views.SitesRetrieveUpdateDestroyAPIView.as_view(),
            name='sites_rest_api'),
    path('api/devices/', api_views.DevicesListCreateAPIView.as_view(), name='devices_rest_api'),
    path('api/devices/<uuid>', api_views.DevicesRetrieveUpdateDestroyAPIView.as_view(),
            name='devices_rest_api'),
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('sites', views.SitesListView.as_view(), name='viewsites'),
    path('sites/<int:pk>', views.SitesDetailView.as_view(), name='sitesdetail'),
    path('updatesite/<int:pk>', views.SiteUpdateView.as_view(), name='updatesite'),
    path('deletesite/<int:pk>', views.SiteDeleteView.as_view(), name='deletesite'),
    path('devices', views.DeviceListView.as_view(), name='viewdevices'),
    path('create/', views.SiteCreateView.as_view(), name='createsite'),
    path('create_device/', views.DeviceCreateView.as_view(), name='createdevice'),
    path('devices/<int:pk>', views.DeviceDetailView.as_view(), name='devicedetail'),
    path('devices/config/<int:pk>', views.DeviceConfigDetailView.as_view(), name='deviceconfig'),
    path('devices/script/<int:pk>', views.DeviceScriptDetailView.as_view(), name='devicescript'),
    path('updatedevice/<int:pk>', views.DeviceUpdateView.as_view(), name='updatedevice'),
    path('deletedevice/<int:pk>', views.DeviceDeleteView.as_view(), name='deletedevice'),
    path('deleteconfig/config/<int:pk>', views.DeviceConfigDeleteView.as_view(), name='deleteconfig'),
    path('devices/syncconfig/<deviceip>&<deviceid>', views.sync_configuration, name='configsync'),
    path('devices/platformsync/<deviceip>&<deviceid>', views.get_platform_detail, name='platformsync'),
    path('search/', views.device_search_function, name='search'),
    path('devices/syncvlans/<deviceip>&<deviceid>', views.sync_device_vlans, name='vlanssync'),
    path('devices/tasks/vlanchange/<deviceip>&<deviceid>', views.port_vlan_assignment, name='vlanchange'),

]
