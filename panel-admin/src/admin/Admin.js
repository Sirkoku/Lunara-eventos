import { useState } from "react";
import Calendar from "react-calendar";
import "react-calendar/dist/Calendar.css";

import Disponibilidad from "./components/Disponibilidad";
import Reservas from "./components/Reservas";

import "../App.css";

function Admin() {
  const [fechaSeleccionada, setFechaSeleccionada] = useState(new Date());
  const [vista, setVista] = useState("disponibilidad");

  const fechaFormateada = fechaSeleccionada.toISOString().split("T")[0];

  return (
    <div className="app">
      <header className="header">
        <h1>Panel Admin — Salon de Eventos</h1>

        <nav>
          <button
            className={vista === "disponibilidad" ? "activo" : ""}
            onClick={() => setVista("disponibilidad")}
          >
            Disponibilidad
          </button>

          <button
            className={vista === "reservas" ? "activo" : ""}
            onClick={() => setVista("reservas")}
          >
            Reservas
          </button>
        </nav>
      </header>

      <div className="contenido">
        <div className="sidebar">
          <Calendar
            onChange={setFechaSeleccionada}
            value={fechaSeleccionada}
          />

          <p className="fecha-seleccionada">
            Fecha: <strong>{fechaFormateada}</strong>
          </p>
        </div>

        <div className="main">
          {vista === "disponibilidad" && (
            <Disponibilidad fecha={fechaFormateada} />
          )}

          {vista === "reservas" && <Reservas />}
        </div>
      </div>
    </div>
  );
}

export default Admin;