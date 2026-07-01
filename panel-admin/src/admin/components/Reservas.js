import { useEffect, useState } from "react";
import axios from "axios";

function Reservas() {
const [reservas, setReservas] = useState([]);
const [loading, setLoading] = useState(false);
const [formulario, setFormulario] = useState(false);
const [nuevaReserva, setNuevaReserva] = useState({
    fecha: "",
    turno: "manana",
    nombre_cliente: "",
    telefono: "",
    email: "",
});
const [mensaje, setMensaje] = useState("");

const cargarReservas = () => {
    setLoading(true);
    axios
    .get("http://127.0.0.1:8000/reservas")
    .then((res) => {
        setReservas(res.data.reservas);
        setLoading(false);
    })
    .catch((err) => {
        console.error(err);
        setLoading(false);
    });
};

useEffect(() => {
    cargarReservas();
}, []);

const coloresEstado = {
    pendiente_sena: "#BA7517",
    senado: "#185FA5",
    pagado: "#1D9E75",
};

const confirmarSena = (id) => {
    axios
    .post("http://127.0.0.1:8000/confirmar_sena", { id })
    .then(() => cargarReservas())
    .catch((err) => console.error(err));
};

const confirmarPago = (id) => {
    axios
    .post("http://127.0.0.1:8000/confirmar_pago", { id })
    .then(() => cargarReservas())
    .catch((err) => console.error(err));
};

const cancelarReserva = (id) => {
    if (window.confirm("¿Seguro que querés cancelar esta reserva?")) {
    axios
        .delete(`http://127.0.0.1:8000/cancelar_reserva/${id}`)
        .then(() => cargarReservas())
        .catch((err) => console.error(err));
    }
};

const crearReserva = () => {
    axios
    .post("http://127.0.0.1:8000/reservar", nuevaReserva)
    .then((res) => {
        if (res.data.error) {
        setMensaje(`Error: ${res.data.error}`);
        } else {
        setMensaje("Reserva creada con exito");
        setFormulario(false);
        setNuevaReserva({
            fecha: "",
            turno: "manana",
            nombre_cliente: "",
            telefono: "",
            email: "",
        });
        cargarReservas();
        }
    })
    .catch((err) => {
        setMensaje("Error al crear la reserva");
        console.error(err);
    });
};
const soloNumeros = (e) => {
const valor = e.target.value.replace(/[^0-9]/g, "");
setNuevaReserva({ ...nuevaReserva, telefono: valor });
};

const soloLetras = (e) => {
const valor = e.target.value.replace(/[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]/g, "");
setNuevaReserva({ ...nuevaReserva, nombre_cliente: valor });
};

if (loading) return <p>Cargando...</p>;

return (
    <div>
    <h2>Reservas</h2>

    {mensaje && (
        <p style={{ marginBottom: "1rem", color: mensaje.includes("Error") ? "#D85A30" : "#1D9E75" }}>
        {mensaje}
        </p>
    )}

    <button
        className="btn-nueva-reserva"
        onClick={() => {
        setFormulario(!formulario);
        setMensaje("");
        }}
    >
        {formulario ? "Cancelar" : "+ Nueva reserva"}
    </button>

    {formulario && (
        <div className="formulario">
        <input
            placeholder="Fecha (YYYY-MM-DD)"
            value={nuevaReserva.fecha}
            onChange={(e) => setNuevaReserva({ ...nuevaReserva, fecha: e.target.value })}
        />
        <select
            value={nuevaReserva.turno}
            onChange={(e) => setNuevaReserva({ ...nuevaReserva, turno: e.target.value })}
        >
            <option value="manana">Mañana</option>
            <option value="mediodia">Mediodía</option>
            <option value="tarde">Tarde</option>
        </select>
        <input
            placeholder="Nombre cliente"
            value={nuevaReserva.nombre_cliente}
            onChange= {soloLetras }
        />
        <input
            placeholder="Telefono"
            value={nuevaReserva.telefono}
            onChange={soloNumeros}
        />
        <input
            placeholder="Email (opcional)"
            value={nuevaReserva.email}
            onChange={(e) => setNuevaReserva({ ...nuevaReserva, email: e.target.value })}
        />
        <button onClick={crearReserva}>Crear reserva</button>
        </div>
    )}

    {reservas.length === 0 && <p>No hay reservas cargadas.</p>}
    <div className="reservas-lista">
        {reservas.map((r) => (
        <div key={r.id} className="reserva-card">
            <div className="reserva-info">
            <span className="reserva-fecha">{r.fecha} — {r.turno}</span>
            <span
                className="reserva-estado"
                style={{ color: coloresEstado[r.estado] }}
            >
                {r.estado}
            </span>
            </div>
            {r.cliente && (
            <div className="reserva-cliente">
                <span>{r.cliente.nombre}</span>
                <span>{r.cliente.telefono}</span>
                {r.cliente.email && <span>{r.cliente.email}</span>}
            </div>
            )}
            <div className="reserva-acciones">
            {r.estado === "pendiente_sena" && (
                <button onClick={() => confirmarSena(r.id)}>
                Confirmar seña
                </button>
            )}
            {r.estado === "senado" && (
                <button onClick={() => confirmarPago(r.id)}>
                Confirmar pago
                </button>
            )}
            <button
                className="btn-cancelar"
                onClick={() => cancelarReserva(r.id)}
            >
                Cancelar
            </button>
            </div>
        </div>
        ))}
    </div>
    </div>
);
}

export default Reservas;