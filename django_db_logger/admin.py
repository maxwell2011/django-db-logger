from __future__ import unicode_literals
import logging
from typing import Union
from datetime import datetime, timedelta
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from import_export.admin import ExportActionModelAdmin

from django_db_logger.config import DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
from .models import StatusLog, TracebackLog
from .resources import StatusLogResource, TracebackLogResource

base_actions = [
    "flush_older_than_1_day_logs",
    "flush_older_than_1_week_logs"
]

def fieldsets_factory(k: str = "t"):
    if k == "t":
        toplevel = "trace"
        msglevel = "msg"
    elif k == "s":
        toplevel = "msg"
        msglevel = "trace"
    else:
        raise Exception("What? '%s'" % k)
    return [
        (None, {"fields": [("logger", "level", "asctime"), toplevel]}),
        ("File", {
            "classes": ["collapse"],
            "fields": ["module", "lineno"]
        }),
        ("Process", {
            "classes": ["collapse"],
            "fields": [("pid", "tid"), msglevel]
        }),
    ]

class BaseLogAdmin(ExportActionModelAdmin):
    list_per_page = DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE
    list_display = ("create_datetime_format", "logger", "level", "colored_msg", "has_traceback")
    list_display_links = ("colored_msg",)
    list_filter = ("level","module", "logger")
    readonly_fields = ["asctime", "msg", "trace", "module", "lineno", "pid", "tid", "logger", "level"]

    def has_add_permission(self, request):
        return False

    def has_traceback(self, instance):
        if instance.trace is not None:
            return True
        return False
        

    has_traceback.boolean = True

    def flush_older_than_1_day_logs(self, request, queryset):
        dt = datetime.now() - timedelta(days=1)
        self.model.objects.filter(asctime__lte=dt).delete()

    flush_older_than_1_day_logs.short_description = "Flush Yesterday" 

    def flush_older_than_1_week_logs(self, request, queryset):
        dt = datetime.now() - timedelta(days=7)
        self.model.objects.filter(asctime__lte=dt).delete()

    flush_older_than_1_week_logs.short_description = "Flush Last Week" 


    def flush_error_logs(self, request, queryset):
        StatusLog.objects.filter(level=logging.ERROR).delete()

    flush_error_logs.short_description = "Flush Error"

    def flush_error_and_below_logs(self, request, queryset):
        StatusLog.objects.filter(level__lte=logging.ERROR).delete()

    flush_error_and_below_logs.short_description = "Flush LTE Error"

    def flush_critical_logs(self, request, queryset):
        StatusLog.objects.filter(level=logging.CRITICAL).delete()

    flush_critical_logs.short_description = "Flush Critical"

    def flush_critical_and_below_logs(self, request, queryset):
        StatusLog.objects.filter(level__lte=logging.CRITICAL).delete()

    flush_critical_and_below_logs.short_description = "Flush LTE Critical"


    def colored_msg(self, instance):
        if instance.level in [logging.NOTSET, logging.INFO]:
            color = "green"
        elif instance.level in [logging.WARNING, logging.DEBUG]:
            color = "orange"
        else:
            color = "red"
        return format_html('<span style="color: {color};">{msg}</span>', color=color, msg=instance.msg)

    colored_msg.short_description = "Message"

    def traceback(self, instance):
        return format_html("<pre><code>{content}</code></pre>", content=instance.trace if instance.trace else "")

    def create_datetime_format(self, instance):
        return timezone.localtime(instance.asctime).strftime("%Y-%m-%d %X")

    create_datetime_format.short_description = "Timestamp"

    class Meta:
        abstract = True

@admin.register(TracebackLog)
class TracebackLogAdmin(BaseLogAdmin):
    actions = base_actions
    fieldsets = fieldsets_factory("t")
    resource_classes = [TracebackLogResource]
    
@admin.register(StatusLog)
class StatusLogAdmin(BaseLogAdmin):
    fieldsets = fieldsets_factory("s")
    actions = base_actions
    actions.extend([
        "flush_debug_logs",
        "flush_info_logs",
        "flush_info_and_below_logs",
        "flush_warning_logs",
        "flush_warning_and_below_logs",
        
    ])
    resource_classes = [StatusLogResource]

    def num_ocurrences(self, instance):
        return StatusLog.objects.filter(level=instance.level)

    def flush_debug_logs(self, request, queryset):
        StatusLog.objects.filter(level=logging.DEBUG).delete()
    
    flush_debug_logs.short_description = "Flush Debug"

    def flush_info_logs(self, request, queryset):
        StatusLog.objects.filter(level=logging.INFO).delete()

    flush_info_logs.short_description = "Flush Info"

    def flush_info_and_below_logs(self, request, queryset):
        StatusLog.objects.filter(level__lte=logging.INFO).delete()

    flush_info_and_below_logs.short_description = "Flush LTE Info"

    def flush_warning_logs(self, request, queryset):
        StatusLog.objects.filter(level=logging.WARNING).delete()

    flush_warning_logs.short_description = "Flush Warning"

    def flush_warning_and_below_logs(self, request, queryset):
        StatusLog.objects.filter(level__lte=logging.WARNING).delete()

    flush_warning_and_below_logs.short_description = "Flush LTE Warning"
