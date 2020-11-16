document.addEventListener('DOMContentLoaded', function() {
    const condicionBtn = document.querySelector('#condicion');
    const listadosDiv = document.querySelector('#listado');
    const tableHead = document.querySelector('#table-head');
    const hiddenForm = document.querySelector('#hidden-form');

    condicionBtn.onchange = () => {
        listadosDiv.innerHTML = '';
        tableHead.innerHTML = '';
        let condicion = condicionBtn.value;

        condicion_json = {
            "condicion": condicion
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
        
        fetch('listados_process', {
            method: 'POST',
            credentials: 'same-origin',
            headers:{ 
                'accept': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(condicion)
        })
        .then(response => response.json())
        .then (data => {
            let listado = JSON.parse(data);

            let alumno_row;
            let name;
            let last;
            let dni;
            let ingreso;
            let lastPlusName;
            let tableHeader1;
            let tableHeader2;
            let tableHeader3;

            let form;
            let nameInput;
            let lastInput;
            let dniInput;

            /* Create table headers */
            tableHeader1 = document.createElement('th');
            tableHeader2 = document.createElement('th');
            tableHeader3 = document.createElement('th');

            tableHeader1.setAttribute('scope', 'col');
            tableHeader2.setAttribute('scope', 'col');
            tableHeader3.setAttribute('scope', 'col');

            tableHeader1.innerHTML = 'Apellido, Nombre';
            tableHeader2.innerHTML = 'DNI';
            tableHeader3.innerHTML = 'Año de ingreso';

            tableHead.appendChild(tableHeader1);
            tableHead.appendChild(tableHeader2);
            tableHead.appendChild(tableHeader3);

            for (let i = 0; i < listado.length; i++){
                /* Create hidden form */
                form = document.createElement('form');
                form.setAttribute('action', "/search");
                form.setAttribute('method', 'POST');
                form.setAttribute('id', `${listado[i].pk}`);
                
                nameInput = document.createElement('input');
                lastInput = document.createElement('input');
                dniInput = document.createElement('input');

                nameInput.setAttribute('type', 'hidden');
                nameInput.setAttribute('name', 'name');
                nameInput.setAttribute('value', `${listado[i].name}`);

                lastInput.setAttribute('type', 'hidden');
                lastInput.setAttribute('name', 'last');
                lastInput.setAttribute('value', `${listado[i].last}`);

                dniInput.setAttribute('type', 'hidden');
                dniInput.setAttribute('name', 'dni');
                dniInput.setAttribute('value', `${listado[i].dni}`);

                form.appendChild(nameInput);
                form.appendChild(lastInput);
                form.appendChild(dniInput);

                /* csrf token */
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

                /* Create hidden input with csrftoken as value */
                let csrfInput = document.createElement('input');
                csrfInput.type = "hidden";
                csrfInput.name = "csrfmiddlewaretoken";
                csrfInput.value = csrftoken;
                
                form.appendChild(csrfInput);

                hiddenForm.appendChild(form);

                /* Create rows for each student */
                alumno_row = document.createElement('tr');
                

                alumno_row.setAttribute('class', 'effect');
                
                
                name = capitalize(listado[i].name);
                last = capitalize(listado[i].last);
                
                lastPlusName = document.createElement('th');
                dni = document.createElement('td');
                ingreso = document.createElement('td');

                lastPlusName.innerHTML = `${last}, ${name}`;
                dni.innerHTML = listado[i].dni;
                ingreso.innerHTML = listado[i].ingreso;

                alumno_row.appendChild(lastPlusName);
                alumno_row.appendChild(dni);
                alumno_row.appendChild(ingreso);

                
                alumno_row.setAttribute('onclick', `document.getElementById("${listado[i].pk}").submit();`);
                
                listadosDiv.appendChild(alumno_row);

                


                
            }
        })
    }

/* Aux Funcs */

const capitalize = (s) => {
    if (typeof s !== 'string') return ''
    return s.charAt(0).toUpperCase() + s.slice(1)
  }

})

