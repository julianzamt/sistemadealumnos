document.addEventListener('DOMContentLoaded', function() {
    /* Initialize variables */
    const editBtn = document.querySelector('#edit');

    /* Edit Student Info */
    editBtn.onclick = () => {

        if (editBtn.innerHTML === "Editar") {
            /* Initialize variables */
            const nameField = document.querySelector('#name');
            const lastField = document.querySelector('#last');
            const dniField = document.querySelector('#dni');
            const ingresoField = document.querySelector('#ingreso');
            const docIngresoField = document.querySelector('#doc_ingreso');
            const disposicionField = document.querySelector('#disposicion');
            const califAnualField = document.querySelector('#calif_anual');
            const trayectoriaField = document.querySelector('#trayectoria');
            
            const textFields = [nameField, lastField, dniField, ingresoField, disposicionField]
            const linkFields = [califAnualField, trayectoriaField]
            
            /* if student.es_egresado == true */
            if (document.querySelector('#es_egresado').value === "True") {
                const egresoField = document.querySelector('#egreso');
                const libroField = document.querySelector('#libro');
                const folioField = document.querySelector('#folio');

                textFields.push(egresoField, libroField, folioField);
            }

            for (let i = 0; i < textFields.length; i++) {
                replace(textFields[i]);
            };

            replaceSelect(docIngresoField);

            for (let i = 0; i < linkFields.length; i++) {
                replaceLink(linkFields[i]);
            };
            
            /* Change Edit to Save */
            editBtn.innerHTML = 'Guardar';
            editBtn.setAttribute('class', 'btn btn-success float-right');
        }
        /* if editBtn === "Guardar" */
        else {
            /* Construct JSON */
            let studentId = document.querySelector('#student-id').value;
            let name = document.querySelector('#name').value;
            let last = document.querySelector('#last').value;
            let dni = document.querySelector('#dni').value;
            let ingreso = document.querySelector('#ingreso').value;
            let disposicion = document.querySelector('#disposicion').value;
            let doc_ingreso = document.querySelector('#doc_ingreso').value;
            let calif_anual = document.querySelector('#calif_anual').value;
            let trayectoria = document.querySelector('#trayectoria').value;
            
            /* if student.es_egresado == True */
            let egreso;
            let folio;
            let libro;

            if (document.querySelector('#es_egresado').value === "True"){
                egreso = document.querySelector('#egreso').value;
                folio = document.querySelector('#folio').value;
                libro = document.querySelector('#libro').value;
            }
            else {
                egreso = '';
                folio = '';
                libro = '';
            }

            editedStudent = {
                "pk" : studentId,
                "name" : name,
                "last" : last,
                "dni": dni, 
                "ingreso" : ingreso,
                "disposicion" : disposicion,
                "doc_ingreso" : doc_ingreso,
                "calif_anual" : calif_anual,
                "trayectoria" : trayectoria,
                "egreso" : egreso,
                "folio" : folio, 
                "libro" : libro
            }

            /* Obtain csrf_token */ 
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            const csrftoken = getCookie('csrftoken');

            /* Send new Data */      
            fetch('student', {
                method:'PUT',
                credentials: 'same-origin',
                headers:{ 
                    'accept': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify(editedStudent)
            })
            .then(response => response.json())
            .then(newStudent => {
                /* Show edited student to user */
                /* Get new replaced tags */
                const nameField = document.querySelector('#name');
                const lastField = document.querySelector('#last');
                const dniField = document.querySelector('#dni');
                const ingresoField = document.querySelector('#ingreso');
                const docIngresoField = document.querySelector('#doc_ingreso');
                const disposicionField = document.querySelector('#disposicion');
                const califAnualField = document.querySelector('#calif_anual');
                const trayectoriaField = document.querySelector('#trayectoria');

                const textFields = [nameField, lastField, dniField, ingresoField, disposicionField, docIngresoField]
                const linkFields = [califAnualField, trayectoriaField]

                /* if student.es_egresado == true */
                if (document.querySelector('#es_egresado').value === "True") {
                    const egresoField = document.querySelector('#egreso');
                    const libroField = document.querySelector('#libro');
                    const folioField = document.querySelector('#folio');

                    textFields.push(egresoField, libroField, folioField);
                }

                /* Show edited student */
                for (let i = 0; i < textFields.length; i++) {
                    reverseReplace(textFields[i], newStudent);
                };

                for (let i = 0; i < linkFields.length; i++) {
                    reverseReplaceLink(linkFields[i], newStudent);
                };
                
                /* Change h1 */
                let studentHeader = document.querySelector('#student-header');
                studentHeader.innerHTML = `${newStudent.name} ${newStudent.last}`;
                let condicionHeader = document.createElement('span');
                condicionHeader.setAttribute('class', 'small text-secondary');
                if (newStudent.condicion == "Egresado/a"){
                    condicionHeader.innerHTML = ' (Egresadx)';
                }
                else if (newStudent.condicion == "Salido con pase"){
                    condicionHeader.innerHTML = ' (Salidx con pase)';
                }
                else if (newStudent.condicion == "Salido sin pase"){
                    condicionHeader.innerHTML = ' (Salidx sin pase)';
                }
                
                studentHeader.appendChild(condicionHeader);


                /* Change btn */
                editBtn.innerHTML = 'Editar';
                editBtn.setAttribute('class', 'btn btn-secondary float-right');       
            })
        }
    }

    /* ########## Aux Funcs ############ */

    function replace(field){
        /* Replaces <span> with <input>
        and pre-populates them */
        let text;
        if (field.innerHTML == "No cargada aún") {
            text = '';
        }
        else {
            text = field.innerHTML;
        }       
        let fieldId = field.id;
        let editField = document.createElement('input');
        editField.id = fieldId;
        if (editField.id == "name" || editField.id == "last") {
            editField.setAttribute('class', 'edit-input text-capitalize');
        }
        else {
            editField.setAttribute('class', 'edit-input');
        }

        editField.value = text;
        field.parentNode.replaceChild(editField, field);
    }

    function replaceSelect(field){
        /* Replaces <span> with <select>
        and pre-populates them */
        let preChoice = field.innerHTML;
        let options = ["Certificado de 7mo", "Constancia de Alumno Regular", "Analítico Parcial"];
        let selectField = document.createElement('select');
        selectField.id = 'doc_ingreso';
        selectField.setAttribute('class', 'edit-input');
        field.parentNode.replaceChild(selectField, field);
        for (let i = 0; i < options.length; i++){
            let option = document.createElement('option');
            option.value = options[i];
            option.text = options[i];
            selectField.appendChild(option);
        }
        /* Pre-select previews choice */
        if (preChoice === "Certificado de 7mo"){
            selectField.selectedIndex = "0";
        }
        else if (preChoice === "Constancia de Alumno Regular"){
            selectField.selectedIndex = "1";
        }
        else {
            selectField.selectedIndex = "2";
        }
    }

    function replaceLink(field){
        /* Replaces <a> with <input>
        and pre-populates them */
        let text;
        if (field.href == undefined){
            text = ''
        }
        else {
            text = field.href;
        }
        let fieldId = field.id;
        let editField = document.createElement('input');
        editField.setAttribute('class', 'form-control');
        editField.id = fieldId;
        editField.value = text;
        field.parentNode.replaceChild(editField, field);
    }

    function reverseReplace (field, newStudent){
        /* Replaces <input> with <span> */
        let newField;
        if (newStudent[`${field.id}`] === null){
            newField = document.createElement('button');
            newField.id = field.id;
            newField.setAttribute('class', 'btn btn-sm btn-warning');
            newField.setAttribute('disabled','');
            newField.innerHTML = "No cargada aún";
        }
        else {
            newField = document.createElement('span');
            newField.id = field.id;
            newField.innerHTML = newStudent[`${field.id}`];
            if (newField.id == "name" || newField.id == "last"){
                newField.setAttribute('class', 'text-capitalize');
            }
        }
        field.parentNode.replaceChild(newField, field);
    }

    function reverseReplaceLink(field, newStudent) {
        /* Replaces <input> with <link> */
        let newField;
        if (newStudent[`${field.id}`] === null) {
            newField = document.createElement('button');
            newField.id = field.id;
            newField.setAttribute('disabled', '');
            newField.setAttribute('class', 'btn btn-sm btn-warning');
            newField.innerHTML = "No cargado aún";
        }
        else {
            newField = document.createElement('a');
            newField.id = field.id;
            newField.href = newStudent[`${field.id}`];
            newField.setAttribute('class', 'btn btn-sm btn-info');
            newField.target = "_blank";
            newField.innerHTML = "Ver";
        }
        field.parentNode.replaceChild(newField, field);
    }
})