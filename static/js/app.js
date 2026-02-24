const form = document.getElementById("formCliente");
const lista = document.getElementById("lista");

async function cargarClientes() {
  const res = await fetch("/clientes");
  const clientes = await res.json();

  lista.innerHTML = "";

  clientes.forEach(c => {
    const li = document.createElement("li");
    li.textContent = `${c.nombre} - ${c.email}`;
    lista.appendChild(li);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  await fetch("/clientes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      nombre: document.getElementById("nombre").value,
      email: document.getElementById("email").value
    })
  });

  cargarClientes();
});

cargarClientes();