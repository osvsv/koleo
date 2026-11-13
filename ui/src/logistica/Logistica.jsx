import React, { useState } from "react";
import { RUTAS, enviarJson } from "../control/api.js";

export default function Logistica({ tarimas = [], historial = [], alRegistrar, alAsignarRuta }) {
  const [f, setF] = useState({ id_tarima: "", peso_kg: "", descripcion: "" });
  const [msg, setMsg] = useState(null);
  const [rutas, setRutas] = useState({}); // id_tarima -> ruta elegida

  async function registrar(e) {
    e.preventDefault();
    setMsg(null);
    try {
      const r = await enviarJson("/api/tarimas", { ...f, peso_kg: f.peso_kg === "" ? null : Number(f.peso_kg) });
      if (!r.ok) { setMsg({ mal: true, t: r.datos.error || `Error HTTP ${r.status}` }); return; }
      setMsg({ mal: false, t: `Tarima ${f.id_tarima} registrada (EN_PISO).` });
      setF({ id_tarima: "", peso_kg: "", descripcion: "" });
      if (alRegistrar) alRegistrar();
    } catch {
      setMsg({ mal: true, t: "No se pudo contactar al backend." });
    }
  }

  const inp = "w-full rounded border px-2 py-1";
  return (
    <section className="space-y-4">
      <h2 className="text-lg font-bold">Gestión logística</h2>
      <form onSubmit={registrar} className="grid gap-3 rounded bg-white p-4 shadow md:grid-cols-4">
        <label className="text-sm">ID de tarima
          <input className={inp} placeholder="TAR-104" value={f.id_tarima}
            onChange={(e) => setF({ ...f, id_tarima: e.target.value })} /></label>
        <label className="text-sm">Peso declarado (kg)
          <input className={inp} type="number" step="0.01" value={f.peso_kg}
            onChange={(e) => setF({ ...f, peso_kg: e.target.value })} /></label>
        <label className="text-sm">Descripción
          <input className={inp} maxLength={100} value={f.descripcion}
            onChange={(e) => setF({ ...f, descripcion: e.target.value })} /></label>
        <button type="submit" className="self-end rounded bg-sky-600 px-4 py-2 font-bold text-white">Registrar tarima</button>
        {msg && <p role="status" className={"md:col-span-4 " + (msg.mal ? "text-red-700" : "text-green-700")}>{msg.t}</p>}
      </form>

      <div className="rounded bg-white p-4 shadow">
        <h3 className="font-semibold">Tarimas</h3>
        <table className="w-full text-left text-sm">
          <thead><tr><th>ID</th><th>Descripción</th><th>Peso (kg)</th><th>Ubicación</th><th>Estado</th><th>Ruta</th></tr></thead>
          <tbody>
            {tarimas.map((t) => (
              <tr key={t.id_tarima} className="border-t">
                <td className="font-mono">{t.id_tarima}</td>
                <td>{t.descripcion || "—"}</td>
                <td>{t.peso_kg ?? "—"}</td>
                <td>{t.ubicacion_nodo || (t.coord_x_cm != null ? `(${t.coord_x_cm}, ${t.coord_y_cm}) cm` : "—")}</td>
                <td>{t.estado}</td>
                <td>
                  {t.estado === "EN_PISO" && (
                    <span className="flex gap-1">
                      <select aria-label={"Ruta de " + t.id_tarima} className="rounded border px-1"
                        value={rutas[t.id_tarima] || RUTAS[0]}
                        onChange={(e) => setRutas({ ...rutas, [t.id_tarima]: e.target.value })}>
                        {RUTAS.map((r) => <option key={r}>{r}</option>)}
                      </select>
                      <button className="rounded bg-slate-700 px-2 text-white"
                        onClick={() => alAsignarRuta(t.id_tarima, rutas[t.id_tarima] || RUTAS[0])}>Asignar</button>
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {tarimas.length === 0 && <p className="text-sm text-slate-500">No hay tarimas registradas.</p>}
      </div>

      <div className="rounded bg-white p-4 shadow">
        <h3 className="font-semibold">Traslados concluidos</h3>
        {historial.length === 0 && <p className="text-sm text-slate-500">Sin traslados concluidos.</p>}
        <ul className="text-sm">
          {[...historial].reverse().map((h) => (
            <li key={h.id_movimiento} className="border-t py-1">
              {h.id_tarima} — {h.ruta_ejecutada} — peso {h.peso_medido_kg ?? "—"} kg — {h.fecha_hora ?? ""}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
