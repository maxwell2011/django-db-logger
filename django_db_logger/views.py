import logging
import json
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, FileResponse
from django.template.response import TemplateResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django_htmx.middleware import HtmxDetails
from import_export.forms import ExportForm
from .utils import for_htmx
from .models import StatusLog, TracebackLog
from .resources import StatusLogResource, TracebackLogResource
# Create your views here.

logger = logging.getLogger('db')

class FlushDebugLogsForm(ModelForm):
    class Meta:
        model = StatusLog

@for_htmx(use_block_from_params=True)
def main(request) -> TemplateResponse:
    return TemplateResponse(
        request,
        "server_logs_modal_main.html",
        {
            "logs": StatusLog.objects.all().order_by("-asctime"),
        },
    )


@require_GET
def logs(request: HtmxHttpRequest) -> HttpResponse:
    _logs_errors = StatusLog.objects.get_errors()
    _logs = StatusLog.objects.all()
    return render(
        request, 
        "server_logs.html",
        {
            "server_logs": _logs,
            "server_errors": _logs_errors
        }
    )

@require_POST
def logs_download_start(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request, 
        "server_logs_download.html"
    )

@require_GET
def logs_download_status(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request, 
        "server_logs_download.html"
    )

@require_GET
def logs_download_file(request: HtmxHttpRequest) -> FileResponse:
    #response = FileResponse(
    #    open(file_path, "rb"),
    #    content_type="application/octet-stream",
    #    filename="server-logs.txt"
    #)
    return {} #response

@require_http_methods(["DELETE"])
def logs_download_reset(request: HtmxHttpRequest) -> HttpResponse:
    return render(
        request, "server_logs.html"
    )


@require_GET
def logs_download_file_error_logs(request: HtmxHttpRequest) -> FileResponse:
    #response = FileResponse(
    #    open(file_path, "rb"),
    #    content_type="application/octet-stream",
    #    filename="server-logs.txt"
    #)
    return {} #response
    #/logs/download/error_logs
