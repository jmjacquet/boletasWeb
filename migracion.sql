
/* Foreign Keys must be dropped in the target to ensure that requires changes can be done*/

ALTER TABLE `dri_estudio_padron` 
	DROP FOREIGN KEY `dri_estudio_padr_id_estudioc_4b779994_fk_dri_estudio_id_estudioc`  ;

ALTER TABLE `web_liquidacion_ctas` 
	DROP FOREIGN KEY `web_li_id_liquidacion_226b5930_fk_web_liquidacion_id_liquidacion`  , 
	DROP FOREIGN KEY `web_liquidacion_ctas_id_cuota_2eb0e28e_fk_cuotas_id_cuota`  ;


/* Alter table in target */
ALTER TABLE `auth_group_permissions` 
	ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) , 
	ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`,`permission_id`) , 
	DROP KEY `group_id` , 
	DROP KEY `permission_id_refs_id_6ba0f519` , 
	DROP FOREIGN KEY `group_id_refs_id_f4b32aac`  , 
	DROP FOREIGN KEY `permission_id_refs_id_6ba0f519`  ;
ALTER TABLE `auth_group_permissions`
	ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` 
	FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) , 
	ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` 
	FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ;


/* Alter table in target */
ALTER TABLE `auth_permission` 
	CHANGE `name` `name` varchar(255)  COLLATE utf8_general_ci NOT NULL after `id` , 
	ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`,`codename`) , 
	DROP KEY `content_type_id` , 
	DROP FOREIGN KEY `content_type_id_refs_id_d043b34a`  ;
ALTER TABLE `auth_permission`
	ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` 
	FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ;


/* Alter table in target */
ALTER TABLE `auth_user` 
	CHANGE `username` `username` varchar(150)  COLLATE utf8_general_ci NOT NULL after `is_superuser` , 
	CHANGE `email` `email` varchar(254)  COLLATE utf8_general_ci NOT NULL after `last_name` , 
	CHANGE `date_joined` `date_joined` datetime(6)   NOT NULL after `is_active` ;

/* Alter table in target */
ALTER TABLE `auth_user_groups` 
	ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) , 
	ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`,`group_id`) , 
	DROP KEY `group_id_refs_id_274b862c` , 
	DROP KEY `user_id` , 
	DROP FOREIGN KEY `group_id_refs_id_274b862c`  , 
	DROP FOREIGN KEY `user_id_refs_id_40c41112`  ;
ALTER TABLE `auth_user_groups`
	ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` 
	FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) , 
	ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` 
	FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ;


