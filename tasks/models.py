from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


# PRIORITY
class Priority(models.Model):
    name_priority = models.CharField(max_length=200)

    def __str__(self):
        return "Priority: " + self.name_priority


# TASK
class Task(models.Model):
    name_task = models.CharField(max_length=200, )
    created_date = models.DateField('Creation Date', auto_now=True)
    changed_date = models.DateField('Date of Change', auto_now=True)
    start_date_time = models.DateTimeField('Start Date Time', null=True, blank=True)
    end_date_time = models.DateTimeField('End Date Time', null=True, blank=True)
    done = models.BooleanField()
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name_task

    def clean(self):
        if self.name_task == "":
            raise AttributeError("Database should not contain an empty name task!")
        elif self.created_date == "":
            raise AttributeError("Database should not contain an empty create date!")
        elif self.changed_date == "":
            raise AttributeError("Database should not contain an empty changed date!")
        elif self.start_date_time is not None and self.end_date_time is not None and self.start_date_time > self.end_date_time:
            raise AttributeError("Start date time should be greater than end date time")

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Task, self).save(*args, **kwargs)