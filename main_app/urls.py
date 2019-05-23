from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import path
from . import views

app_name = 'main_app'
urlpatterns = [
    path('', login_required(views.HomeTemplateView.as_view()), name='home'),
    path('sites', login_required(views.SitesListView.as_view()), name='viewsites'),
    path('sites/<int:pk>', login_required(views.SitesDetailView.as_view()), name='sitesdetail'),
    path('updatesite/<int:pk>', login_required(views.SiteUpdateView.as_view()), name='updatesite'),
    path('deletesite/<int:pk>', login_required(views.SiteDeleteView.as_view()), name='deletesite'),
    path('devices', login_required(views.DeviceListView.as_view()), name='viewdevices'),
    path('create/', login_required(views.SiteCreateView.as_view()), name='createsite'),
    path('create_device/', login_required(views.DeviceCreateView.as_view()), name='createdevice'),
    path('devices/<int:pk>', login_required(views.DeviceDetailView.as_view()), name='devicedetail'),
    path('devices/config/<int:pk>', login_required(views.DeviceConfigDetailView.as_view()), name='deviceconfig'),
    path('devices/script/<int:pk>', login_required(views.DeviceScriptDetailView.as_view()), name='devicescript'),
    path('updatedevice/<int:pk>', login_required(views.DeviceUpdateView.as_view()), name='updatedevice'),
    path('deletedevice/<int:pk>', login_required(views.DeviceDeleteView.as_view()), name='deletedevice'),
    path('deleteconfig/config/<int:pk>', login_required(views.DeviceConfigDeleteView.as_view()), name='deleteconfig'),
    path('devices/<deviceip>&<deviceid>', views.sync_configuration, name='configsync'),
    path('search/', views.device_search_function, name='search'),

]
