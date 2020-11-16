from django.db import models
from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):
    secretaria = "Secretaria/o"
    preceptor = "Preceptor/a"
    tipos = [
        (secretaria, "Secretaria/o"),
        (preceptor, "Preceptor/a")
    ]
    user_type = models.CharField(choices=tipos, blank=False, null=False, max_length=64, default=tipos[1][1])

class Alumno(models.Model):
    name = models.CharField(max_length=200, blank=False, error_messages={'required': 'Ingresar nombre ↓'})
    last = models.CharField(max_length=200, blank=False, error_messages={'required': 'Ingresar apellido ↓'})
    dni = models.CharField(max_length=8, blank=False, unique=True, error_messages={'unique': 'Ya existe un estudiante con este DNI ↓', 'required': 'Ingresar DNI ↓'})
    ingreso = models.CharField(max_length=4, blank=False, error_messages={'required': 'Ingresar año de ingreso ↓'})
    disposicion = models.CharField(max_length=6, blank=True, null=True, default=None, unique=True, error_messages={'unique': 'Esta disposición ya fue asignada ↓'})

    # choices de doc_ingreso
    certif_7mo = "Certificado de 7mo"
    constancia = "Constancia de materias aprobadas"
    analitico = "Analítico parcial"
    categories = [
        (certif_7mo, "Certificado de 7mo"),
        (constancia, "Constancia de materias aprobadas"),
        (analitico, "Analítico parcial")
    ]
    doc_ingreso = models.CharField(choices=categories, blank=True, max_length=64)
    
    # En ver 1.0, links a Drive. 2.0 Incluirá la posibilidad Drive / Db Interna
    calif_anual = models.CharField(max_length=200, blank=True, null=True, default=None, unique=True, error_messages={'unique': 'Ya existe un estudiante con este calificador anual ↓'})
    trayectoria = models.CharField(max_length=200, blank=True, null=True, default=None, unique=True, error_messages={'unique': 'Ya existe un estudiante con este calificador personal ↓'})

    # choices de condicion
    regular = "Regular"
    egresado = "Egresado/a"
    salido_con_pase = "Salido con pase"
    salido_sin_pase = "Salido sin pase"
    condicion = [
        (regular, "Regular"),
        (egresado, "Egresado/a"),
        (salido_con_pase, "Salido/a con pase"),
        (salido_sin_pase, "Salido/a sin pase")
    ]
    condicion = models.CharField(choices=condicion, blank=False, null=False, default=regular, max_length=64)

    # Egresados
    egreso = models.CharField(max_length=4, blank=True)
    
    titulo_confeccionado = models.BooleanField(default=False)
    titulo_legalizado = models.BooleanField(default=False)
    titulo_retirado = models.BooleanField(default=False)

    fecha_titulo_confeccionado = models.CharField(max_length=64, blank=True)
    fecha_titulo_legalizado = models.CharField(max_length=64, blank=True)
    fecha_titulo_retirado = models.CharField(max_length=64, blank=True)

    folio = models.CharField(max_length=6, blank=True)
    libro = models.CharField(max_length=6, blank=True)

    # Salidos con pase
    pase_confeccionado = models.BooleanField(default=False)
    pase_legalizado = models.BooleanField(default=False)

    fecha_pase_confeccionado = models.CharField(max_length=64, blank=True)
    fecha_pase_legalizado = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return f"{self.name} {self.last}"


