let recibidos;
let enproceso;
let finalizados;
let pagados
function update (){$.ajax({
    type: "GET",
    contentType: "application/json; charset-utf-8",
    dateType: "json",                     // initialize an AJAX request
    url: '/admin/updateRequest/',                    // set the url of the request
    data: {},
    success: function (data) {   
        this.recibidos = data.recibidos
        this.enproceso = data.enproceso
        this.finalizados = data.finalizados
        this.pagados = data.pagados
        document.getElementById('recibido').innerHTML=''
        document.getElementById('enproceso').innerHTML=''
        document.getElementById('finalizado').innerHTML=''
        document.getElementById('pagado').innerHTML=''
        for (let i of this.recibidos) {
            pedido = document.getElementById('recibido')
            total=0
            output =`<div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Pedido N°${i.id_pedido}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${i.Fecha}</h6>
                <p class="card-text">`
            for(let j of i.Detalle_pedido){
                total+=j.Precio*j.Cantidad
                output+=`<div> ${j.Producto}: $${j.Precio*j.Cantidad} x${j.Cantidad}</div>`
            }
       
       output+=`
       <div>Total: $${total}</div>
       <p class="card-text">
        
        </p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>`
            pedido.innerHTML+=output
        }
        for (let i of this.enproceso) {
            pedido = document.getElementById('enproceso')
            total=0
            output =`<div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Pedido N°${i.id_pedido}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${i.Fecha}</h6>
                <p class="card-text">`
            for(let j of i.Detalle_pedido){
                total+=j.Precio*j.Cantidad
                output+=`<div> ${j.Producto}: $${j.Precio*j.Cantidad} x${j.Cantidad}</div>`
            }
       
       output+=`
       <div>Total: $${total}</div>
       <p class="card-text">
        
        </p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>`
            pedido.innerHTML+=output
        
        }
        for (let i of this.finalizados) {
            pedido = document.getElementById('finalizado')
            total=0
            output =`<div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Pedido N°${i.id_pedido}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${i.Fecha}</h6>
                <p class="card-text">`
            for(let j of i.Detalle_pedido){
                total+=j.Precio*j.Cantidad
                output+=`<div> ${j.Producto}: $${j.Precio*j.Cantidad} x${j.Cantidad}</div>`
            }
       
       output+=`
       <div>Total: $${total}</div>
       <p class="card-text">
        
        </p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>`
            pedido.innerHTML+=output
        
        }
        for (let i of this.pagados) {
            pedido = document.getElementById('pagado')
            total=0
            output =`<div class="card" style="width: 18rem;">
            <div class="card-body">
                <h5 class="card-title">Pedido N°${i.id_pedido}</h5>
                <h6 class="card-subtitle mb-2 text-muted">${i.Fecha}</h6>
                <p class="card-text">`
            for(let j of i.Detalle_pedido){
                total+=j.Precio*j.Cantidad
                output+=`<div> ${j.Producto}: $${j.Precio*j.Cantidad} x${j.Cantidad}</div>`
            }
       
       output+=`
       <div>Total: $${total}</div>
       <p class="card-text">
        
        </p>
        <a href="#" class="btn btn-primary">Go somewhere</a>
    </div>
</div>`
            pedido.innerHTML+=output
        }
    }
})}
django.jQuery(document).ready(function () {
    update()
    setInterval(update(), 20000);
})
