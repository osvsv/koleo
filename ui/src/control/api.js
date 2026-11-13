export const RUTAS = ["RUTA_1", "RUTA_2", "RUTA_3"];

export async function enviarJson(url, cuerpo) {
  const r = await fetch(url, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(cuerpo),
  });
  let datos = {};
  try { datos = await r.json(); } catch { /* sin cuerpo */ }
  return { ok: r.ok, status: r.status, datos };
}

export async function obtenerJson(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
  return r.json();
}
