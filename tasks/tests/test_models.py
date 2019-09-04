from django.test import TestCase
from django.db import transaction
from parameterized import parameterized
from django.core.exceptions import ValidationError
from ..models import Task
from ..models import Priority
from django.contrib.auth.models import User


ALLOWED_TASKS = [
    ("Tarea de Prueba", "2019-01-01", "2019-01-01", "2019-01-02 11:00", "2019-01-02 12:00", False, '1234'),
    ("Tarea de Prueba", "2019-01-01", "2019-01-01", None, None, True, '1234')
]

NOT_ALLOWED_TASKS = [
    ("", "2019-01-01", "2019-01-01", "2019-01-02 11:00", "2019-01-02 12:00", False, '1234', AttributeError),
    ("Tarea de Prueba", "2019-01-01 11:00", "2019-01-01 11:00", "2019-01-01 11:00", "2019-01-02 12:00", False, '1234', 
        ValidationError),
    ("Tarea de Prueba", "", "2019-01-01", "2019-01-02 11:00", "2019-01-02 12:00", False, '1234', AttributeError),
    ("Tarea de Prueba", "2019-01-01", "2019-01-01", "2019-01-02 11:00", "2019-01-02 12:00", False, '', ValidationError),
    ("Tarea de Prueba", "2019-01-01", "2019-01-01", "2019-01-02 11:00", "2019-01-01 11:00", False, '1234', 
        AttributeError),
]


# Test Priorities
class PriorityModelTests(TestCase):

    @parameterized.expand([
        ("Low",),
        ("Medium",),
        ("Urgent",)
    ])
    def test_str_priorities(self, name):
        priority = Priority.objects.create(name_priority=name)
        self.assertEquals(str(priority), "Priority: " + name)


# Test Tasks
class TaskModelTests(TestCase):

    def setUp(self):
        self.author = User.objects.create_user('foo', password='bar')
        self.priority = Priority.objects.create(name_priority='Low')

    # Test Creation
    @parameterized.expand(ALLOWED_TASKS)
    def test_allowed_tasks(self, name, creation_date, change_date, start_dt, end_dt, done, event):
        task = Task.objects.create(name_task=name, created_date=creation_date, changed_date=change_date, 
            start_date_time=start_dt, done=done, priority=self.priority, event_id=event, author=self.author)
        self.assertIsNone(task.full_clean())

    @parameterized.expand(NOT_ALLOWED_TASKS)
    def test_not_allowed_tasks(self, name, creation_date, change_date, start_dt, end_dt, done, event, exception):
        with transaction.atomic() and self.assertRaises(exception):
            Task.objects.create(name_task=name, created_date=creation_date, changed_date=change_date, 
                start_date_time=start_dt, end_date_time=end_dt, done=done, priority=self.priority, event_id=event, author=self.author)

