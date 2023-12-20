const divEditarPerfil = document.querySelector('.div-editar-perfil');

divEditarPerfil.style.display = 'none';

function abrirAdminProfile() {
    if (divEditarPerfil.style.display === 'none' || divEditarPerfil.style.display === '') {
        divEditarPerfil.style.display = 'block'; // Mostrar el div al hacer clic
    } else {
        divEditarPerfil.style.display = 'none'; // Ocultar el div si ya está visible
    }
}

function ocultarAdminProfile() {
    if (divEditarPerfil.style.display === 'none' || divEditarPerfil.style.display === '') {
        divEditarPerfil.style.display = 'block'; // Mostrar el div al hacer clic
    } else {
        divEditarPerfil.style.display = 'none'; // Ocultar el div si ya está visible
    }
}