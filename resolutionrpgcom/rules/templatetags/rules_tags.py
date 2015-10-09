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
def section_text(sections, skills_context, autoescape=True):
    skills = skills_context["skills"]
    skill_types = skills_context["skill_types"]
    skill_specializations = skills_context["skill_specializations"]

    if autoescape:
        escaper = conditional_escape
    else:
        escaper = lambda x: x

    output = []
    table = []

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

        # at the end of the skill list section, add all of the skills as a list
        if item.title == 'Skill List':
            tabs += 1
            # create table to insert into document
            table.append('<table id="skill-list-table" class="col-1-left table table-right-wrap">')
            table.append('<caption>skill list</caption>')
            table.append('<tbody>')

            output.append('<div id="skill-text-list" class="section-content">')

            # set skill classes variable equal to list of distinct classes from skills
            skill_classes_list = skills.values_list('skill_class', flat=True).distinct()
            skill_classes = sorted(list(set(skill_classes_list)))

            # iterate through classes
            for skill_class in skill_classes:
                tabs += 1

                # create title
                output.append('<div class="skill-class-title">%s Skills</div>' % skill_class)

                # add label to table
                table.append('<tr><th>%s Skills</th><th>Base Aptitude</th></tr>' % skill_class)

                # get current skills of this class
                current_skills = skills.filter(skill_class=skill_class)

                # iterate through current skills
                for skill in current_skills:
                    # set variables
                    current_types = skill_types.filter(base_skill=skill)
                    has_types = current_types.exists()
                    current_specializations = skill_specializations.filter(base_skill=skill)
                    has_specializations = current_specializations.exists()

                    # set the skill name
                    skill_name = skill.name
                    if has_types:
                        skill_name += " ()"

                    # create the skill div, title the skill
                    output.append('<div class="skill-div">')
                    output.append('<div class="skill-title">%s</div>' % skill_name)
                    output.append('<div class="skill-content">')

                    # add to the table
                    table.append('<tr><td>%s</td><td>%s</td></tr>' % (skill_name, skill.base_aptitude.name))

                    # add a div for the type thing if necessary
                    if has_types:
                        output.append('<div class="skill-content-typed">Typed skill</div>')

                    # make and label aptitude, what, when
                    output.append('<div class="skill-content-aptitude"><span>Aptitude:</span> %s</div>' % skill.base_aptitude.name)
                    output.append('<div class="skill-content-what"><span>What:</span> %s</div>' % skill.what)
                    output.append('<div class="skill-content-when"><span>When:</span> %s</div>' % skill.when)

                    # create sample types div
                    if has_types:
                        output.append('<div class="skill-content-types"><span>Sample Types:</span> %s</div>' % ', '.join(current_types.values_list('name', flat=True)))

                    # label specializations depending on whether the skill has specializations
                    if has_specializations:
                        output.append('<div class="skill-content-specializations"><span>Specializations:</span> %s</div>' % ', '.join(current_specializations.values_list('name', flat=True)))
                    else:
                        output.append('<div class="skill-content-specializations"><span>Specializations:</span> %s</div>' % skill.specialization_text)

                    # close opened divs
                    output.append('</div>')
                    output.append('</div>')
                # end loop through current skills
                tabs -= 1
            # end loop through skill classes
            output.append('</div>')
            tabs -= 1

            # finish table, insert into document
            table.append('</tbody>')
            table.append('</table>')

        children = sections.filter(parent=item)
        if children.exists():
            for child in children:
                format_children(child)
        tabs -= 1
        output.append('</div>')

    for section in sections.filter(parent__isnull=True):
        format_children(section)

    merged = output + table

    return mark_safe('\n'.join(merged))
