from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from unittest.mock import patch

dictionary = {
    'events': []
}
# URL
# data
# response
# asserts
class EventListTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        UserSocialAuth.objects.create(
            user=self.user,
            provider='eventbrite',
            uid='34563456',
            extra_data={
                'auth_time': 1567447106,
                'access_token': 'KLHJLJHLKJH',
                'token_type': 'bearer',
            }
        )
    # PLANTEAR LOS ESCENARIOS PARA EVENTOS
    # LISTA VACIA
    # LISTA CON EVENTOS
    @patch('tasks.views.Eventbrite.get', return_value=dictionary)
    def test_get_events(self, mocked_get):
        self.client.force_login(self.user)
        self.client.get('/events/')
        mocked_get.assert_called_with('/users/me/events/')
        self.client.logout()


# LOGIN
# class LoginTest(TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='testuser', password='12345')
    
#     def test_login(self):
#         response = self.client.post('/accounts/login',
#             {'username': 'testuser', 'password': '12345'})
#         self.assertEquals(response.status_code, 302)
# LOGOUT
# TaskList
# TaskCreate (Revisar los codigos de response)
# TaskUpdate (Revisar los codigos de response)
# TaskDelete (Revisar los codigos de response)
