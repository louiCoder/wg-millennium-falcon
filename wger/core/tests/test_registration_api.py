# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

from wger.core.tests.base_testcase import WorkoutManagerTestCase
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationApiTest(APITestCase, WorkoutManagerTestCase):

    def test_get_registration(self):
        client = APIClient()
        response = client.get('/api/v2/register/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        '''
        User registration over API
        '''

        self.user_login('test')
        user = User.objects.get(username='test')
        key = Token.objects.get(user=user)

        client = APIClient()
        data = {
            "user": {
                "username": "omrj",
                "password": "omr",
                "first_name": "",
                "last_name": "",
                "email": ""
            },
            "key": key.key
        }
        response = client.post('/api/v2/register/', data=data)
        # Test for user created
        self.assertEqual(response.status_code, 201)

    def test_register_empty_key(self):
        '''
        Test user registration over API when api empty
        '''

        self.user_login('test')

        client = APIClient()
        data = {
            "user": {
                "username": "omrj",
                "password": "omr",
                "first_name": "",
                "last_name": "",
                "email": ""
            },
            "key": ""
        }
        response = client.post('/api/v2/register/', data=data)
        # Test for bad request returned
        self.assertEqual(response.status_code, 400)

    def test_register_no_key(self):
        '''
            Test user registration over API when no key field available
        '''

        self.user_login('test')

        client = APIClient()
        data = {
            "user": {
                "username": "omrj",
                "password": "omr",
                "first_name": "",
                "last_name": "",
                "email": ""
            }
        }
        response = client.post('/api/v2/register/', data=data)
        # Test for bad request returned
        self.assertEqual(response.status_code, 400)
