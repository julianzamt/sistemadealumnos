from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.core import serializers
from django.urls import reverse, reverse_lazy
from django.db import IntegrityError
from django.http import Http404
from django.forms import ModelForm
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json

from .models import User, Alumno
from .forms import AlumnoNuevoForm, PasswordsChangeForm, salidaForm

# Custom decorator (access level)
# @secretaria_required
secretaria_test = user_passes_test(lambda user: user.user_type == "Secretaria/o", login_url='logout')

def secretaria_required(view_func):
    decorated_view_func = login_required(secretaria_test(view_func))
    return decorated_view_func
####################################

@login_required
def index(request):
    if request.user.is_authenticated:
        return render(request, "secretaria/index.html")
    else:
        return HttpResponseRedirect(reverse("login"))

@login_required
def user_profile(request):
    if request.method == "POST":
        # Update user 
        user = User.objects.get(pk=request.user.pk)
        user.username = request.POST["username"]
        user.first_name = request.POST["name"]
        user.last_name = request.POST["last"]
        user.email = request.POST["email"]

        # Try to udpate
        try:
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "secretaria/index.html", {
                    "message": "El nombre de usuario ya existe.",
                    "is_error": "error"
                })
            
        
        return render(request, "secretaria/index.html", {
            "message": "Perfil actualizado con éxito"
        })
    else:
        return render(request, "secretaria/profile.html")

@login_required
def search(request):
    # Procesa la request de búsqueda de index.html
    if request.method == "POST":
        name = (request.POST["name"]).lower()
        last = (request.POST["last"]).lower()
        dni = request.POST["dni"]
    
        try:
            student = Alumno.objects.get(dni=dni)
            return render(request, 'secretaria/student.html', {
                "student": student
                })

        except:
            students = Alumno.objects.filter(name__unaccent=name, last__unaccent=last)
            students_last = Alumno.objects.filter(last__unaccent=last)
            students_name = Alumno.objects.filter(name__unaccent=name)

            if len(students) == 1:
                student = students[0]
                return render(request, 'secretaria/student.html', {
                    "student": student
                    })
            elif len(students) > 1:
                return render(request, 'secretaria/disambiguation.html', {
                    "students": students,
                    })
            elif len(students_last) == 1:
                student = students_last[0]
                return render(request, 'secretaria/student.html', {
                    "student": student
                    })
            elif len(students_last) != 0:
                return render(request, 'secretaria/disambiguation.html', {
                    "students": students_last,
                    })
            elif len(students_name) != 0:
                return render(request, 'secretaria/disambiguation.html', {
                    "students": students_name,
                    })
            else:
                message = "No encontrado/a"
                return render(request, 'secretaria/error.html', {
                        "message": message
                    })

    # if request.method == GET
    else:
        ctx= {
            'message' : request.GET.get('message'),
            'student_pk' : request.GET.get('pk')
        }

        student = Alumno.objects.get(pk=ctx["student_pk"])

        return render(request, 'secretaria/student.html', {
                    "message": ctx["message"],
                    "student": student
                    })

        return HttpResponse('Hola')

@login_required
@secretaria_required
def student(request):
    # Procesa EDIT de student.html
    if request.method == "PUT":
        edit_info = json.load(request)
        student = Alumno.objects.get(pk=edit_info['pk'])

        student.name = (edit_info["name"]).lower()
        student.last = (edit_info["last"]).lower()
        student.dni = edit_info["dni"]
        student.ingreso = edit_info["ingreso"]
        student.disposicion = edit_info["disposicion"]
        student.doc_ingreso = edit_info["doc_ingreso"]
        student.calif_anual = edit_info["calif_anual"]
        student.trayectoria = edit_info["trayectoria"]

        if student.condicion == "Egresado/a":
            student.egreso = edit_info["egreso"]
            student.libro = edit_info["libro"]
            student.folio = edit_info["folio"]
        
        # Process '' in calif_anual, trayectoria and disposicion
        # to be stored as None
        # (Because uniquiness needs None to don´t
        # equalize the empty string)
        if student.calif_anual == '':
            student.calif_anual = None
        if student.trayectoria == '':
            student.trayectoria = None
        if student.disposicion == '':
            student.disposicion = None
        
        student.save()

        dict_student = model_to_dict(student)
    
    return JsonResponse(dict_student)

@login_required
def listados(request):
    return render(request, "secretaria/listados.html")

@login_required
def listados_process(request):
    condicion = json.load(request)
    listado = Alumno.objects.filter(condicion=condicion).values('pk', 'name', 'last', 'dni', 'ingreso').order_by('last', 'name')
    
    listado_json = json.dumps(list(listado))
    return JsonResponse(listado_json, safe=False)


