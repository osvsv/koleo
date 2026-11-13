import { useEffect, useState } from "react";

export const PERIODO_MS = 1000; // SUP-015

async function get(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
  return r.json();
}

// Consulta cada 1 s. Si una consulta falla, se descartan los datos: no se muestran datos viejos.
export function useTablero() {
  const [estado, setEstado] = useState({ conectado: null, robots: [], indicadores: null, historial: [], ordenes: [] });
  useEffect(() => {
    let vivo = true;
    const ciclo = async () => {
      try {
        const [robots, indicadores, historial, ordenes] = await Promise.all([
          get("/api/robots"), get("/api/indicadores"), get("/api/historial"), get("/api/ordenes"),
        ]);
        if (vivo) setEstado({ conectado: true, robots, indicadores, historial, ordenes });
      } catch {
        if (vivo) setEstado({ conectado: false, robots: [], indicadores: null, historial: [], ordenes: [] });
      }
    };
    ciclo();
    const id = setInterval(ciclo, PERIODO_MS);
    return () => { vivo = false; clearInterval(id); };
  }, []);
  return estado;
}
