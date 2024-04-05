from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()

@register.filter(name="path_spliter")
@stringfilter
def path_spliter(path:str, arg:int):
    """ cut & return last word of url path """
    return path.split("/")[arg]

