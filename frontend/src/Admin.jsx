import { useState, useEffect } from "react";

const vacio = { nombre: "", descripcion: "", precio: "", duracionMinutos: "" };
const fecha = (f) => new Date(f).toLocaleString("es-PE", { dateStyle: "medium", timeStyle: "short" });

// api(ruta, body, metodo) ya viene con el token del administrador
export default function Admin({ api, servicios, recargar }) {
  const [f, setF] = useState(vacio);
  const [editId, setEditId] = useState(null);
  const [reservas, setReservas] = useState([]);
  const [estado, setEstado] = useState("");
  const [msg, setMsg] = useState("");
  const set = (k, v) => setF({ ...f, [k]: v });
  const error = (e) => setMsg(e.message);

  const cargar = () => api("/admin/reservas" + (estado ? `?estado=${estado}` : "")).then(setReservas).catch(error);
  useEffect(() => { cargar(); }, [estado]);

  const guardar = (e) => {
    e.preventDefault();
    const body = { ...f, precio: +f.precio, duracionMinutos: +f.duracionMinutos };
    api(editId ? `/servicios/${editId}` : "/servicios", body, editId ? "PUT" : "POST")
      .then(() => { setF(vacio); setEditId(null); setMsg(""); recargar(); })
      .catch(error);
  };
  const editar = (s) => { setEditId(s.id); setF({ nombre: s.nombre, descripcion: s.descripcion || "", precio: s.precio, duracionMinutos: s.duracionMinutos }); };
  const desactivar = (id) => confirm("¿Desactivar este servicio?") && api(`/servicios/${id}`, null, "DELETE").then(recargar).catch(error);
  const atender = (id) => api(`/admin/reservas/${id}/atendida`, null, "PUT").then(cargar).catch(error);

  return (
    <div className="admin">
      <div className="fila-admin">
        <div className="panel-lista">
          <div className="scroll lista mis">
            <h2>Servicios activos</h2>
            {servicios.map((s) => (
              <div className="item" key={s.id}>
                <h3>{s.nombre} <small>S/ {s.precio.toFixed(2)} · {s.duracionMinutos} min</small></h3>
                <p><button className="btn" onClick={() => editar(s)}>Editar</button><button className="btn" onClick={() => desactivar(s.id)}>Desactivar</button></p>
              </div>
            ))}
          </div>
        </div>

        <form className="form" onSubmit={guardar}>
          <h2>{editId ? "Editar servicio" : "Nuevo servicio"}</h2>
          <input required placeholder="Nombre" value={f.nombre} onChange={(e) => set("nombre", e.target.value)} />
          <input placeholder="Descripción" value={f.descripcion} onChange={(e) => set("descripcion", e.target.value)} />
          <div className="fila">
            <input required type="number" min="0" step="0.01" placeholder="Precio (S/)" value={f.precio} onChange={(e) => set("precio", e.target.value)} />
            <input required type="number" min="1" placeholder="Duración (min)" value={f.duracionMinutos} onChange={(e) => set("duracionMinutos", e.target.value)} />
          </div>
          <button className="btn">{editId ? "Guardar cambios" : "Agregar servicio"}</button>
          {editId && <a href="#citas" className="cambio" onClick={() => { setEditId(null); setF(vacio); }}>Cancelar edición</a>}
          <small className="msg">{msg}</small>
        </form>
      </div>

      <div className="lista mis">
        <h2>Reservas</h2>
        <select value={estado} onChange={(e) => setEstado(e.target.value)}>
          <option value="">Todas</option>
          {["CONFIRMADA", "ATENDIDA", "CANCELADA"].map((x) => <option key={x}>{x}</option>)}
        </select>
        {reservas.map((r) => (
          <div className="item" key={r.id}>
            <h3>{r.servicioNombre} · {r.nombreMascota}</h3>
            <p>
              {r.clienteNombre} · {fecha(r.fechaHora)} · {r.estado}
              {r.estado === "CONFIRMADA" && <button className="btn" onClick={() => atender(r.id)}>Marcar atendida</button>}
            </p>
          </div>
        ))}
        {!reservas.length && <p>No hay reservas.</p>}
      </div>
    </div>
  );
}
