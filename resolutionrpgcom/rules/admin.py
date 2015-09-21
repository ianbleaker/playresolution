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
        tier = obj.tier()
        prepend = ""
        while tier > 0:
            prepend += "-"
            tier -= 1
        return "%s %s" % (prepend, obj.title)


# form field to include choice field above
class SectionAdminForm(forms.ModelForm):
    parent = SectionParentChoiceField(queryset=Section.objects.all())

    class Meta:
        model = Section
        fields = '__all__'


# include written form to include choice field change
class SectionAdmin(admin.ModelAdmin):
    form = SectionAdminForm
    list_display = ('title', 'type', 'terse')

admin.site.register(Section, SectionAdmin)
