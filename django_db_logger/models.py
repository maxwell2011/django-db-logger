import logging
from django.db.models import (
    Model, 
    Manager,
    QuerySet,
    Q,
    CharField, 
    DateTimeField, 
    PositiveIntegerField,
    PositiveSmallIntegerField,
    TextField
)
from django.utils.translation import gettext_lazy as _

LOG_LEVELS = (
    (logging.NOTSET, _('NotSet')),
    (logging.INFO, _('Info')),
    (logging.WARNING, _('Warning')),
    (logging.DEBUG, _('Debug')),
    (logging.ERROR, _('Error')),
    (logging.FATAL, _('Fatal')),
)

class StatusLogQuerySet(QuerySet):
    pass

class StatusLogManager(Manager):
    def get_queryset(self):
        return TracebackLogQuerySet(self.model, using=self._db)

    def get_errors(self):
        return self.get_queryset().filter(level__gte=logging.ERROR)

class StatusLog(Model):
    asctime = DateTimeField(
        verbose_name=_("Timestamp"),
        help_text=_("Timestamp of the log entry"),
        editable=False
    )
    module = CharField(
        verbose_name=_("Module"),
        help_text=_("Name portion of the filename"),
        max_length=100,
        editable=False
    )
    lineno = PositiveIntegerField(
        verbose_name=_("Line Number"),
        help_text=_("Source line number where the logging call was issued (if available, default: 0)"),
        blank=False, null=False, default = 0,
        editable=False
    )
    pid = PositiveIntegerField(
        verbose_name=_("Process ID"),
        help_text=_("Process id (if available, default: 0)"),
        blank=False, null=False, default = 0,
        editable=False
    )
    tid = PositiveIntegerField(
        verbose_name=_("Thread ID"),
        help_text=_("Thread id (if available, default: 0)"),
        blank=False, null=False, default = 0,
        editable=False
    )
    logger = CharField(
        verbose_name=_("Logger"),
        help_text=_("Name of the logger"),
        blank=False, null=False, max_length=100,
        editable=False
    )
    level = PositiveSmallIntegerField(
        verbose_name=_("Level"),
        help_text=_("Log level of the entry"),
        choices=LOG_LEVELS, default=logging.ERROR, db_index=True,
        editable=False)
    msg = TextField(
        verbose_name=_("Message"),
        help_text=_("Raw message"),
        max_length=4096,
        editable=False
    )
    trace = TextField(
        verbose_name=_("Traceback"),
        help_text=_("Raw traceback exception info (if available)"),
        blank=True, null=True, 
        max_length=4096,
        editable=False)

    objects = StatusLogManager()

    def __int__(self) -> int:
        return self.level

    def __str__(self):
        return self.msg

    @property
    def levelname(self) -> str:
        match self.level:
            case logging.NOTSET:    return _("Not Set")
            case logging.INFO:      return _("Info")
            case logging.WARNING:   return _("Warning")
            case logging.DEBUG:     return _("Debug")
            case logging.ERROR:     return _("Error")
            case logging.FATAL:     return _("Fatal")
            case _:                 
                logger.error("Unknown/Undefined loglevel: '%s'" % (str(self.level),))
                return _("Undefined")

    class Meta:
        ordering = ("-asctime",)
        verbose_name = _("Logging")
        verbose_name_plural = verbose_name = _("Logging")

class TracebackLogQuerySet(QuerySet):
    pass

class TracebackLogManager(Manager):

    def get_queryset(self):
        return TracebackLogQuerySet(self.model, using=self._db).filter(~Q(trace=None))

class TracebackLog(StatusLog):

    objects = TracebackLogManager()

    class Meta:
        proxy = True
        ordering = ("-asctime",)
        verbose_name = _("Traceback Log")
        verbose_name_plural = verbose_name = _("Traceback Logs")
