from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import Task
from django.urls import (
    reverse_lazy
)
from eventbrite import Eventbrite

empty_response = {
    "events": []
}


class TaskLogin(LoginView):
    pass


class TaskLogout(LogoutView):
    pass


class EventList(TemplateView):

    template_name = 'events/list_events.html'

    def get_events(self):
        social = self.request.user.social_auth.filter(provider='eventbrite')[0]
        token = social.access_token
        eventbrite = Eventbrite(token)
        events = eventbrite.get('/users/me/events/')
        if not events['events']:
            return empty_response
        return events['events']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events_list'] = self.get_events()
        return context


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    fields = ['name_task', 'priority', 'done']

    def get_queryset(self):
        return Task.objects.filter(event_id=int(self.kwargs['event_id']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_id'] = self.kwargs['event_id']
        return context


class TaskCreate(CreateView):
    model = Task
    fields = ['name_task', 'priority', 'done', 'start_date_time', 'end_date_time']

    def get_success_url(self):
        return reverse_lazy('task-list', kwargs={'event_id': self.kwargs['event_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['event_id'] = self.kwargs['event_id']
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.event_id = self.kwargs['event_id']
        self.object = form.save()
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(UpdateView):
    model = Task
    fields = ['name_task', 'priority', 'done', 'start_date_time', 'end_date_time']

    def get_success_url(self):
        return reverse_lazy('task-list', kwargs={'event_id': self.kwargs['event_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class TaskDelete(DeleteView):
    model = Task

    def get_success_url(self):
        return reverse_lazy('task-list', kwargs={'event_id': self.kwargs['event_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context