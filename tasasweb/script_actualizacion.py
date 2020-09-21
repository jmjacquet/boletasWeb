# -*- coding: utf-8 -*-
#!/usr/bin/python

# import the MySQLdb and sys modules
import MySQLdb
import sys


BASES_EXCEPTUADAS = ('gg_gestion','gg_configuracion','gg_multeo')
LISTA_BASES = "SELECT SCHEMA_NAME FROM `SCHEMATA` WHERE (SCHEMA_NAME LIKE 'gg_%') AND (SCHEMA_NAME NOT IN "+str(BASES_EXCEPTUADAS)+");"

lista_dbs = []
# connection = MySQLdb.connect (host = "www.boletaweb.com.ar", user = "gg", passwd = "battlehome", db = "information_schema")
connection = MySQLdb.connect (host = "localhost", user = "gg", passwd = "battlehome", db = "information_schema", port=3308)
cursor = connection.cursor ()
cursor.execute(LISTA_BASES)
row = cursor.fetchall()
# close the cursor object
cursor.close ()
# close the connection
connection.close ()
lista_dbs = list(row)


#SCRIPT_EJECUCION = "INSERT INTO `configuracion_vars` VALUES(1, 'pago_online', 'Variable de PAGO ONLine a Cajero24', NULL, 'N', NULL);"
#SCRIPT_EJECUCION =INSERT INTO `configuracion_vars` VALUES(2, 'NoComercio', 'Variable de Entidad para Cajero24 ', NULL, NULL, NULL);"
#SCRIPT_EJECUCION =INSERT INTO `configuracion_vars` VALUES(3, 'modif_bases_imp', 'Modificación de Bases Imponibles de Períodos pagados', NULL, 'N', NULL);"
#SCRIPT_EJECUCION ="INSERT INTO `configuracion_vars` VALUES(4, 'dri_retenciones', 'Modificación del campo label de Retenciones en Liquidación y Boleta DReI', NULL, NULL, NULL);"
#SCRIPT_EJECUCION = "INSERT INTO `configuracion_vars` VALUES(5, 'dri_cartel_inicio', 'Cartel que aparece al Liquidar DReI', NULL, NULL, NULL);"
#SCRIPT_EJECUCION = "DELETE FROM `django_session`;"
#SCRIPT_EJECUCION = "ALTER TABLE tributo ADD COLUMN CORRER_VENC_FDESDE DATE NULL;"
#SCRIPT_EJECUCION = "ALTER TABLE tributo ADD COLUMN CORRER_VENC_FHASTA DATE NULL;"
#SCRIPT_EJECUCION = "SELECT t.* FROM tributo as t where t.tipo_interes=7"
SCRIPT_EJECUCION = "SELECT COUNT(*) FROM cuotas;"
#SCRIPT_EJECUCION = "CREATE TABLE `suscriptores`(`id` int(11) NOT NULL  auto_increment ,`tributo` int(11) NOT NULL  , `id_padron` int(11) NOT NULL  , `fecha_alta` date NOT NULL  , \
#	`fecha_baja` date NULL  , PRIMARY KEY (`id`) ) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';"

print "##############################################"
print SCRIPT_EJECUCION

UPDATE_DELETE = False

total_bases = len(lista_dbs)
bases_ok = 0
lista_final=[]
for r in lista_dbs:
	nombre_base = r[0] 
	# db = MySQLdb.connect (host = "www.boletaweb.com.ar", user = "gg", passwd = "battlehome", db =nombre_base)
	db = MySQLdb.connect (host = "localhost", user = "gg", passwd = "battlehome", db =nombre_base, port=3308)
	cursor = db.cursor ()
	try:
		cursor.execute(SCRIPT_EJECUCION)
		if UPDATE_DELETE:			
			db.commit()
			print nombre_base+' --> OK'
		else:
			row = cursor.fetchone()
			for f in row:
				 print nombre_base+' --> '+str(f)
				 lista_final.append([nombre_base,int(f)])
		bases_ok+=1
	except Exception as e:
		print nombre_base+' --> '+str(e)
	# close the cursor object
	cursor.close ()
	# close the connection
	db.close ()
print "##############################################"
print "SCRIPT EJECUTADO CON EXITO EN %s de %s BASES" % (bases_ok,total_bases)


# import operator
# lista_final = sorted(lista_final.items(), key=operator.itemgetter(1),reverse=True)

lista_final = sorted(lista_final, key=lambda x: x[1],reverse=True)

for f in lista_final:
	print f[0]+' --> '+str(f[1])

print lista_final

import csv
csv_file = "cuotas_x_base.csv"

# try:
# 	with open(csv_file, 'w') as f:
# 		for key in lista_final.keys():
# 			f.write("%s,%s\n"%(key,lista_final[key]))
# except IOError:
#     print "I/O error"


f = open(csv_file, "w")
writer = csv.writer(f,delimiter=';', lineterminator='\n')
writer.writerows(lista_final)

f.close()


# exit the program
sys.exit()