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
    specialization_text = models.CharField(max_length=200, default="As appropriate to the type")

    # define choices and the choice block
    INFO = 'information'
    SOCIAL = 'social'
    ACTIVE = 'active'
    COMBAT = 'combat'
    CLASS_CHOICES = (
        (INFO, 'Information'),
        (SOCIAL, 'Social'),
        (ACTIVE, 'Active'),
        (COMBAT, 'Combat')
    )

    skill_class = models.CharField(max_length=11, choices=CLASS_CHOICES)


class SkillType(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, default='type')
    base_skill = models.ForeignKey(Skill)


class SkillSpecialization(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=50, default='specialization')
    base_skill = models.ForeignKey(Skill)


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
            if section.depth_string != relations[section.id]:
                Section.objects.filter(id=section.id).update(depth_string=relations[section.id])

    @staticmethod
    def list_section_relations():
        child_list = {}
        sections = Section.objects.filter(parent__isnull=True).order_by('order')
        depth = [1]

        def get_children(child):
            depth_string = '.'.join([str(i) for i in depth])
            child_list[child.id] = depth_string

            children = Section.objects.filter(parent=child).order_by('order')
            if children.exists():
                depth.append(1)
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

    def top_parent(self):
        output = self
        while output.has_parent():
            output = output.parent
        return output

    def has_child(self):
        try:
            child = self.parent.title
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
    SUBSECTION = 's'
    EXAMPLE = 'ex'
    INFO = 'i'
    TYPE_CHOICES = (
        (NORMAL, 'Normal'),
        (SUBSECTION, 'Subsection'),
        (EXAMPLE, 'Example'),
        (INFO, 'Info Block')
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
