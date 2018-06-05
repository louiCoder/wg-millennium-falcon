# -*- coding: utf-8 -*-

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

import logging
import datetime
import json

from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from wger.manager.models import Workout
from wger.manager.helpers import render_workout_day
from wger.utils.helpers import check_token
from wger.utils.pdf import styleSheet
from wger.utils.pdf import render_footer

from reportlab.lib.pagesizes import A4, cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Table,
    Spacer
)

from reportlab.lib import colors

from wger import get_version

logger = logging.getLogger(__name__)


def workout_log(request, id, images=False, comments=False, uidb64=None, token=None):
    '''
    Generates a PDF with the contents of the given workout

    See also
    * http://www.blog.pythonlibrary.org/2010/09/21/reportlab
    * http://www.reportlab.com/apis/reportlab/dev/platypus.html
    '''
    comments = bool(int(comments))
    images = bool(int(images))

    # Load the workout
    if uidb64 is not None and token is not None:
        if check_token(uidb64, token):
            workout = get_object_or_404(Workout, pk=id)
        else:
            return HttpResponseForbidden()
    else:
        if request.user.is_anonymous():
            return HttpResponseForbidden()
        workout = get_object_or_404(Workout, pk=id, user=request.user)

    if len(workout.canonical_representation['day_list']) > 0:

        exercise_set = workout.canonical_representation['day_list'][0]['set_list']

        workout_details = {
            'description': workout.canonical_representation['day_list'][0]['obj'].description,
            'workout_days': workout.canonical_representation['day_list'][0]['days_of_week']['text']
        }

        set_list = []

        for set in exercise_set:
            set_dict = {}
            exercise_list = []
            holder = {}
            set_dict['set_id'] = set['obj'].id

            for item in set['exercise_list']:
                holder['name_of_exercise'] = item['obj'].name
                holder['setting_list'] = item['setting_list']
                holder['comments'] = item['comment_list']
                exercise_list.append(holder)

            set_dict['exercise_list'] = exercise_list

            set_list.append(set_dict)

        workout_details['set_list'] = set_list
    else:
        workout_details = []

    json_data = json.dumps(workout_details)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(json_data, content_type='application/json')

    # Create the HttpResponse object with the appropriate PDF headers.
    response['Content-Disposition'] = 'attachment; filename=Workout-{0}.json'.format(id)
    response['Content-Length'] = len(response.content)
    return response
