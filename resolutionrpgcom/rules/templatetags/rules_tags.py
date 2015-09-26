from django import template

from django.utils.encoding import force_text
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from django.utils.text import slugify

register = template.Library()


@register.filter(is_safe=True, needs_autoescape=True)
def child_nav_list(sections, autoescape=True):
    if autoescape:
        escaper = conditional_escape
    else:
        escaper = lambda x: x

    output = []

    def format_children(item, tabs=1):
        indent = '\t' * tabs
        shadow_string = ""
        if item.tier() is 1:
            shadow_string = ' class="z-depth-1"'
        output.append('%s<li role="presentation"><a href="#%s"%s>%s</a>' % (indent, slugify(item.title), shadow_string, item.title))
        children = sections.filter(parent=item)
        if children.exists():
            tabs += 1
            output.append('%s<ul class="nav nav-stacked">' % indent)
            for child in children:
                if "ex" not in child.type and "i" not in child.type:
                    format_children(child)
            output.append('%s</ul>' % indent)
            tabs -= 1
        output.append('%s</li>' % indent)

    for section in sections.filter(parent__isnull=True):
        format_children(section)

    return mark_safe('\n'.join(output))

@register.filter(is_safe=True, needs_autoescape=True)
def section_text(sections, autoescape=True):
    if autoescape:
        escaper = conditional_escape
    else:
        escaper = lambda x: x

    output = []

    def format_children(item, tabs=1):
        indent = '\t' * tabs
        output.append('%s<div id="%s" class="rule-section section-type-%s scrollspy">' % (indent, slugify(item.title), section.type))
        tabs += 1
        output.append('%s<div id="%s-title" class="section-title">%s</div>' % (indent, slugify(item.title), item.title))
        output.append('%s<div id="%s-content" class="section-content">%s</div>' % (indent, slugify(item.title), item.content))
        children = sections.filter(parent=item)
        if children.exists():
            for child in children:
                format_children(child)
        tabs -= 1
        output.append('%s</div>' % indent)

    for section in sections.filter(parent__isnull=True):
        format_children(section)

    return mark_safe('\n'.join(output))
