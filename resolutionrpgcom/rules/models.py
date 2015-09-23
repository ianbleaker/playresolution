from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from ordered_model.models import OrderedModel
from django.db import transaction


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


class Section(OrderedModel):
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Section, self).save(*args, **kwargs)
        self.update_all_depths()

    @transaction.atomic
    def update_all_depths(self):
        sections = Section.objects.all()
        relations = Section.list_section_relations()
        for section in sections:
            if section.depth_string != relations[section.title]:
                Section.objects.filter(id=section.id).update(depth_string=relations[section.title])

    @staticmethod
    def list_section_relations():
        child_list = {}
        sections = Section.objects.filter(parent__isnull=True)
        depth = [1]

        def get_children(child):
            depth_string = '.'.join([str(i) for i in depth])
            child_list[child.title] = depth_string

            depth.append(1)
            children = Section.objects.filter(parent=child).order_by('order')
            for sub_child in children:
                get_children(sub_child)
                depth[-1] += 1
            depth.pop()

        for section in sections:
            get_children(section)
            depth[0] += 1

        return child_list

    def has_parent(self):
        try:
            parent = self.parent.title
            answer = True
        except AttributeError:
            answer = False
        return answer

    def tier(self):
        tier_number = len(self.depth_string.split('.'))
        return tier_number

    def slug(self):
        slug = slugify(self.title)
        return slug

    # define choices and the choice block
    NORMAL = 'n'
    EXAMPLE = 'ex'
    INFO = 'i'
    TYPE_CHOICES = (
        (NORMAL, 'Normal'),
        (EXAMPLE, 'Example'),
        (INFO, 'Information Block')
    )

    title = models.CharField(max_length=50, default='Section Title')
    terse = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=NORMAL)
    content = RichTextField(blank=True, null=True)
    depth_string = models.CharField(max_length=19, blank=True, null=True)
    order_with_respect_to = 'parent'

    class Meta:
        pass
