import React from "react";

const f = (v, u = "", n = 1) => (v === null || v === undefined ? "—" : `${Number(v).toFixed(n)}${u}`);

export default function Indicadores({ ind }) {
  const pos = ind.posicion_robot;
  const items = [
    ["Ocupación", `${Math.round(ind.ocupacion * 100)} %`],
    ["Posición del robot", pos ? `(${f(pos.x_cm, "", 0)}, ${f(pos.y_cm, "", 0)}) cm` : "—"],
    ["Tiempo de ciclo", f(ind.tiempo_ciclo_s, " s")],
    ["Peso", f(ind.peso_kg, " kg")],
    ["Precisión", f(ind.precision_cm, " cm")],
    ["Alertas", String(ind.alertas.length)],
  ];
  return (
    <section aria-label="Indicadores" className="grid grid-cols-2 gap-4 md:grid-cols-6">
      {items.map(([k, v]) => (
        <div key={k} className="rounded bg-white p-4 shadow" data-indicador={k}>
          <div className="text-xs uppercase text-slate-500">{k}</div>
          <div className="text-2xl font-semibold">{v}</div>
        </div>
      ))}
    </section>
  );
}
