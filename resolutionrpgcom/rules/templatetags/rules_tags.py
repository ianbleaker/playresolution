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
        output.append('%s<li><a id="%s-%s-a" href="#%s-%s">%s</a>' % (indent, item.top_parent().slug(), item.slug(), item.top_parent().slug(), item.slug(), item.title))
        if item.tier() == 1:
            output.append('<div class="left-menu-reveal closed"><i class="material-icons">keyboard_arrow_down</i></div>')
            output.append('<div class="ul-wrapper" id="%s-%s-ul">' % (item.top_parent().slug(), item.slug()))
        children = sections.filter(parent=item)
        if children.exists():
            tabs += 1
            output.append('%s<ul>' % indent)
            for child in children:
                if "ex" not in child.type and "i" not in child.type:
                    format_children(child)
            output.append('%s</ul>' % indent)
            tabs -= 1
        if item.tier() == 1:
            output.append('</div>')
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
        scrollspy = ""
        if "ex" in item.type or "n" in item.type:
            scrollspy = " scrollspy"
        output.append('%s<div id="%s-%s" class="rule-section section-type-%s tier-%s%s%s">' % (indent, item.top_parent().slug(), item.slug(), item.type, item.tier(), type_string, scrollspy))
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
