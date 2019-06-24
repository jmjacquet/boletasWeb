# -*- coding: utf-8 -*-
from django import forms
from tadese.models import *
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from datetime import datetime,date
from tadese.utilidades import MESES,ANIOS,ADICIONALES,PERIODOS,PrependWidget
from django.contrib import admin
from django.forms.widgets import TextInput,NumberInput
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import Widget
from django.utils.safestring import mark_safe

class PrependWidget(Widget):
    def __init__(self, base_widget, data, *args, **kwargs):
        u"""Initialise widget and get base instance"""
        super(PrependWidget, self).__init__(*args, **kwargs)
        self.base_widget = base_widget(*args, **kwargs)
        self.data = data

    def render(self, name, value, attrs=None):
        u"""Render base widget and add bootstrap spans"""
        field = self.base_widget.render(name, value, attrs)
        return mark_safe((
            u'<div class="input-group">'
            u'    <span class="input-group-addon">%(data)s</span>%(field)s'
            u'</div>'
        ) % {'field': field, 'data': self.data})

class LiqDreiBoletaForm(ModelForm):
    id_padron = forms.IntegerField(widget=forms.HiddenInput) 
    anio = forms.IntegerField(widget=forms.HiddenInput) 
    mes = forms.IntegerField(widget=forms.HiddenInput) 
    vencimiento = forms.DateField(widget=forms.HiddenInput) 
    total = forms.DecimalField(widget=forms.HiddenInput,decimal_places=2)
    adic_detalle = forms.CharField(widget=forms.HiddenInput,required=False)
    adic_select = forms.ChoiceField(choices=ADICIONALES, required=False)
    recargo = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','readonly':'readonly'},base_widget=NumberInput, data=u'Recargo/Punitorios $'),initial=0.00,decimal_places=2,required=False)    
    adic_monto = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False,decimal_places=2) 
    #derecho_neto = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,required=False)    
    derecho_neto = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data=u'Derecho Neto $'),initial=0.00,decimal_places=2,required=False)
    tasa_salud_publ = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data=u'Tasa Salud Pública $'),initial=0.00,decimal_places=2,required=False)
    retenciones = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data='Retenciones $'),initial=0.00,decimal_places=2,required=False)
    minimo_global = forms.DecimalField(widget=forms.HiddenInput,decimal_places=2,required=False)    
    class Meta:
        model = DriBoleta
        exclude = ['fechapago','id_cuota','pago_anterior']

    def __init__(self, *args, **kwargs):        
        super(LiqDreiBoletaForm, self).__init__(*args, **kwargs)
        self.fields['vencimiento'].initial = date.today()                

    def clean(self):
        super(forms.ModelForm,self).clean()
        total = self.cleaned_data['total']              
        derecho_neto = self.cleaned_data['derecho_neto']        
        if derecho_neto:
            if derecho_neto<0:
                self._errors['derecho_neto'] = [u'El importe Derecho Neto debe ser mayor a 0.']
        tasa_salud_publ = self.cleaned_data['tasa_salud_publ']        
        if tasa_salud_publ:
            if tasa_salud_publ<0:
                self._errors['tasa_salud_publ'] = [u'El importe Tasa Salud publ. debe ser mayor a 0.']

       

        if total<0:
            raise forms.ValidationError("El importe total debe ser mayor a 0.")
        
        return self.cleaned_data
    

class LiqDreiRectifForm(ModelForm):
    id_padron = forms.IntegerField(widget=forms.HiddenInput) 
    anio = forms.IntegerField(widget=forms.HiddenInput) 
    mes = forms.IntegerField(widget=forms.HiddenInput) 
    vencimiento = forms.DateField(widget=forms.HiddenInput) 
    total = forms.DecimalField(widget=forms.HiddenInput,decimal_places=2)
    adic_detalle = forms.CharField(widget=forms.HiddenInput,required=False)
    adic_select = forms.ChoiceField(choices=ADICIONALES, required=False)
    adic_monto = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False,decimal_places=2) 
    recargo = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','readonly':'readonly'},base_widget=NumberInput, data=u'Recargo/Punitorios $'),initial=0.00,decimal_places=2,required=False)    
    adic_monto = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False,decimal_places=2) 
    derecho_neto = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data=u'Derecho Neto $'),initial=0.00,decimal_places=2,required=False)
    tasa_salud_publ = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data=u'Tasa Salud Pública $'),initial=0.00,decimal_places=2,required=False)
    retenciones = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data='Retenciones $'),initial=0.00,decimal_places=2,required=False)
    minimo_global = forms.DecimalField(widget=forms.HiddenInput,decimal_places=2,required=False)
    pago_anterior = forms.DecimalField(label='',widget=PrependWidget(attrs={'class':'form-control','step':0.01},base_widget=NumberInput, data=u'Importe ya Abonado (boleta a Rectificar) $'),initial=0.00,decimal_places=2,required=False)
    
    class Meta:
        model = DriBoleta
        exclude = ['fechapago','id_cuota']
        
    def __init__(self, *args, **kwargs):        
        super(LiqDreiRectifForm, self).__init__(*args, **kwargs)
        self.fields['vencimiento'].initial = date.today() 


    def clean(self):
        pago_anterior = self.cleaned_data['pago_anterior']        
        if pago_anterior<=0:
            self._errors['pago_anterior'] = [u'El importe pagado debe ser mayor a 0.']
        return self.cleaned_data
  