@login_required
@secretaria_required
def new_student(request):
    if request.method == "POST":
        new_student_form = AlumnoNuevoForm(request.POST)
        if new_student_form.is_valid():
            new_student = new_student_form.save(commit=False)
            
            # lowercase name and last before send them to db
            new_student.name = (new_student.name).lower()
            new_student.last = (new_student.last).lower()
                        
            new_student.save()

            message = "Estudiante ingresado/a con éxito"

            # Retrieve results to index page
            form_ingreso = AlumnoNuevoForm()
            return render(request, "secretaria/index.html", {
                    "form_ingreso": form_ingreso,
                    "message": message,
                })
        
        # if form.is_valid == False
        else:
            message = "Ups!"
            return render(request, "secretaria/new_student.html", {
                    "form_ingreso": new_student_form,
                    "message": message
                })

    # if request.method == GET
    else:
        form_ingreso = AlumnoNuevoForm()
        return render(request, "secretaria/new_student.html", {
                "form_ingreso": form_ingreso,
            })

@login_required
@secretaria_required
def salida(request, student_pk):
    if request.method == "POST":
        student = Alumno.objects.get(pk=student_pk)

        form = salidaForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["condicion"])
            if form.cleaned_data["condicion"] == 'Egresado/a':
                egreso = form.cleaned_data["egreso"]
                condicion = form.cleaned_data["condicion"]
                titulo_confeccionado = form.cleaned_data["titulo_confeccionado"]
                titulo_legalizado = form.cleaned_data["titulo_legalizado"]
                titulo_retirado = form.cleaned_data["titulo_retirado"]
                fecha_titulo_confeccionado = form.cleaned_data["fecha_titulo_confeccionado"]
                fecha_titulo_legalizado = form.cleaned_data["fecha_titulo_legalizado"]
                fecha_titulo_retirado = form.cleaned_data["fecha_titulo_retirado"]
                libro = form.cleaned_data["libro"]
                folio = form.cleaned_data["folio"]

                student.egreso = egreso
                student.condicion = condicion
                student.titulo_confeccionado = titulo_confeccionado
                student.titulo_legalizado = titulo_legalizado
                student.titulo_retirado = titulo_retirado
                student.fecha_titulo_confeccionado = fecha_titulo_confeccionado
                student.fecha_titulo_legalizado = fecha_titulo_legalizado
                student.fecha_titulo_retirado = fecha_titulo_retirado
                student.libro = libro
                student.folio = folio

                student.save()

            elif form.cleaned_data["condicion"] == 'Salido con pase':
                condicion = form.cleaned_data["condicion"]
                pase_confeccionado = form.cleaned_data["pase_confeccionado"]
                pase_legalizado = form.cleaned_data["pase_legalizado"]
                fecha_pase_confeccionado = form.cleaned_data["fecha_pase_confeccionado"]
                fecha_pase_legalizado = form.cleaned_data["fecha_pase_legalizado"]

                student.condicion = condicion
                student.pase_confeccionado = pase_confeccionado
                student.pase_legalizado = pase_legalizado
                student.fecha_pase_confeccionado = fecha_pase_confeccionado
                student.fecha_pase_legalizado = fecha_pase_legalizado
                
                student.save()

            elif form.cleaned_data["condicion"] == 'Salido sin pase':
                condicion = form.cleaned_data["condicion"]

                student.condicion = condicion
                student.save()
            
            elif form.cleaned_data["condicion"] == 'Regular':
                condicion = form.cleaned_data["condicion"]

                student.condicion = condicion
                student.save()
            
            student = Alumno.objects.get(pk=student_pk)

            message = f"La gestión fue procesada con éxito"
            
            return redirect(f'/search?pk={student.pk}&message={message}')
    
    # if request.method == GET
    else:
        student = Alumno.objects.get(pk=student_pk)
        form = salidaForm(initial=model_to_dict(student))
        return render(request, "secretaria/salida.html", {
            "student": student,
            "form": form
        })

######## Login - Logout - Register - 404 - PasswordChange - decorators #########

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "secretaria/login.html", {
                    "message": "Usuario y/o contraseña inválidos"
                })
    else:
        return render(request, "secretaria/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        # Initialize Variables
        username = request.POST["username"]
        name = request.POST["name"]
        last = request.POST["last"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "secretaria/register.html", {
                "message": "Las passwords deben coincidir."
            })
        
        # Ensure no user had register the email before
        try:
            mail_match = User.objects.get(email=email)
            if mail_match:
                return render(request, "secretaria/register.html", {
                "message": "El mail ya existe."
            })
        except:
            pass

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, password=password, email=email, first_name=name, last_name=last)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "secretaria/register.html", {
                "message": "El usuario ya existe."
            })
        
        # Automatically login new user
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    
    # If GET method
    else:
        return render(request, "secretaria/register.html")

def handle404(request, exception):
    return render(request, 'secretaria/404.html', status=404)

class PasswordsChangeView (PasswordChangeView):
    form_class = PasswordsChangeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        message = "Contraseña actualizada con éxito"
        return render(self.request, 'secretaria/index.html', {
            "message": message
        })