/* Alter table in target */
ALTER TABLE `auth_user_user_permissions` 
	ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) , 
	ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`,`permission_id`) , 
	DROP KEY `permission_id_refs_id_35d9ac25` , 
	DROP KEY `user_id` , 
	DROP FOREIGN KEY `permission_id_refs_id_35d9ac25`  , 
	DROP FOREIGN KEY `user_id_refs_id_4dc23c39`  ;
ALTER TABLE `auth_user_user_permissions`
	ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` 
	FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) , 
	ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` 
	FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ;


/* Alter table in target */
ALTER TABLE `configuracion` 
	CHANGE `nombre` `nombre` varchar(100)  COLLATE utf8_general_ci NULL after `id` , 
	CHANGE `direccion` `direccion` varchar(100)  COLLATE utf8_general_ci NULL after `nombre` , 
	CHANGE `varios1` `varios1` varchar(100)  COLLATE utf8_general_ci NULL after `direccion` , 
	CHANGE `punitorios` `punitorios` decimal(15,4)   NULL after `varios1` , 
	CHANGE `tipo_punitorios` `tipo_punitorios` int(11)   NULL after `punitorios` , 
	CHANGE `linea1` `linea1` varchar(100)  COLLATE utf8_general_ci NULL after `tipo_punitorios` , 
	CHANGE `linea2` `linea2` varchar(100)  COLLATE utf8_general_ci NULL after `linea1` , 
	CHANGE `link_retorno` `link_retorno` varchar(100)  COLLATE utf8_general_ci NULL after `linea2` , 
	CHANGE `mantenimiento` `mantenimiento` int(11)   NULL after `link_retorno` , 
	CHANGE `ncuerpo1` `ncuerpo1` varchar(20)  COLLATE utf8_general_ci NULL after `mantenimiento` , 
	CHANGE `ncuerpo2` `ncuerpo2` varchar(20)  COLLATE utf8_general_ci NULL after `ncuerpo1` , 
	CHANGE `ncuerpo3` `ncuerpo3` varchar(20)  COLLATE utf8_general_ci NULL after `ncuerpo2` , 
	CHANGE `codigo_visible` `codigo_visible` varchar(1)  COLLATE utf8_general_ci NULL after `ncuerpo3` , 
	CHANGE `debug` `debug` varchar(1)  COLLATE utf8_general_ci NULL after `codigo_visible` , 
	CHANGE `alicuota_unidad` `alicuota_unidad` varchar(10)  COLLATE utf8_general_ci NULL after `diasExtraVencim` , 
	CHANGE `alicuota_coeficiente` `alicuota_coeficiente` decimal(15,2)   NULL after `alicuota_unidad` , 
	CHANGE `detalleContrib` `detalleContrib` varchar(300)  COLLATE utf8_general_ci NULL after `alicuota_coeficiente` , 
	CHANGE `ver_unico_padron` `ver_unico_padron` varchar(1)  COLLATE utf8_general_ci NULL after `detalleContrib` , 
	CHANGE `liquidacion_web` `liquidacion_web` varchar(1)  COLLATE utf8_general_ci NULL after `ver_unico_padron` , 
	CHANGE `codigo_link_visible` `codigo_link_visible` varchar(1)  COLLATE utf8_general_ci NULL after `liquidacion_web` , 
	CHANGE `longitudCodigoBarra` `longitudCodigoBarra` int(11)   NULL after `codigo_link_visible` , 
	CHANGE `minimo_por_activ` `minimo_por_activ` varchar(1)  COLLATE utf8_general_ci NULL after `longitudCodigoBarra` , 
	CHANGE `alicuota_fija` `alicuota_fija` varchar(1)  COLLATE utf8_general_ci NULL after `minimo_por_activ` , 
	CHANGE `puede_rectificar` `puede_rectificar` varchar(1)  COLLATE utf8_general_ci NULL after `alicuota_fija` ;

/* Alter table in target */
ALTER TABLE `cuotas` 
	CHANGE `anio` `anio` int(11)   NULL after `id_unidad` , 
	CHANGE `cuota` `cuota` varchar(4)  COLLATE utf8_general_ci NULL after `anio` , 
	CHANGE `saldo` `saldo` decimal(15,2)   NULL after `cuota` , 
	CHANGE `id_padron` `id_padron` varchar(20)  COLLATE utf8_general_ci NULL after `vencimiento` , 
	CHANGE `padron` `padron` varchar(20)  COLLATE utf8_general_ci NULL after `id_padron` , 
	CHANGE `estado` `estado` int(11)   NULL after `fechapago` , 
	ADD COLUMN `piso` varchar(2)  COLLATE utf8_general_ci NULL after `segundo_vencimiento` , 
	ADD COLUMN `nombre` varchar(100)  COLLATE utf8_general_ci NULL after `piso` , 
	ADD COLUMN `sexo` varchar(1)  COLLATE utf8_general_ci NULL after `nombre` , 
	ADD COLUMN `codseg` varchar(10)  COLLATE utf8_general_ci NULL after `sexo` , 
	ADD COLUMN `numero` int(11)   NULL after `codseg` , 
	ADD COLUMN `calle` varchar(35)  COLLATE utf8_general_ci NULL after `numero` , 
	ADD COLUMN `nombre_boleta` varchar(30)  COLLATE utf8_general_ci NULL after `calle` , 
	ADD COLUMN `depto` varchar(2)  COLLATE utf8_general_ci NULL after `nombre_boleta` , 
	ADD COLUMN `nrodocu` varchar(30)  COLLATE utf8_general_ci NULL after `depto` , 
	ADD COLUMN `localidad` varchar(25)  COLLATE utf8_general_ci NULL after `nrodocu` , 
	ADD COLUMN `fecha_audit` datetime(6)   NULL after `localidad` , 
	ADD KEY `cuotas_05167f1e`(`padron`) , 
	DROP KEY `cuotas_48431b1b` , 
	DROP KEY `cuotas_5c4ed745` , 
	DROP KEY `cuotas_6fc8e14d` , 
	DROP KEY `cuotas_deec8ae2` , 
	ADD KEY `cuotas_e2d7f44b`(`id_padron`) , 
	ADD KEY `cuotas_id_responsable_2a338dcc_fk_responsables_id_responsable`(`id_responsable`) , 
	ADD KEY `cuotas_tributo_4eefbc14_fk_tributo_id_tributo`(`tributo`) ;
ALTER TABLE `cuotas`
	ADD CONSTRAINT `cuotas_tributo_4eefbc14_fk_tributo_id_tributo` 
	FOREIGN KEY (`tributo`) REFERENCES `tributo` (`id_tributo`) ;


/* Alter table in target */
ALTER TABLE `django_admin_log` 
	CHANGE `object_id` `object_id` longtext  COLLATE utf8_general_ci NULL after `action_time` , 
	CHANGE `object_repr` `object_repr` varchar(200)  COLLATE utf8_general_ci NOT NULL after `object_id` , 
	CHANGE `change_message` `change_message` longtext  COLLATE utf8_general_ci NOT NULL after `action_flag` , 
	DROP KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` , 
	ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) , 
	DROP KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` , 
	ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id`) , 
	DROP FOREIGN KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id`  , 
	DROP FOREIGN KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id`  , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;
