from django import template
register = template.Library()
#Filtro para agregar css a los formfields (bootstrapearlo)
@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})


