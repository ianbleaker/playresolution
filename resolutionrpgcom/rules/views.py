from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .models import Section, Skill, SkillType, SkillSpecialization


# Create your views here.
def index(request):
    sections = Section.objects.all().order_by('depth_string')
    skills = Skill.objects.all().order_by('name')
    skill_types = SkillType.objects.all().order_by('name')
    skill_specializations = SkillSpecialization.objects.all().order_by('name')
    skill_context = {'skills': skills, 'skill_types': skill_types, 'skill_specializations': skill_specializations}
    context = {'sections': sections, 'skill_context': skill_context}
    return render(request, 'rules/index.html', context)


def text(request):
    return render(request, 'rules/text.html')


def json_section(request):
    sections = serializers.serialize("json", Section.objects.all().order_by('depth_string'))
    return HttpResponse(sections, content_type='application/json')
