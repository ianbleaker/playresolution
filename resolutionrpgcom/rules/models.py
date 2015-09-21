from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


# Create your models here.
class Aptitude(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField()


class Statistic(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    derived = models.ForeignKey('DerivedStatistic', blank=True, null=True)


class DerivedStatistic(models.Model):
    def __str__(self):
        return "({}+{})/{}".format(self.dividend_a, self.dividend_b, self.divisor)
    dividend_a = models.ForeignKey('Aptitude', related_name='dividend_a')
    dividend_b = models.ForeignKey('Aptitude', related_name='dividend_b')
    divisor = models.IntegerField(default=5)


class Trait(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    value = models.IntegerField(default=10)
    race_requisite = models.CharField(max_length=20, blank=True, null=True)
    trait_requisite = models.ForeignKey('self', blank=True, null=True)


class Skill(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=200)
    base_aptitude = models.ForeignKey(Aptitude)
    what = models.TextField(default='what')
    when = models.TextField(default='when')


class SkillDescriptor(models.Model):
    def __str__(self):
        return self.name

    # define choices and choice block
    TYPE = 'type'
    SPECIAL = 'special'
    DESCRIPTOR_CHOICES = (
        (TYPE, 'Skill Type'),
        (SPECIAL, 'Skill Specialization')
    )

    base_skill = models.ForeignKey('Skill')
    descriptor = models.CharField(max_length=7, choices=DESCRIPTOR_CHOICES, default=SPECIAL)
    name = models.CharField(max_length=50, default='type')


class Section(models.Model):
    def __str__(self):
        return self.title

    def has_parent(self):
        try:
            parent = self.parent.title
            answer = True
        except AttributeError:
            answer = False
        return answer

    def tier(self):
        tier_number = 0
        section = self
        while section.has_parent():
            tier_number += 1
            section = section.parent
        return tier_number

    def slug(self):
        slug = slugify(self.title)
        return slug

    # define choices and the choice block
    NORMAL = 'normal'
    EXAMPLE = 'example'
    INFO = 'info'
    TYPE_CHOICES = (
        (NORMAL, 'Normal Text'),
        (EXAMPLE, 'Play Example'),
        (INFO, 'Information Block')
    )

    title = models.CharField(max_length=50, default='Section Title')
    terse = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=NORMAL)
    content = RichTextField(blank=True, null=True)

    class Meta:
        order_with_respect_to = 'parent'
