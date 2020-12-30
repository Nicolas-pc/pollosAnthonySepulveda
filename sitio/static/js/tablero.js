let pedidos;
let target=undefined;
function update() {
    $.ajax({
        type: "GET",
        contentType: "application/json; charset-utf-8",
        dateType: "json",                     // initialize an AJAX request
        url: '/admin/updateRequest/',                    // set the url of the request
        data: {},
        success: function (data) {
            this.pedidos = data;
            for (let k in this.pedidos) {
                pedido = document.getElementById(k);
                pedido.innerHTML = '';
                for (let i of this.pedidos[k]) {
                    total = 0;
                    hora = new Date(i.Fecha).getHours()
                    hora = ("0" + hora).slice(-2);
                    minutos = new Date(i.Fecha).getMinutes()
                    minutos = ("0" + minutos).slice(-2);
                    output = `<div class="card" id="${i.id_pedido}" style="width: 18rem;">
                    <div class="n_pedido">N:${i.id_pedido}</div>
                    <div class="hora">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" class="bi bi-clock" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M8 15A7 7 0 1 0 8 1a7 7 0 0 0 0 14zm8-7A8 8 0 1 1 0 8a8 8 0 0 1 16 0z"/>
  <path fill-rule="evenodd" d="M7.5 3a.5.5 0 0 1 .5.5v5.21l3.248 1.856a.5.5 0 0 1-.496.868l-3.5-2A.5.5 0 0 1 7 9V3.5a.5.5 0 0 1 .5-.5z"/>
</svg>
                    ${hora}:${minutos}</div>
            <div class="card-body">
                <h5 class="card-title">${i.Cliente}</h5>
                <h6 class="card-subtitle mb-2 text-muted"><div>
                <svg class="phone"xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-telephone-fill" viewBox="0 0 16 16">
                        <path fill-rule="evenodd" d="M2.267.98a1.636 1.636 0 0 1 2.448.152l1.681 2.162c.309.396.418.913.296 1.4l-.513 2.053a.636.636 0 0 0 .167.604L8.65 9.654a.636.636 0 0 0 .604.167l2.052-.513a1.636 1.636 0 0 1 1.401.296l2.162 1.681c.777.604.849 1.753.153 2.448l-.97.97c-.693.693-1.73.998-2.697.658a17.47 17.47 0 0 1-6.571-4.144A17.47 17.47 0 0 1 .639 4.646c-.34-.967-.035-2.004.658-2.698l.97-.969z"/>
                    </svg>
                    ${i.Telefono}
                </div>
                <div>
                <svg class="address"xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" class="bi bi-house-door-fill" viewBox="0 0 16 16">
  <path d="M6.5 10.995V14.5a.5.5 0 0 1-.5.5H2a.5.5 0 0 1-.5-.5v-7a.5.5 0 0 1 .146-.354l6-6a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 .146.354v7a.5.5 0 0 1-.5.5h-4a.5.5 0 0 1-.5-.5V11c0-.25-.25-.5-.5-.5H7c-.25 0-.5.25-.5.495z"/>
  <path fill-rule="evenodd" d="M13 2.5V6l-2-2V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5z"/>
</svg>
${i.Direccion}</div>
                </h6>
                <div class="card-text">`
                    for (let j of i.Detalle_pedido) {
                        total += j.Precio * j.Cantidad;
                        output += `<div> ${j.Producto}: $${j.Precio} x${j.Cantidad}</div>`
                    }
                    output += `<div class="total">Total: $${total}</div></div>`
                    if (k !== 'pagados') {
                        output += `<a class="btn submit" onclick="openModal(${i.id_pedido})">
                            <svg class="icon-submit"xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-arrow-right-circle-fill" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-11.5.5a.5.5 0 0 1 0-1h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5z" />
                            </svg>
                        </a>`}
                    output += `</div></div>`;
                    pedido.innerHTML += output;
                }
            }
        }
    })
}
django.jQuery(document).ready(function () {
    new bootstrap.Modal(document.getElementById('myModal'), {
        keyboard: false
    })
    update();
    setInterval(update(), 20000);
})

function closeModal() {
    $("#myModal").modal('hide');
    this.target=undefined;
}
function openModal(id_pedido){
    $("#myModal").modal('show');
    this.target=id_pedido;
    console.log(this.target)
}
function changeState() {
    req=this.target;
    $.ajax({
        contentType: "application/json; charset-utf-8",
        dateType: "json",                     // initialize an AJAX request
        url: '/admin/changeState/',                    // set the url of the request
        data: { req },
        success: function (data) {
            update()
            closeModal();
        }
    })
    

}