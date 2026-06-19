import logging
from django.utils import timezone
from datetime import timezone as dt_tz
from datetime import datetime
from django_db_logger.config import DJANGO_DB_LOGGER_ENABLE_FORMATTER, MSG_STYLE_SIMPLE


db_default_formatter = logging.Formatter()


class DatabaseLogHandler(logging.Handler):
    def make_asctime_timezone_aware(self, record):
        if hasattr(record, "asctime"):
            return timezone.make_aware(datetime.fromisoformat(record.asctime), dt_tz.utc)
            
    def emit(self, record):
        from .models import StatusLog
        
        trace = None

        if record.exc_info:
            trace = db_default_formatter.formatException(record.exc_info)

        if DJANGO_DB_LOGGER_ENABLE_FORMATTER:
            msg = self.format(record)
        else:
            msg = record.getMessage()

        kwargs = {
            "asctime": self.make_asctime_timezone_aware(record),
            "module": record.module,
            "lineno": record.lineno,
            "pid": record.process,
            "tid": record.thread,
            "logger": record.name,
            "level": record.levelno,
            "msg": msg,
            "trace": trace
        }

        StatusLog.objects.create(**kwargs)

    def format(self, record):
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = db_default_formatter

        if type(fmt) == logging.Formatter:
            record.message = record.getMessage()

            if fmt.usesTime():
                record.asctime = fmt.formatTime(record, fmt.datefmt)

            # ignore exception traceback and stack info

            return fmt.formatMessage(record)
        else:
            return fmt.format(record)
