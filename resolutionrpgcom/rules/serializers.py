from rest_framework import serializers
from .models import Skill, Aptitude, SkillSpecialization, SkillType, Section, Trait, Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment


class TraitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trait


class AptitudeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aptitude
        fields = ('id', 'name')


class SkillSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillSpecialization


class SkillTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillType
        field = ('id', 'name')


class SkillSerializer(serializers.ModelSerializer):
    base_aptitude = AptitudeSerializer()
    specializations = SkillSpecializationSerializer(many=True)
    types = SkillTypeSerializer(many=True)

    class Meta:
        model = Skill


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
