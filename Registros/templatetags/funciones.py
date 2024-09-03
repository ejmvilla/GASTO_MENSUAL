from django import template

register = template.Library()

@register.filter()
def Mes(value):
    sMes=""
    if value == 1:
        sMes = "Enero"
    elif value == 2:
        sMes = "Febrero"
    elif value == 3:
        sMes = "Marzo"
    elif value == 4:
        sMes = "Abril"
    elif value == 5:
        sMes = "Mayo"
    elif value == 6:
        sMes = "Junio"
    elif value == 7:
        sMes = "Julio"
    elif value == 8:
        sMes = "Agosto"
    elif value == 9:
        sMes = "Septiembre"
    elif value == 10:
        sMes = "Octubre"
    elif value == 11:
        sMes = "Noviembre"
    elif value == 12:
        sMes = "Diciembre"
    return sMes
