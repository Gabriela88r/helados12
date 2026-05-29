let carrito = [];
let productosGlobal = [];

// 🔥 CARGAR PRODUCTOS
async function cargarProductos() {

    try {

        const res = await fetch("/api/productos/");
        const data = await res.json();

        productosGlobal = data;

        renderProductos(data);

    } catch (error) {

        console.error("Error cargando productos:", error);

    }
}

// 🎨 RENDER PRODUCTOS
function renderProductos(productos) {

    const contenedor = document.getElementById("productos");

    contenedor.innerHTML = "";

    productos.forEach(p => {

        const card = document.createElement("div");

        card.className = "card";

        card.innerHTML = `
            <img src="${p.img}" alt="${p.nombre}">

            <h3>${p.nombre}</h3>

            <p>₡${p.precio}</p>

            <button class="btn-card">
                Agregar
            </button>
        `;

        card.querySelector("button").addEventListener("click", () => {
            agregarCarrito(p);
        });

        contenedor.appendChild(card);

    });
}

// 🛒 AGREGAR CARRITO
function agregarCarrito(producto) {

    const existe = carrito.find(p => p.id === producto.id);

    if (existe) {

        existe.cantidad += 1;

    } else {

        carrito.push({
            ...producto,
            cantidad: 1
        });

    }

    renderCarrito();
}

// ❌ ELIMINAR
function eliminarProducto(index) {

    carrito.splice(index, 1);

    renderCarrito();
}

// 🔄 RENDER CARRITO
function renderCarrito() {

    const lista = document.getElementById("carrito");
    const totalText = document.getElementById("total");
    const contador = document.getElementById("contador");

    lista.innerHTML = "";

    let total = 0;
    let items = 0;

    carrito.forEach((p, i) => {

        const li = document.createElement("li");

        li.innerHTML = `
            <div>
                <strong>${p.nombre}</strong>
                x${p.cantidad}
            </div>

            <div>
                ₡${p.precio * p.cantidad}

                <button class="btn-eliminar" onclick="eliminarProducto(${i})">
    ✕
</button>
            </div>
        `;

        lista.appendChild(li);

        total += p.precio * p.cantidad;
        items += p.cantidad;

    });

    totalText.textContent = `Total: ₡${total}`;

    contador.textContent = items;
}

// 🧹 VACIAR
document.getElementById("vaciar").addEventListener("click", () => {

    carrito = [];

    renderCarrito();

});

// 🔍 BUSCADOR
document.getElementById("buscar").addEventListener("input", (e) => {

    const texto = e.target.value.toLowerCase();

    const filtrados = productosGlobal.filter(p =>
        p.nombre.toLowerCase().includes(texto)
    );

    renderProductos(filtrados);

});

// 📩 ENVIAR PEDIDO
async function enviarPedido() {

    if (carrito.length === 0) {

        alert("Carrito vacío");

        return;
    }

    const total = carrito.reduce((sum, p) => {
        return sum + (p.precio * p.cantidad);
    }, 0);

    try {

        await fetch("/api/pedidos/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                productos: carrito,
                total,
                fecha: new Date()
            })
        });

        alert("Pedido enviado 🍦");

        carrito = [];

        renderCarrito();

    } catch (error) {

        console.error("Error enviando pedido:", error);

    }
}

// 🔥 BOTÓN PEDIDO
document
    .getElementById("pedido")
    .addEventListener("click", enviarPedido);

// 🚀 INIT
window.onload = cargarProductos;