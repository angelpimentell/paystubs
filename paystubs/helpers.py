from django.template.loader import select_template, TemplateDoesNotExist

def check_template_exists(template_name):
    try:
        select_template([template_name])
        return True
    except TemplateDoesNotExist:
        return False