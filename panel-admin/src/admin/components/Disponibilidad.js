import { useEffect, useState } from "react";
import axios from "axios";

function Disponibilidad({ fecha }) {
  const [disponibilidad, setDisponibilidad] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    axios
      .get(`http://127.0.0.1:8000/disponibilidad?fecha=${fecha}`)
      .then((res) => {
        setDisponibilidad(res.data.disponibilidad);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [fecha]);

  const colores = {
    libre: "#1D9E75",
    ocupado: "#D85A30",
  };

  if (loading) return <p>Cargando...</p>;
  if (!disponibilidad) return <p>Sin datos para esta fecha.</p>;

  return (
    <div>
      <h2>Disponibilidad — {fecha}</h2>
      <div className="turnos">
        {Object.entries(disponibilidad).map(([turno, estado]) => (
          <div
            key={turno}
            className="turno-card"
            style={{ borderLeft: `4px solid ${colores[estado]}` }}
          >
            <span className="turno-nombre">{turno}</span>
            <span
              className="turno-estado"
              style={{ color: colores[estado] }}
            >
              {estado}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Disponibilidad;