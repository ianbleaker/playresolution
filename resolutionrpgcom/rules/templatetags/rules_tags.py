from django import template

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True, needs_autoescape=True)
def section_bookmark_list(sections, autoescape=True):
    if autoescape:
        escaper = conditional_escape
    else:
        escaper = lambda x: x

    output = []

    def format_children(item, tabs=1):
        indent = '\t' * tabs
        shadow_string = ""
        if item.tier() is 1:
            shadow_string = ' class=""'
        output.append('%s<li role="presentation"><a href="#%s-%s"%s>%s</a>' % (indent, item.slug(), item.tier(), shadow_string, item.title))
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
        type_string = ""
        if "ex" in item.type:
            type_string = " card-panel"
        output.append('%s<div id="%s-%s" class="rule-section section-type-%s tier-%s scrollspy%s">' % (indent, item.slug(), item.tier(), item.type, item.tier(), type_string))
        tabs += 1
        output.append('%s<div id="%s-title" class="section-title">%s</div>' % (indent, item.slug(), item.title))
        output.append('%s<div id="%s-content" class="section-content">%s</div>' % (indent, item.slug(), item.content))
        children = sections.filter(parent=item)
        if children.exists():
            for child in children:
                format_children(child)
        tabs -= 1
        output.append('%s</div>' % indent)

    for section in sections.filter(parent__isnull=True):
        format_children(section)

    return mark_safe('\n'.join(output))
