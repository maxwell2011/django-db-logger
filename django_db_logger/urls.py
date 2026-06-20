from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.main),
    path("main/flush/debug/", views.flush_debug_main, name="server_logs_flush_debug_main"),
    path("main/flush/info/", views.flush_info_main, name="server_logs_flush_info_main"),
    path("main/download/", views.download_logfile_main, name="server_logs_download_logfile_main"),
]
