import React, { useState } from "react";
import { useTablero } from "./usePolling.js";
import Flotilla from "./Flotilla.jsx";
import Monitoreo from "./Monitoreo.jsx";
import Indicadores from "./Indicadores.jsx";
import Control from "./control/Control.jsx";
import Logistica from "./logistica/Logistica.jsx";
import { useTarimas } from "./logistica/useTarimas.js";

export default function App() {
  const d = useTablero();
  const [vista, setVista] = useState("flotilla");
  const [asignada, setAsignada] = useState({ ruta: "", id_tarima: "" });
  const { tarimas, refrescar } = useTarimas(d.conectado === true);
  const tabs = [["flotilla", "Flotilla"], ["monitoreo", "Monitoreo"], ["control", "Control"], ["logistica", "Logística"]];
  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="flex items-center justify-between bg-slate-800 px-6 py-3 text-white">
        <h1 className="text-xl font-bold">KOLEO - Tablero</h1>
        <nav className="flex gap-2">
          {tabs.map(([k, t]) => (
            <button key={k} onClick={() => setVista(k)}
              className={"rounded px-3 py-1 " + (vista === k ? "bg-sky-600" : "bg-slate-600")}>{t}</button>
          ))}
        </nav>
      </header>
      {d.conectado === false && (
        <div role="alert" className="bg-red-600 px-6 py-3 text-lg font-bold text-white">
          Sin conexión con el backend. No hay datos actuales que mostrar.
        </div>
      )}
      {d.conectado === null && <p className="p-6">Conectando...</p>}
      {d.conectado && (
        <main className="space-y-6 p-6">
          <Indicadores ind={d.indicadores} />
          {vista === "flotilla" && <Flotilla robots={d.robots} />}
          {vista === "monitoreo" && <Monitoreo robots={d.robots} historial={d.historial} />}
          {vista === "control" && <Control tarimas={tarimas} rutaInicial={asignada.ruta} tarimaInicial={asignada.id_tarima} />}
          {vista === "logistica" && (
            <Logistica tarimas={tarimas} historial={d.historial} alRegistrar={refrescar}
              alAsignarRuta={(id_tarima, ruta) => { setAsignada({ ruta, id_tarima }); setVista("control"); }} />
          )}
        </main>
      )}
    </div>
  );
}
