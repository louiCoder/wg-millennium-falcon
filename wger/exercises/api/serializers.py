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

from rest_framework import serializers
from wger.exercises.models import (
    Muscle,
    Exercise,
    ExerciseImage,
    ExerciseCategory,
    Equipment,
    ExerciseComment
)


class ExerciseSerializer(serializers.ModelSerializer):
    '''
    Exercise serializer
    '''
    class Meta:
        model = Exercise


class EquipmentSerializer(serializers.ModelSerializer):
    '''
    Equipment serializer
    '''
    class Meta:
        model = Equipment


class ExerciseImageSerializer(serializers.ModelSerializer):
    '''
    ExerciseImage serializer
    '''
    class Meta:
        model = ExerciseImage


class ExerciseInfoSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Exercise info serialiser
    '''
    muscles = serializers.StringRelatedField(many=True)
    language = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField()
    equipment = serializers.StringRelatedField(many=True)
    muscles_secondary = serializers.StringRelatedField(many=True)
    license = serializers.StringRelatedField()
    exerciseimage_set = ExerciseImageSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ('id', 'license_author', 'license', 'category', 'equipment',
                  'description', 'name', 'name_original', 'muscles', 'muscles_secondary',
                  'creation_date', 'language', 'uuid', 'exerciseimage_set')


class ExerciseCategorySerializer(serializers.ModelSerializer):
    '''
    ExerciseCategory serializer
    '''
    class Meta:
        model = ExerciseCategory


class ExerciseCommentSerializer(serializers.ModelSerializer):
    '''
    ExerciseComment serializer
    '''
    class Meta:
        model = ExerciseComment


class MuscleSerializer(serializers.ModelSerializer):
    '''
    Muscle serializer
    '''
    class Meta:
        model = Muscle
