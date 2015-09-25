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
            shadow_string = ' class="shadow-z-1"'
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