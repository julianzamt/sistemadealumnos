document.addEventListener('DOMContentLoaded', function() {
    const condicionSelect = document.querySelector('#id_condicion');
    const egresadoView = document.querySelector('#egresado-view');
    const salidoView = document.querySelector('#salido-view');
    const salidoSinPaseView = document.querySelector('#salido-sin-pase-view');
    const regularView = document.querySelector('#regular-view');


    /* Habilitar Guardar al elegir una nueva condición */
    condicionSelect.onchange = () => {
        if (condicionSelect.value == 'Egresado/a'){
            loadView(egresadoView);
        }
        else if (condicionSelect.value == 'Salido con pase') {
            loadView(salidoView);
        }
        else if (condicionSelect.value == 'Salido sin pase') {
            loadView(salidoSinPaseView);
        }
        else if (condicionSelect.value == 'Regular'){
            loadView(regularView);
        }
    }

    /* Aux Funcs */

    function loadView(view) { 
        
        if (view == egresadoView) {
            egresadoView.style.display = 'block';
            salidoView.style.display = 'none';
            salidoSinPaseView.style.display = 'none';
            regularView.style.display = 'none';
        }
        else if (view == salidoView) {
            egresadoView.style.display = 'none';
            salidoView.style.display = 'block';
            salidoSinPaseView.style.display = 'none';
            regularView.style.display = 'none';
        }
        else if (view == salidoSinPaseView){
            egresadoView.style.display = 'none';
            salidoView.style.display = 'none';
            salidoSinPaseView.style.display = 'block';
            regularView.style.display = 'none';
        }
        else if (view == regularView) {
            egresadoView.style.display = 'none';
            salidoView.style.display = 'none';
            salidoSinPaseView.style.display = 'none';
            regularView.style.display = 'block';
        }
    }
})