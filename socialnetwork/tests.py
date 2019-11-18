from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class SocialNetworkTest(TestCase):

    # fixtures = ['db_test.json']

    def setUp(self):
        self.client = Client()
        self.token = self.login()


    def login(self):
        data = {"username": 'Ervin2',"password": 'Ervin2'}
        url = reverse('login')
        response = self.client.post(url, data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print("\n>LOGIN \nname: {}\nToken: {}\nstatus_code: {}".format(
        response.data['name'], response.data['token'], response.status_code))
        return 'Token ' + response.data['token']

    # Profile Endpoints

    def test_profile_list(self):
        url = reverse('profiles-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        print("\n> PROFILE_LIST \nstatus_code: {}".format(
        response.status_code))

    def test_profile_detail(self):
        url = reverse('profile-detail', kwargs={'pk': 2})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)
        print("\n> TEST_PROFILE_DETAIL \nname: {}\nstatus_code: {}".format(
        response.data['name'], response.status_code))
