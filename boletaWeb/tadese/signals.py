from django.dispatch import receiver
from django.db.models.signals import pre_delete

from .models import *

# Receive the pre_delete signal and delete the file associated with the model instance.
from django.db.models.signals import post_save


@receiver(post_save, sender=DriPadronActividades)
def DriPadronActividades_save(sender, **kwargs):
    if settings.DEBUG:
    	print "entro!!"
    # dpa = kwargs['instance']
    # boleta_activ = DriBoleta_actividades.objects.filter(id_boleta__id_padron=dpa.id_padron,id_actividad=dpa.id_actividad)
    # print boleta_activ

