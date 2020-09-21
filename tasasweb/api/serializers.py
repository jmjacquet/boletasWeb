# -*- coding: utf-8 -*-
from rest_framework import serializers 
from tadese.models import Cuotas,Tributo,DriBoleta,DriBoleta_actividades
from tadese.utilidades import ESTADOS

class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        return self._choices[obj]
        
# class ResponsablesSerializer(serializers.ModelSerializer): 	
# 	class Meta: 
# 		model = Responsables
# 		fields = ('id_responsable', 'nombre', 'nrodocu','codseg')

class TributoSerializer(serializers.ModelSerializer): 	
	class Meta: 
		model = Tributo
		fields = ['id_tributo', 'descripcion', 'abreviatura']


class CuotasSerializer(serializers.ModelSerializer): 
	id_cuota = serializers.IntegerField()
	cuota = serializers.IntegerField()
	anio = serializers.IntegerField()
	#tributo = TributoSerializer(read_only=True)
	tributo_nombre = serializers.CharField(read_only=True)	
	tributo_abreviatura = serializers.CharField(read_only=True)	
	estado_nombre = serializers.CharField(source="get_estado",read_only=True)
	class Meta: 
		model = Cuotas
		# exclude = ['fecha_audit']	
		fields = '__all__'


class Boletas_ActividadesSerializer(serializers.ModelSerializer): 		
	class Meta: 
		model = DriBoleta_actividades
		# exclude = ['fecha_audit']
		fields = '__all__'

class BoletasSerializer(serializers.ModelSerializer): 	
	boleta_actividades = Boletas_ActividadesSerializer(many=True,read_only=True)		
	class Meta: 
		model = DriBoleta
		# exclude = ['fecha_audit']
		fields = '__all__'
		



class CustomCuotasSerializer(serializers.Serializer): 
	id_cuota = serializers.IntegerField()
	cuota = serializers.IntegerField()
	anio = serializers.IntegerField()
	nombre_tributo = serializers.CharField(source="tributo__descripcion")	
	padron = serializers.CharField()
	estado = serializers.ChoiceField(choices=ESTADOS)		
	class Meta: 
		model = Cuotas
		# exclude = ['fecha_audit']	
		fields = '__all__'			