ALTER TABLE `django_admin_log`
	ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` 
	FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) , 
	ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` 
	FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ;


/* Alter table in target */
ALTER TABLE `django_content_type` 
	DROP KEY `app_label` , 
	ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`,`model`) ;

/* Alter table in target */
ALTER TABLE `django_migrations` 
	CHANGE `app` `app` varchar(255)  COLLATE utf8_general_ci NOT NULL after `id` , 
	CHANGE `name` `name` varchar(255)  COLLATE utf8_general_ci NOT NULL after `app` , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `django_session` 
	CHANGE `session_key` `session_key` varchar(40)  COLLATE utf8_general_ci NOT NULL first , 
	CHANGE `session_data` `session_data` longtext  COLLATE utf8_general_ci NOT NULL after `session_key` , 
	DROP KEY `django_session_de54fa62` , 
	ADD KEY `django_session_expire_date_a5c62663`(`expire_date`) , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `django_site` 
	CHANGE `domain` `domain` varchar(100)  COLLATE utf8_general_ci NOT NULL after `id` , 
	CHANGE `name` `name` varchar(50)  COLLATE utf8_general_ci NOT NULL after `domain` , 
	ADD UNIQUE KEY `django_site_domain_a2e37b91_uniq`(`domain`) , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `dri_actividades` 
	CHANGE `minimo` `minimo` decimal(18,2)   NULL after `id_subrubro` ;

/* Alter table in target */
ALTER TABLE `dri_boleta` 
	CHANGE `id_cuota` `id_cuota` int(11)   NULL after `retenciones` , 
	DROP KEY `dri_boleta_2e98c605` , 
	DROP KEY `dri_boleta_6fc8e14d` , 
	ADD KEY `dri_boleta_e2d7f44b`(`id_padron`) , 
	ADD KEY `dri_boleta_id_cuota_1f0002de_fk_cuotas_id_cuota`(`id_cuota`) , 
	DROP FOREIGN KEY `id_cuota_refs_id_cuota_d225de19`  ;

/* Alter table in target */
ALTER TABLE `dri_boleta_actividades` 
	CHANGE `base` `base` decimal(15,2)   NULL after `id_actividad` , 
	ADD KEY `dri_boleta_actividade_id_boleta_350993cc_fk_dri_boleta_id_boleta`(`id_boleta`) , 
	DROP KEY `dri_boleta_actividades_931d7b9a` , 
	DROP KEY `dri_boleta_actividades_a8d4e7cf` , 
	ADD KEY `dri_boleta_id_actividad_17e62655_fk_dri_actividades_id_actividad`(`id_actividad`) , 
	DROP FOREIGN KEY `id_actividad_refs_id_actividad_9964c5b9`  , 
	DROP FOREIGN KEY `id_boleta_refs_id_boleta_6a7f7151`  ;
ALTER TABLE `dri_boleta_actividades`
	ADD CONSTRAINT `dri_boleta_actividade_id_boleta_350993cc_fk_dri_boleta_id_boleta` 
	FOREIGN KEY (`id_boleta`) REFERENCES `dri_boleta` (`id_boleta`) ON DELETE CASCADE ON UPDATE CASCADE ;


/* Create table in target */
CREATE TABLE `dri_cuota_actividad`(
	`id_cuota_actividad` int(11) NOT NULL  auto_increment , 
	`id_padron` int(11) NOT NULL  , 
	`id_actividad` int(11) NOT NULL  , 
	`denominacion` varchar(200) COLLATE utf8_general_ci NULL  , 
	`codigo` varchar(10) COLLATE utf8_general_ci NULL  , 
	`alicuota` decimal(15,2) NULL  , 
	`minimo` decimal(18,2) NULL  , 
	`actividad_principal` varchar(1) COLLATE utf8_general_ci NULL  , 
	`id_cuota` int(11) NULL  , 
	PRIMARY KEY (`id_cuota_actividad`) , 
	KEY `dri_cuota_actividad_id_cuota_072b2a01_fk_cuotas_id_cuota`(`id_cuota`) 
) ENGINE=InnoDB DEFAULT CHARSET='utf8' COLLATE='utf8_general_ci';


/* Alter table in target */
ALTER TABLE `dri_ddjj_actividades` 
	CHANGE `id_boleta` `id_boleta` int(11)   NOT NULL after `periodo` , 
	ADD KEY `dri_ddjj_a_id_actividad_5418123c_fk_dri_actividades_id_actividad`(`id_actividad`) , 
	DROP KEY `dri_ddjj_actividades_931d7b9a` , 
	DROP KEY `dri_ddjj_actividades_a8d4e7cf` , 
	DROP KEY `dri_ddjj_actividades_aff2ac17` , 
	ADD KEY `dri_ddjj_actividades_id_ddjj_7c381882_fk_dri_ddjj_id_ddjj`(`id_ddjj`) , 
	DROP FOREIGN KEY `id_actividad_refs_id_actividad_c2a535f3`  , 
	DROP FOREIGN KEY `id_boleta_refs_id_boleta_6b368c1e`  , 
	DROP FOREIGN KEY `id_ddjj_refs_id_ddjj_987787c3`  ;
ALTER TABLE `dri_ddjj_actividades`
	ADD CONSTRAINT `dri_ddjj_a_id_actividad_5418123c_fk_dri_actividades_id_actividad` 
	FOREIGN KEY (`id_actividad`) REFERENCES `dri_actividades` (`id_actividad`) , 
	ADD CONSTRAINT `dri_ddjj_actividades_id_ddjj_7c381882_fk_dri_ddjj_id_ddjj` 
	FOREIGN KEY (`id_ddjj`) REFERENCES `dri_ddjj` (`id_ddjj`) ;


/* Alter table in target */
ALTER TABLE `dri_estudio` 
	CHANGE `Denominacion` `Denominacion` varchar(100)  COLLATE utf8_general_ci NULL after `id_estudioc` , 
	CHANGE `usuario` `usuario` varchar(30)  COLLATE utf8_general_ci NULL after `Denominacion` , 
	CHANGE `clave` `clave` varchar(30)  COLLATE utf8_general_ci NULL after `usuario` , 
	CHANGE `numero` `numero` varchar(30)  COLLATE utf8_general_ci NULL after `clave` , 
	CHANGE `email` `email` varchar(100)  COLLATE utf8_general_ci NULL after `numero` , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `dri_estudio_padron` 
	CHANGE `id_estudioc` `id_estudioc` int(11)   NULL after `id_negocio` , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `dri_padron_actividades` 
	CHANGE `id` `id` int(11)   NOT NULL auto_increment first , 
	CHANGE `id_padron` `id_padron` int(11)   NOT NULL after `id` , 
	CHANGE `fecha_inicio` `fecha_inicio` date   NULL after `id_actividad` , 
	CHANGE `principal` `principal` varchar(1)  COLLATE utf8_general_ci NOT NULL after `fecha_fin` , 
	CHANGE `expediente` `expediente` varchar(20)  COLLATE utf8_general_ci NOT NULL after `monto_minimo` , 
	ADD KEY `dri_padron_actividades_aecfaef1`(`id_actividad`) , 
	DROP KEY `id` , 
	ADD UNIQUE KEY `id_padron`(`id_padron`,`id_actividad`,`fecha_inicio`) , ENGINE=InnoDB, DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;
ALTER TABLE `dri_padron_actividades`
	ADD CONSTRAINT `dri_padron__id_actividad_f2eb5d2_fk_dri_actividades_id_actividad` 
	FOREIGN KEY (`id_actividad`) REFERENCES `dri_actividades` (`id_actividad`) ;


/* Alter table in target */
ALTER TABLE `sinc` 
	CHANGE `id` `id` int(11)   NOT NULL first , 
	CHANGE `hora` `hora` time(6)   NOT NULL after `fecha` , 
	DROP KEY `sinc_474a6b98` , 
	ADD KEY `sinc_94ed4167`(`fecha`) , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `sinc_pers` 
	CHANGE `id` `id` int(11)   NOT NULL first , 
	CHANGE `hora` `hora` time(6)   NOT NULL after `fecha` , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `tributo` 
	CHANGE `CAJAIMPORTE` `CAJAIMPORTE` varchar(1)  COLLATE utf8_general_ci NULL after `abreviatura` , 
	CHANGE `REPORTE` `REPORTE` varchar(30)  COLLATE utf8_general_ci NULL after `CAJAIMPORTE` , 
	CHANGE `FORMATO` `FORMATO` varchar(20)  COLLATE utf8_general_ci NULL after `INTERES` ;

/* Alter table in target */
ALTER TABLE `tributo_interes` DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `user_profile` 
	DROP FOREIGN KEY `user_id_refs_id_19352c75`  ;

/* Alter table in target */
ALTER TABLE `web_liquidacion` 
	CHANGE `vencimiento` `vencimiento` date   NULL after `tipo` , 
	CHANGE `nominal` `nominal` decimal(10,2)   NULL after `vencimiento` , 
	CHANGE `interes` `interes` decimal(10,2)   NULL after `nominal` , 
	CHANGE `total` `total` decimal(10,2)   NULL after `interes` , 
	CHANGE `pasado_a_cnv` `pasado_a_cnv` int(11)   NULL after `total` , 
	CHANGE `fecha` `fecha` date   NULL after `pasado_a_cnv` , 
	CHANGE `hora` `hora` time(6)   NULL after `fecha` , 
	CHANGE `usuario` `usuario` varchar(30)  COLLATE utf8_general_ci NULL after `hora` , 
	CHANGE `punitorios` `punitorios` decimal(10,2)   NULL after `fecha_punitorios` , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ;

/* Alter table in target */
ALTER TABLE `web_liquidacion_ctas` 
	CHANGE `id_liquidacion` `id_liquidacion` int(11)   NULL after `id` , 
	CHANGE `tributo` `tributo` int(11)   NULL after `id_cuota` , 
	CHANGE `nominal` `nominal` decimal(10,2)   NULL after `tributo` , 
	CHANGE `interes` `interes` decimal(10,2)   NULL after `nominal` , DEFAULT CHARSET='utf8', COLLATE ='utf8_general_ci' ; 


COMMIT;

-- update cuotas as c
-- left join responsables as r on (r.id_responsable=c.id_responsable)
-- set c.piso=r.piso,c.nombre=r.nombre,c.sexo=r.sexo,c.codseg=r.codseg,c.numero=r.numero,c.calle=r.calle,
-- c.nombre_boleta=r.nombre_boleta,c.depto=r.depto,c.nrodocu=r.nrodocu,c.localidad=r.localidad

-- COMMIT;
