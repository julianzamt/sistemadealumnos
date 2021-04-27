# Sistema de Alumnos (Spanish)

## A Django app for helping manage student information at the secretary offices of high schools.

It uses Postgres as its database, javascript/css for updating and animating the views, and bootstrap for the layout.

It was tailor-made for the 'EEM 1 DE 2' high school, from Buenos Aires, Argentina, but it could be easily adapted for other institutions as well.

It allows a fully-authorized user to add new students, edit their info, and retrieve them based on a wide variety of optional parameters. 

It provides two different kinds of user accounts: a fully-authorized type called 'Secretario/a', and 'Preceptor/a', which can search for students and edit their grades, but can’t add or edit student’s school documentation-related info. Which type of user each count will be is decided by the app administrator.

For tracking grades, as required by the school it was made for, the app asks for a google sheet link for each student. Thus, in this version, grades are kept as an external resource. 

* Nombre (Name) - Required
* Apellido (Last name) - Required
* DNI (National Document number) - Required
* Año de ingreso (Date of admission) - Required
* Disposición interna (Internal situation) 
* Documento presentado al ingreso (Documentation presented at admission)
    * Certificado de séptimo (Elementary school certificate)
    * Constancia de materias aprobadas (Temporary Certification of approved subjects)
    * Analítico parcial (Certification of approved subjects)
* Calificador anual (Present year degrees)
* Calificador personal (Historical degrees)

The default 'Condition' for every new student is 'Regular'.

Every student could be edited or changed on its condition by 'Gestionar Salida' ('Exit management'). The app admits four different conditions:
* Regular
* Egresado/a (Graduate)
    Gestión del egreso: (Graduation management)
    * Año de egreso (Graduation year)
    * Título confecionado / Fecha (Title made / Date)
    * Título legalizado / Fecha (Title legalized / Date)
    * Título retirado / Fecha (Title retrieved / Date)
    * Libro y Folio (Registry book and page)
* Salido/a con pase (School swap)
    Gestión del pase (School swap management)
    * Pase confeccionado / Fecha (Swap made / Date) 
    * Pase legalizado / Fecha (Swap legalized / Date)
* Salida sin pase (Dismiss)

The app also provides the user with a profile page, where he/she can edit its personal information. Also, from Profile a user can require the admin to upgrade the account type, for editing permissions.

The app gives nicely designed feedback either in success or exceptions when accesing the database. It also displays a custom made 404 page when trying to access non existing endpoints.

This program was made as the final project for 'CS50w Web Programming with Python and JavaScript'.

Julián Zamt, ©2020

---

#### In adittion to common Django files, the app contains:

forms.py: Forms used by the views.
student.js: Process the edition of students.html without reloading the page.
listados.js: Delivers groups of Students grouped by condition to listados.html.
salida.js: Shows different parts of the 'Exit management' form, depending on what the user is asking for, in salida.html.

---

#### Requirements (as in requirements.txt):
asgiref==3.2.10
Django==3.1.2
psycopg2-binary==2.8.6
pytz==2020.1
sqlparse==0.4.1

---

Julián Zamt, November 2020
