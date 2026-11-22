import { useState, useEffect } from "react";
import Admin from "./Admin";
import "./App.css";

const API = (import.meta.env.VITE_API_URL || "http://localhost:8000/api").replace(/\/$/, "");
const IMG = { hero: "/img/hero.png", gato: "/img/gato.png", perro: "/img/perro.png", ave: "/img/ave.png", servicios: "/img/servicios.png" };
const mascotas = [["Gatos", IMG.gato], ["Perros", IMG.perro], ["Aves", IMG.ave]];
// Datos fijos: el backend aún no tiene tabla de doctores
const doctores = [["Dra. Ester Mendez", "Veterinaria"], ["Dr. Martin Juarez", "Cirujano"], ["Dr. Luis Mesa", "Dentista"], ["Dra. Nataly Flores", "Oncóloga"]]
  .map(([n, r], i) => [n, r, `/img/doctor${i + 1}.png`]);
// Horario del backend: lunes a sábado, 09:00 a 21:00 (el servicio debe terminar antes del cierre)
const horas = Array.from({ length: 12 }, (_, i) => `${String(9 + i).padStart(2, "0")}:00`);

const api = (ruta, body, token, metodo) =>
  fetch(API + ruta, {
    method: metodo || (body ? "POST" : "GET"),
    headers: { "Content-Type": "application/json", ...(token && { Authorization: `Bearer ${token}` }) },
    body: body && JSON.stringify(body),
  }).then(async (r) => {
    const d = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(d.mensaje || d.detail || "Ocurrió un error");
    return d;
  });

