from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
register = template.Library()

#DropDownHelper
@register.simple_tag
def ParameterListFor(*args, **kwargs):
    list = defaultnull(kwargs,'list')                       #資料列表
    html_id =  defaultnull(kwargs,'html_id')                #該控制項的ID
    pleaseselect=  defaultnull(kwargs,'pleaseselect')       #預設的字串
    selectitem=  defaultnull(kwargs,'selectitem')           #預選項目
    HtmlClass=defaultnull(kwargs,'HtmlClass')               #該控制項的CLASS
    HtmlStyle=defaultnull(kwargs,'HtmlStyle')
    if HtmlClass=='':
        HtmlClass="form-control rounded-0 col-xl-3 col-sm-6 mb-3"
    if HtmlStyle!='':
        HtmlStyle="style='"+HtmlStyle+"'"

    selecthelper='<select class="%s" id="%s" name="%s" %s>' % (HtmlClass,html_id,html_id,HtmlStyle)
    if pleaseselect != '':
        selecthelper='%s<option value="">%s</option>' % (selecthelper,pleaseselect)

    for key,val in list:
        if pleaseselect == '' and selectitem==key:
            selecthelper='%s<option value=%s selected="selected">%s</option>' % (selecthelper,key,val)
        else:
            selecthelper='%s<option value=%s>%s</option>' % (selecthelper,key,val)
    return mark_safe(selecthelper+'</select>')

#如果值為None則帶入空值
def defaultnull(kwargs,key):
    try:
        return kwargs[key]
    except:
        return ''
