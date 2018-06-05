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
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from wger.core.tests.base_testcase import WorkoutManagerTestCase
from wger.utils.helpers import make_token


class WorkoutJsonExportTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting a workout as a Json
    '''

    def test_export_json_token(self):
        '''
        Function to test exporting a workout as a json using tokens
        '''

        user = User.objects.get(username='test')
        uid, token = make_token(user)
        response = self.client.get(reverse('manager:workout:json-data', kwargs={'id': 3,
                                                                                'uidb64': uid,
                                                                                'token': token}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename=Workout-3.json')

    def test_export_json_token_wrong(self):
        '''
        Function to test exporting a workout as a json using a wrong token
        '''

        uid = 'AB'
        token = 'abc-11223344556677889900'
        response = self.client.get(reverse('manager:workout:json-data', kwargs={'id': 3,
                                                                                'uidb64': uid,
                                                                                'token': token}))

        self.assertEqual(response.status_code, 403)

    def test_export_json(self, fail=False):
        '''
        Function to test exporting a workout as a json
        '''

        user = User.objects.get(username='test')
        uid, token = make_token(user)

        response = self.client.get(reverse('manager:workout:json-data', kwargs={'id': 3,
                                                                                'uidb64': uid,
                                                                                'token': token}))

        if fail:
            self.assertIn(response.status_code, (403, 404, 302))
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/json')
            self.assertEqual(response['Content-Disposition'],
                             'attachment; filename=Workout-3.json')
