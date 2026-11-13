import React from "react";

const CAPACIDAD_KG = 10;

export default function Monitoreo({ robots, historial }) {
  return (
    <section className="space-y-4">
      <h2 className="text-lg font-bold">Monitoreo</h2>
      <div className="grid gap-4 md:grid-cols-2">
        {robots.map((r) => {
          const peso = r.peso_kg ?? 0;
          const pct = Math.min(100, (peso / CAPACIDAD_KG) * 100);
          return (
            <div key={r.robot_id} className="rounded bg-white p-4 shadow">
              <div className="font-mono font-bold">{r.robot_id} ({r.estado})</div>
              <div className="mt-2 text-sm">Peso declarado: {r.peso_kg ?? "—"} kg de {CAPACIDAD_KG} kg</div>
              <div className="h-3 w-full rounded bg-slate-200">
                <div className={"h-3 rounded " + (peso > CAPACIDAD_KG ? "bg-red-600" : "bg-sky-600")} style={{ width: pct + "%" }} />
              </div>
              <div className="mt-2 text-sm">Velocidad: {r.velocidad_cm_s ?? "—"} cm/s</div>
              <div className="text-sm">Ruta: {r.ruta_actual ?? "sin ruta en curso"}</div>
            </div>
          );
        })}
      </div>
      <div className="rounded bg-white p-4 shadow">
        <h3 className="font-semibold">Historial reciente</h3>
        <ul className="text-sm">
          {historial.slice(-10).reverse().map((h) => (
            <li key={h.id_movimiento} className="border-t py-1">{h.id_tarima} — ruta {h.ruta_ejecutada}</li>
          ))}
          {historial.length === 0 && <li className="text-slate-500">Sin movimientos.</li>}
        </ul>
      </div>
    </section>
  );
}