export default function App() {
  const [servicios, setServicios] = useState([]);
  const [abierto, setAbierto] = useState(0);
  const [sesion, setSesion] = useState(() => JSON.parse(localStorage.getItem("sesion") || "null"));
  const [registro, setRegistro] = useState(false);
  const [f, setF] = useState({ nombreCompleto: "", telefono: "", email: "", password: "", servicioId: "", fecha: "", hora: "", nombreMascota: "", observaciones: "" });
  const [msg, setMsg] = useState("");
  const [citas, setCitas] = useState([]);
  const set = (k, v) => setF({ ...f, [k]: v });

  useEffect(() => { api("/servicios").then(setServicios).catch(() => setMsg("No se pudo conectar con el servidor")); }, []);

  const esAdmin = sesion?.rol === "ADMIN";
  const recargar = () => api("/servicios").then(setServicios).catch(() => {});
  const cargarCitas = () => sesion && !esAdmin && api("/reservas/mis-reservas", null, sesion.token).then(setCitas).catch(() => {});
  useEffect(() => { cargarCitas(); }, [sesion]);
  const cancelar = (id) => api(`/reservas/${id}/cancelar`, null, sesion.token, "PUT").then(cargarCitas).catch((err) => setMsg(err.message));

  const servicio = servicios.find((s) => s.id === +f.servicioId);
  const cabeEn = (h) => !servicio || +h.slice(0, 2) * 60 + servicio.duracionMinutos <= 21 * 60;

  const entrar = (e) => {
    e.preventDefault();
    api(registro ? "/auth/registro" : "/auth/login", f)
      .then((d) => {
        if (registro) return api("/auth/login", f).then(guardar); // tras registrarse, inicia sesión
        guardar(d);
      })
      .catch((err) => setMsg(err.message));
  };
  const guardar = (d) => { localStorage.setItem("sesion", JSON.stringify(d)); setSesion(d); setMsg(""); };
  const salir = () => { localStorage.removeItem("sesion"); setSesion(null); };

  const reservar = (e) => {
    e.preventDefault();
    if (new Date(f.fecha + "T00:00").getDay() === 0) return setMsg("No atendemos los domingos");
    api("/reservas", { servicioId: +f.servicioId, fechaHora: `${f.fecha}T${f.hora}:00`, nombreMascota: f.nombreMascota, observaciones: f.observaciones }, sesion.token)
      .then(() => { setMsg("¡Cita confirmada!"); cargarCitas(); setF({ ...f, hora: "", nombreMascota: "", observaciones: "" }); })
      .catch((err) => setMsg(err.message));
  };

  return (
    <>
      <nav className="nav">
        <b>🐾 Huellitas</b>
        <div className="links">
          {["Servicios", "Doctores", "Citas"].map((l) => <a key={l} href={`#${l.toLowerCase()}`}>{l}</a>)}
        </div>
        {sesion ? <button className="btn" onClick={salir}>Salir</button> : <a href="#citas" className="btn">Reservar</a>}
      </nav>

      <header className="hero">
        <div>
          <h1>Mascotas sanas, corazones felices</h1>
          <p>Una clínica veterinaria moderna que ayuda a tus mascotas a superar cualquier problema de salud.</p>
          <a href="#citas" className="btn">Reservar cita</a>
        </div>
        <img src={IMG.hero} alt="Mascota feliz" />
      </header>

      <section>
        <h2>¿Cuál es tu mascota?</h2>
        <div className="grid">
          {mascotas.map(([n, img]) => (
            <a href="#citas" className="card" key={n}><img src={img} alt={n} /><h3>{n}</h3></a>
          ))}
        </div>
      </section>

      <section id="servicios" className="claro">
        <h2>Nuestros servicios</h2>
        <div className="dos">
        <div className="lista">
          {servicios.map((s, i) => (
            <div key={s.id} className={`item ${abierto === i ? "abierto" : ""}`} onClick={() => setAbierto(abierto === i ? -1 : i)}>
              <h3>{s.nombre} <span>{abierto === i ? "−" : "+"}</span></h3>
              <div className="det"><div><p>{s.descripcion} <br /><small>S/ {s.precio.toFixed(2)} · {s.duracionMinutos} min</small></p></div></div>
            </div>
          ))}
        </div>
        <img src={IMG.servicios} alt="Nuestros servicios" />
        </div>
      </section>

      <section id="doctores">
        <h2>Nuestros especialistas</h2>
        <div className="grid g4">
          {doctores.map(([n, r, img]) => (
            <div className="card" key={img}><img src={img} alt={n} /><h3>{n}</h3><small>{r}</small></div>
          ))}
        </div>
      </section>

      <section id="citas" className="claro">
        {!sesion ? (
          <form className="form" onSubmit={entrar}>
            <h2>{registro ? "Crea tu cuenta" : "Inicia sesión para reservar"}</h2>
            {registro && (
              <div className="fila">
                <input required placeholder="Nombre completo" value={f.nombreCompleto} onChange={(e) => set("nombreCompleto", e.target.value)} />
                <input type="tel" placeholder="Teléfono" value={f.telefono} onChange={(e) => set("telefono", e.target.value)} />
              </div>
            )}
            <input required type="email" placeholder="Correo" value={f.email} onChange={(e) => set("email", e.target.value)} />
            <input required type="password" placeholder="Contraseña" value={f.password} onChange={(e) => set("password", e.target.value)} />
            <button className="btn">{registro ? "Registrarme" : "Entrar"}</button>
            <small className="msg">{msg}</small>
            <a href="#citas" className="cambio" onClick={() => { setRegistro(!registro); setMsg(""); }}>
              {registro ? "¿Ya tienes cuenta? Inicia sesión" : "¿No tienes cuenta? Regístrate"}
            </a>
          </form>
        ) : esAdmin ? (
          <Admin api={(ruta, body, metodo) => api(ruta, body, sesion.token, metodo)} servicios={servicios} recargar={recargar} />
        ) : (
          <form className="form" onSubmit={reservar}>
            <h2>Agenda una cita</h2>
            <select required value={f.servicioId} onChange={(e) => setF({ ...f, servicioId: e.target.value, hora: "" })}>
              <option value="">Elige un servicio</option>
              {servicios.map((s) => <option key={s.id} value={s.id}>{s.nombre}</option>)}
            </select>
            <input required type="date" min={new Date().toISOString().slice(0, 10)} value={f.fecha} onChange={(e) => set("fecha", e.target.value)} />
            <div className="chips">
              {horas.map((h) => (
                <button type="button" key={h} disabled={!cabeEn(h)} className={f.hora === h ? "on" : ""} onClick={() => set("hora", h)}>{h}</button>
              ))}
            </div>
            <input required placeholder="Nombre de tu mascota" value={f.nombreMascota} onChange={(e) => set("nombreMascota", e.target.value)} />
            <input placeholder="Observaciones (opcional)" maxLength={500} value={f.observaciones} onChange={(e) => set("observaciones", e.target.value)} />
            <button className="btn" disabled={!f.hora}>Confirmar cita</button>
            <small className="msg">{msg}</small>
          </form>
        )}

        {sesion && !esAdmin && citas.length > 0 && (
          <div className="lista mis">
            <h2>Mis citas</h2>
            {citas.map((c) => (
              <div className="item" key={c.id}>
                <h3>{c.servicioNombre} · {c.nombreMascota}</h3>
                <p>
                  {new Date(c.fechaHora).toLocaleString("es-PE", { dateStyle: "medium", timeStyle: "short" })} · {c.estado}
                  {c.estado === "CONFIRMADA" && <button className="btn" onClick={() => cancelar(c.id)}>Cancelar</button>}
                </p>
              </div>
            ))}
          </div>
        )}
      </section>

      <footer>© 2026 Huellitas · Clínica veterinaria</footer>
    </>
  );
}
