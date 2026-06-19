from import_export.resources import ModelResource
from .models import StatusLog, TracebackLog

class StatusLogResource(ModelResource):

    class Meta:
        model = StatusLog


class TracebackLogResource(ModelResource):

    class Meta:
        model = TracebackLog
