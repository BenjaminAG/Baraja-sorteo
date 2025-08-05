let cartaSeleccionada = null;

function cargarCartas() {
  fetch('/cartas')
    .then(res => res.json())
    .then(data => {
      const contenedor = document.getElementById('baraja');
      contenedor.innerHTML = '';
      data.forEach(carta => {
        const div = document.createElement('div');
        div.className = 'carta';
        if (carta.vendida) {
          div.classList.add('vendida');
          div.innerHTML = `<span>🂠</span><small>${carta.nombre}</small>`;
        } else {
          div.innerHTML = `<strong>${carta.numero}</strong><br>${carta.palo}`;
          div.onclick = () => mostrarFormulario(carta);
        }
        contenedor.appendChild(div);
      });
    });
}

function seleccionarAlAzar() {
  fetch('/seleccionar_azar', { method: 'POST' })
    .then(res => res.json())
    .then(data => mostrarFormulario(data));
}

function seleccionarManual() {
  const id = document.getElementById('idCartaManual').value;
  fetch('/seleccionar_manual', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) alert(data.error);
      else mostrarFormulario(data);
    });
}

function mostrarFormulario(carta) {
  cartaSeleccionada = carta;
  document.getElementById('cartaSeleccionada').textContent =
    `Carta: ${carta.numero} de ${carta.palo}`;
  document.getElementById('formularioGanador').style.display = 'block';
}

function guardarGanador() {
  const nombre = document.getElementById('nombre').value;
  const telefono = document.getElementById('telefono').value;

  fetch('/vender_carta', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      id: cartaSeleccionada.id,
      nombre,
      telefono
    })
  })
    .then(res => res.json())
    .then(() => {
      cargarCartas();
      document.getElementById('formularioGanador').style.display = 'none';
    });
}

window.onload = cargarCartas;
