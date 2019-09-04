from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EventList.as_view(), name='event-list'),
    url(r'(?P<event_id>[0-9]+)/tasks/update/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='task-update'),
    url(r'(?P<event_id>[0-9]+)/tasks/delete/(?P<pk>[0-9]+)/$', views.TaskDelete.as_view(), name='task-delete'),
    url(r'(?P<event_id>[0-9]+)/tasks/create/$', views.TaskCreate.as_view(), name='task-create'),
    url(r'(?P<event_id>[0-9]+)/tasks/$', views.TaskList.as_view(), name='task-list'),
]