class LiqDreiActivForm(ModelForm):       
    id_actividad = forms.IntegerField(widget=forms.HiddenInput) 
    impuesto = forms.DecimalField(widget=forms.HiddenInput) 
    base = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    alicuota = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    activ_descr = forms.CharField(label='',widget=forms.Textarea(attrs={ 'readonly':'readonly','rows': 2, 'cols':60}),max_length=200, required=False)               
    minimo = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    class Meta:
        model = DriBoleta_actividades
        exclude = ['id']

    def __init__(self, *args, **kwargs):
        super(LiqDreiActivForm, self).__init__(*args, **kwargs)
        sitio = Configuracion.objects.get(id=settings.MUNI_ID)
        if sitio.alicuota_fija=='S':
            self.fields['alicuota'].widget.attrs['readonly'] = True
        if sitio.minimo_por_activ=='N':
            self.fields['minimo'].widget.attrs['readonly'] = True    
    
    def clean_id_actividad(self):
        value = self.cleaned_data['id_actividad']
        try:
            return DriActividades.objects.filter(id_actividad=value)[0]
        except:
            raise ValidationError('La Actividad %s no existe!!' % value) 

class EstudioForm(ModelForm):    
    numero = forms.CharField(max_length=10,label='Código') 
    denominacion = forms.CharField(max_length=50,label='Denominación')     
    clave = forms.CharField(widget=forms.PasswordInput(render_value = True),max_length=30,label='Contraseña',required=True) 
    email = forms.EmailField(max_length=50,label='E-Mail Contacto') 
    class Meta:
        model = DriEstudio
        exclude = ['id_estudioc','usuario']
        fields = ['numero', 'denominacion', 'email', 'clave']

class ResponsableForm(ModelForm):    
   nombre = forms.CharField(max_length=50,label='Nombre')     


class AgregarDDJJForm(forms.Form):       
    anio = forms.ChoiceField(choices=ANIOS)

class DriDDJJAForm(ModelForm):
    id_padron = forms.IntegerField(widget=forms.HiddenInput) 
    anio = forms.IntegerField(widget=forms.HiddenInput)  
    total_imponible = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False,decimal_places=2) 
    total_impuestos = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False,decimal_places=2) 
    total_adicionales = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False,decimal_places=2) 
    
    class Meta:
        model = DriDDJJA
        exclude = ['fecha_carga','fecha_confirmado','fecha_impresa']    

class DriDDJJA_actividadesForm(ModelForm):      
    periodo = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly':'readonly'}),required=False) 
    id_boleta = forms.IntegerField(widget=forms.HiddenInput) 
    id_ddjj = forms.IntegerField(widget=forms.HiddenInput) 
    id_actividad = forms.IntegerField(widget=forms.HiddenInput) 
    base = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    alicuota = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    minimo = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    impuesto = forms.DecimalField(widget=forms.HiddenInput) 
    adicionales = forms.DecimalField(widget=forms.NumberInput(attrs={'step':0.01}),decimal_places=2,initial=0.00,min_value=0.00) 
    activ_descr = forms.CharField(max_length=200, required=False) 
    
    class Meta:
        model = DriDDJJA_actividades
        exclude = ['id']    

    def clean_id_actividad(self):
        value = self.cleaned_data['id_actividad']
        try:
            return DriActividades.objects.get(id_actividad=value)
        except DriActividades.DoesNotExist:
            raise ValidationError('La Actividad %s no existe!!' % value) 


class DriBoletaAdmin(admin.ModelAdmin):
    list_display = ('ver_padron','ver_representante', 'anio', 'mes', 'vencimiento','total','id_padron')
    list_display_links = ('id_padron',)
    search_fields = ['ver_representante']
    form = LiqDreiBoletaForm
    
    def ver_padron(self, obj):
        return obj.id_cuota.padron
    def ver_representante(self, obj):
        return obj.id_cuota.id_responsable

    #author_first_name.admin_order_field = 'author__first_name'

    

class BusquedaDDJJForm(forms.Form):      
    contribuyente = forms.CharField(label='Contribuyente',max_length=100,widget=forms.TextInput(attrs={'class':'form-control','text-transform': 'uppercase'}),required=False)     
    padron = forms.CharField(label=u'Nº Padrón',max_length=20,widget=forms.TextInput(attrs={'class':'form-control','text-transform': 'uppercase'}),required=False)     
    anio = forms.ChoiceField(label=u'Año',choices=ANIOS,required=True,initial=date.today().year)
    mes = forms.ChoiceField(label=u'Mes',choices=PERIODOS,required=True,initial=date.today().month)