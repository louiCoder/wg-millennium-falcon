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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit,
    Apikeyuserprofile)


class MainuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class UserSerializer(serializers.ModelSerializer):

    user = MainuserSerializer(required=True, many=False)

    class Meta:
        model = Apikeyuserprofile
        fields = ('user', 'key')

    def create(self, validated_data):

        try:
            validated_data['key']
            validated_data['user']
        except KeyError as missing_key:
            message = "Please supply a " + str(missing_key) + \
                " and a value"
            raise serializers.ValidationError(message)

        key = validated_data['key']

        if key == "":
            message = 'You must provide a value for the api key'
            raise serializers.ValidationError(message)

        if Token.objects.filter(key=key).exists() is False:
            raise serializers.ValidationError('Invalid api key supplied')

        validatated_user = validated_data.pop('user')

        username, email, first_name, last_name, password = 0, 0, 0, 0, 0

        for item in validatated_user.items():
            if item[0] == 'username':
                username = item[1]
            if item[0] == 'email':
                email = item[1]
            if item[0] == 'first_name':
                first_name = item[1]
            if item[0] == 'last_name':
                last_name = item[1]
            if item[0] == 'password':
                password = item[1]

        new_user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        api = Apikeyuserprofile.objects.create(key=key, user=new_user)

        return api


class UserprofileSerializer(serializers.ModelSerializer):
    '''
    Workout session serializer
    '''
    class Meta:
        model = UserProfile


class UsernameSerializer(serializers.Serializer):
    '''
    Serializer to extract the username
    '''
    username = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    '''
    Language serializer
    '''
    class Meta:
        model = Language


class DaysOfWeekSerializer(serializers.ModelSerializer):
    '''
    DaysOfWeek serializer
    '''
    class Meta:
        model = DaysOfWeek


class LicenseSerializer(serializers.ModelSerializer):
    '''
    License serializer
    '''
    class Meta:
        model = License


class RepetitionUnitSerializer(serializers.ModelSerializer):
    '''
    Repetition unit serializer
    '''
    class Meta:
        model = RepetitionUnit


class WeightUnitSerializer(serializers.ModelSerializer):
    '''
    Weight unit serializer
    '''
    class Meta:
        model = WeightUnit
