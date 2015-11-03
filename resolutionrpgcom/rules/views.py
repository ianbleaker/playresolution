from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Section, Skill, Trait
from .serializers import SkillSerializer, SectionSerializer, TraitSerializer
from rest_framework.renderers import JSONRenderer


def rules(request):
    return render(request, 'rules/base.html')


def query_json(request, name):
    if name == 'sections':
        queryset = Section.objects.all().order_by('depth_string')
        serializer = SectionSerializer(queryset, many=True)
    if name == 'skills':
        queryset = Skill.objects.all().select_related()
        serializer = SkillSerializer(queryset, many=True)
    if name == 'traits':
        queryset = Trait.objects.all()
        serializer = TraitSerializer(queryset, many=True)

    json = JSONRenderer().render(serializer.data)

    return HttpResponse(json, content_type='application/json')
