from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Section, Skill, Trait, Equipment
from .serializers import SkillSerializer, SectionSerializer, TraitSerializer, EquipmentSerializer
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
    if name == 'equipment':
        queryset = Equipment.objects.all()
        serializer = EquipmentSerializer(queryset, many=True)

    json = JSONRenderer().render(serializer.data)

    return HttpResponse(json, content_type='application/json')
