from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter()
def ParameterListFor(list,args, autoescape=True):
    if args is None:
        return ''
    arg_list = [arg.strip() for arg in args.split(',')]
    selecthelper='<select class="form-control rounded-0 col-xl-3 col-sm-6 mb-3" id="%s" name="%s">' % (arg_list[0],arg_list[0])
    try:
        selecthelper='%s<option value="">%s</option>' % (selecthelper,arg_list[1])
    except Exception as e:
        pass

    for key,val in list:
        selecthelper='%s<option value=%s>%s</option>' % (selecthelper,key,val)
    return mark_safe(selecthelper+'</select>')
