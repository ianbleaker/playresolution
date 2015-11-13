from django.contrib import admin
from django import forms
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from .py.subclasses import DisableableSelect
from ordered_model.admin import OrderedModelAdmin

# Register your models here.

admin.site.register(Species)
admin.site.register(Aptitude)
admin.site.register(Statistic)
admin.site.register(DerivedStatistic)


# EQUIPMENT ADMIN
class EquipmentModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'sub_category', 'cost', 'short_description')
    ordering = ('category', 'sub_category', 'name')

admin.site.register(Equipment, EquipmentModelAdmin)

###############
# TRAIT ADMIN #
###############
class TraitModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'value', 'short_description')
    ordering = ('type', 'name')

admin.site.register(Trait, TraitModelAdmin)


###############
# SKILL ADMIN #
###############
class SkillTypeInline(admin.TabularInline):
    model = SkillType
    extra = 0


class SkillSpecializationInline(admin.TabularInline):
    model = SkillSpecialization
    extra = 0


class SkillModelAdmin(admin.ModelAdmin):
    fields = ['name', 'base_aptitude', 'skill_class', 'what', 'when', 'specialization_text']
    inlines = [SkillTypeInline, SkillSpecializationInline]

admin.site.register(Skill, SkillModelAdmin)


#################
# SECTION ADMIN #
#################
class SectionParentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        disabled = ''
        model_id = self.initial['model_id']
        try:
            current_model = self._queryset.get(id=model_id)
            children = self._queryset.filter(depth_string__startswith=current_model.depth_string)
            if obj in children:
                disabled = ' [child]disable_option'
            if obj.title == current_model.title:
                disabled = ' [current]disable_option'
        except ObjectDoesNotExist:
            pass

        if obj.type != 'n':
            content_type = "(" + obj.type + ")"
        else:
            content_type = ""

        return "%s - %s %s%s" % (obj.depth_string, obj.title, content_type, disabled)


# form field to include choice field above
class SectionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SectionAdminForm, self).__init__(*args, **kwargs)
        self.fields['parent'].initial = {'model_id': self.instance.id}

    parent = SectionParentChoiceField(
        queryset=Section.objects.all(),
        required=False,
        widget=DisableableSelect
    )

    class Meta:
        model = Section
        exclude = ('depth_string',)


# include written form to include choice field change
class SectionAdmin(OrderedModelAdmin):
    form = SectionAdminForm
    list_display = ('title', 'type', 'terse', 'depth_string', 'order')
    ordering = ('depth_string',)


admin.site.register(Section, SectionAdmin)
