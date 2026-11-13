import { useCallback, useEffect, useState } from "react";
import { obtenerJson } from "../control/api.js";

// Consulta /api/tarimas cada 1 s; si falla, descarta la lista (no muestra datos viejos).
export function useTarimas(activo) {
  const [tarimas, setTarimas] = useState([]);
  const [n, setN] = useState(0);
  const refrescar = useCallback(() => setN((x) => x + 1), []);
  useEffect(() => {
    if (!activo) return undefined;
    let vivo = true;
    const ciclo = async () => {
      try {
        const t = await obtenerJson("/api/tarimas");
        if (vivo) setTarimas(t);
      } catch {
        if (vivo) setTarimas([]);
      }
    };
    ciclo();
    const id = setInterval(ciclo, 1000);
    return () => { vivo = false; clearInterval(id); };
  }, [activo, n]);
  return { tarimas, refrescar };
}
