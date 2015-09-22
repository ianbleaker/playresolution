from django.contrib import admin
from django import forms
from .models import *

# Register your models here.

admin.site.register(Aptitude)
admin.site.register(Statistic)
admin.site.register(DerivedStatistic)
admin.site.register(Trait)
admin.site.register(Skill)
admin.site.register(SkillDescriptor)


#################
# SECTION ADMIN #
#################
# choice field; if something has a parent, add "-" equal to number of parents
class SectionParentChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        section_depth = Section.list_section_relations()
        prepend = section_depth[obj.title]

        model_id = self.initial['model_id']
        current_model = Section.objects.get(id=model_id)
        children = current_model.list_all_children()

        disabled = ''
        if obj.title in children:
            disabled = '[child]disable_option'
        if obj.title == current_model.title:
            disabled = '[current]disable_option'

        if obj.type != 'n':
            content_type = "(" + obj.type + ")"
        else:
            content_type = ""

        return "%s - %s %s%s" % (prepend, obj.title, content_type, disabled)


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
        fields = '__all__'


# include written form to include choice field change
class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    list_display = ('title', 'sibling_depth', 'type', 'terse')

admin.site.register(Section, SectionAdmin)
