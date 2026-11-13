import React, { useEffect, useState } from "react";
import { RUTAS, enviarJson, obtenerJson } from "./api.js";

const COLOR = { pendiente: "bg-amber-500", aceptada: "bg-green-600", rechazada: "bg-red-600" };

export default function Control({ tarimas = [], rutaInicial = "", tarimaInicial = "" }) {
  const [ruta, setRuta] = useState(rutaInicial || RUTAS[0]);
  const [idTarima, setIdTarima] = useState(tarimaInicial);
  const [ordenes, setOrdenes] = useState([]); // {id_orden, tipo, estado, motivo}
  const [error, setError] = useState(null);

  useEffect(() => { if (rutaInicial) setRuta(rutaInicial); }, [rutaInicial]);
  useEffect(() => { if (tarimaInicial) setIdTarima(tarimaInicial); }, [tarimaInicial]);

  // Refleja el ack: consulta cada segundo las ordenes aun pendientes.
  useEffect(() => {
    const pendientes = ordenes.filter((o) => o.estado === "pendiente");
    if (pendientes.length === 0) return undefined;
    const id = setInterval(async () => {
      for (const o of pendientes) {
        try {
          const act = await obtenerJson(`/api/ordenes/${o.id_orden}`);
          if (act.estado !== "pendiente") {
            setOrdenes((lista) => lista.map((x) => (x.id_orden === o.id_orden
              ? { ...x, estado: act.estado, motivo: act.motivo } : x)));
          }
        } catch { /* se reintenta en el siguiente ciclo */ }
      }
    }, 1000);
    return () => clearInterval(id);
  }, [ordenes]);

  async function enviar(tipo) {
    setError(null);
    const cuerpo = { tipo };
    if (tipo === "INICIAR") { cuerpo.ruta = ruta; if (idTarima) cuerpo.id_tarima = idTarima; }
    try {
      const r = await enviarJson("/api/ordenes", cuerpo);
      if (!r.ok) { setError(r.datos.error || `Error HTTP ${r.status}`); return; }
      setOrdenes((l) => [{ id_orden: r.datos.id_orden, tipo, estado: "pendiente" }, ...l].slice(0, 8));
    } catch {
      setError("No se pudo contactar al backend.");
    }
  }

  const sel = "rounded border px-2 py-1";
  return (
    <section className="space-y-4">
      <h2 className="text-lg font-bold">Control</h2>
      <div className="flex flex-wrap items-end gap-4 rounded bg-white p-4 shadow">
        <label className="text-sm">Ruta<br />
          <select aria-label="Ruta" className={sel} value={ruta} onChange={(e) => setRuta(e.target.value)}>
            {RUTAS.map((r) => <option key={r}>{r}</option>)}
          </select>
        </label>
        <label className="text-sm">Tarima<br />
          <select aria-label="Tarima" className={sel} value={idTarima} onChange={(e) => setIdTarima(e.target.value)}>
            <option value="">— elegir —</option>
            {tarimas.map((t) => <option key={t.id_tarima} value={t.id_tarima}>{t.id_tarima} ({t.estado})</option>)}
          </select>
        </label>
        <button onClick={() => enviar("INICIAR")} className="rounded bg-green-600 px-4 py-2 font-bold text-white">INICIAR</button>
        <button onClick={() => enviar("CANCELAR")} className="rounded bg-amber-600 px-4 py-2 font-bold text-white">CANCELAR</button>
        <button onClick={() => enviar("PARO")} className="rounded bg-red-700 px-6 py-2 font-bold text-white">PARO</button>
      </div>
      {error && <div role="alert" className="rounded bg-red-100 p-3 text-red-800">{error}</div>}
      <div className="rounded bg-white p-4 shadow">
        <h3 className="font-semibold">Órdenes enviadas</h3>
        {ordenes.length === 0 && <p className="text-sm text-slate-500">Sin órdenes en esta sesión.</p>}
        <ul className="text-sm">
          {ordenes.map((o) => (
            <li key={o.id_orden} className="flex items-center gap-2 border-t py-1">
              <span className="font-mono">{o.id_orden}</span><span>{o.tipo}</span>
              <span className={"rounded px-2 text-white " + (COLOR[o.estado] || "bg-slate-500")}>{o.estado}</span>
              {o.motivo && <span className="text-slate-600">{o.motivo}</span>}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
