from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def ParameterListFor(*args, **kwargs):
    list = defaultnull(kwargs,'list')
    html_id =  defaultnull(kwargs,'html_id')
    pleaseselect=  defaultnull(kwargs,'pleaseselect')
    selectitem=  defaultnull(kwargs,'selectitem')
    HtmlClass=defaultnull(kwargs,'HtmlClass')
    if HtmlClass=='':
        HtmlClass="form-control rounded-0 col-xl-3 col-sm-6 mb-3"

    selecthelper='<select class="%s" id="%s" name="%s">' % (HtmlClass,html_id,html_id)
    if pleaseselect != '':
        selecthelper='%s<option value="">%s</option>' % (selecthelper,pleaseselect)

    for key,val in list:
        if pleaseselect == '' and selectitem==key:
            selecthelper='%s<option value=%s selected="selected">%s</option>' % (selecthelper,key,val)
        else:
            selecthelper='%s<option value=%s>%s</option>' % (selecthelper,key,val)
    return mark_safe(selecthelper+'</select>')
def defaultnull(kwargs,key):
    try:
        return kwargs[key]
    except:
        return ''
