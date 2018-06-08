# -*- coding: utf-8 *-*

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

import datetime

from django.utils.timezone import now
from django.core.management.base import BaseCommand
from wger.core.models import (UserProfile, Apikeyuserprofile)


class Command(BaseCommand):
    '''
    Helper admin command to list all users created with a particular api key
    '''

    def add_arguments(self, parser):
        # Optional arguments
        parser.add_argument('api_key', type=str, nargs='*')

    def handle(self, *args, **options):

        if len(options['api_key']) > 0:
            keys = Apikeyuserprofile.objects.all().filter(key=options['api_key'][1])
        else:
            keys = Apikeyuserprofile.objects.all()

        if len(keys) == 0:
            self.stdout.write("Sorry no users found")

        for key in keys:
            self.stdout.write("Username:" + key.user.username
                              + " ---------------> Token: " + key.key
                              )
