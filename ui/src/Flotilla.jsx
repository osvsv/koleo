import React from "react";

export default function Flotilla({ robots, alertas }) {
  return (
    <section>
      <h2 className="mb-2 text-lg font-bold">Flotilla</h2>
      <table className="w-full rounded bg-white shadow">
        <thead className="text-left text-sm text-slate-500">
          <tr><th className="p-2">Robot</th><th>Conexión</th><th>Estado</th><th>Alertas</th></tr>
        </thead>
        <tbody>
          {robots.map((r) => (
            <tr key={r.robot_id} className="border-t">
              <td className="p-2 font-mono">{r.robot_id}</td>
              <td className={r.conexion === "EN_LINEA" ? "font-semibold text-green-700" : "font-semibold text-red-700"}>{r.conexion}</td>
              <td>{r.estado}</td>
              <td>
                {r.distancia_obstaculo_cm !== null && r.distancia_obstaculo_cm < 20 && (
                  <div>Obstáculo a {r.distancia_obstaculo_cm} cm</div>
                )}
                {alertas.length === 0 ? "Sin alertas" : alertas.map((a) => (
                  <div key={a.fecha_hora + a.id_tarima} className="text-red-700">
                    {a.id_tarima}: {a.motivo} ({a.peso_detectado_kg} kg)
                  </div>
                ))}
              </td>
            </tr>
          ))}
          {robots.length === 0 && <tr><td colSpan="4" className="p-4 text-slate-500">Sin robots registrados.</td></tr>}
        </tbody>
      </table>
    </section>
  );
}
