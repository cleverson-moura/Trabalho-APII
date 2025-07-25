// const btn1 = document.getElementById('btn-ponto');
// const btn2 = document.getElementById('btn-hoteis');

// function mostrar_hoteis() {
//     btn1.classList.remove('ativo');
//     btn1.classList.add('inativo');
//     btn2.classList.remove('inativo');
//     btn2.classList.add('ativo');
// }

// function mostrar_pontos() {
//     btn1.classList.remove('inativo');
//     btn1.classList.add('ativo');
//     btn2.classList.remove('ativo');
//     btn2.classList.add('inativo');
// }

document.addEventListener("DOMContentLoaded", function() {
    const btnAbrirPopup = document.getElementById("btn-abrir-popup");
    const popup = document.getElementById("popup");
    const fecharPopup = document.getElementById("fechar-popup");

    btnAbrirPopup.addEventListener("click", function() {
        popup.classList.add("ativo");
    });

    fecharPopup.addEventListener("click", function() {
        popup.classList.remove("ativo");
    });
});
