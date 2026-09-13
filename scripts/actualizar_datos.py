#!/usr/bin/env python3
"""
Regenera data.json a partir de las bases TRABAJOS y SESIONES del
"SIDLL 2026 · Sistema maestro" en Notion.

Requiere la variable de entorno NOTION_TOKEN (integración interna de Notion
con acceso de lectura compartido sobre esas dos bases).

Uso:
    NOTION_TOKEN=secret_xxx python3 scripts/actualizar_datos.py

Nota sobre la API usada: este script consulta por "data source" (API de
Notion 2025-09-03), que es el modelo que usa este workspace para bases
multi-fuente. Si Notion devuelve error 404/400 en la primera ejecución,
lo más probable es que tu integración necesite consultar por database_id
clásico en su lugar (API 2022-06-28) — ver comentario en `query_data_source`.
"""
import json
import os
import sys
import urllib.request
import urllib.error

NOTION_VERSION = "2025-09-03"
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

# IDs de las "data sources" (vistos en Notion como collection://<uuid>)
TRABAJOS_DS_ID = "4a76c18b-460b-472b-bbc2-32c207528b58"
SESIONES_DS_ID = "122f8770-c65c-4d3b-b6a2-39d294d3025d"
PERSONAS_DS_ID = "f641f884-26d8-4f70-8818-57b1e519a766"

DAY_ORDER = {"Miércoles 25": 0, "Jueves 26": 1, "Viernes 27": 2, None: 99}


def notion_request(path, body):
    req = urllib.request.Request(
        f"https://api.notion.com/v1/{path}",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise SystemExit(
            f"Notion API error {e.code} en POST {path}:\n{detail}\n\n"
            "Si el error es 404 o menciona 'data_sources', prueba a cambiar "
            "este script para usar el endpoint clásico "
            "POST /v1/databases/{database_id}/query con Notion-Version "
            "2022-06-28 y el database_id (no el data source id)."
        )


def query_data_source(data_source_id):
    """Pagina todas las filas de una data source de Notion."""
    rows = []
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        # Endpoint API 2025-09-03 (bases multi-fuente):
        page = notion_request(f"data_sources/{data_source_id}/query", body)
        rows.extend(page.get("results", []))
        if not page.get("has_more"):
            break
        cursor = page.get("next_cursor")
    return rows


def extract(prop):
    """Extrae un valor escalar razonable de una propiedad de Notion,
    sea cual sea su tipo (title, rich_text, select, formula, number, date...)."""
    if prop is None:
        return None
    t = prop.get("type")
    if t == "title":
        parts = prop.get("title") or []
        return "".join(p.get("plain_text", "") for p in parts) or None
    if t == "rich_text":
        parts = prop.get("rich_text") or []
        return "".join(p.get("plain_text", "") for p in parts) or None
    if t == "select":
        sel = prop.get("select")
        return sel.get("name") if sel else None
    if t == "status":
        st = prop.get("status")
        return st.get("name") if st else None
    if t == "number":
        return prop.get("number")
    if t == "date":
        d = prop.get("date")
        return d.get("start") if d else None
    if t == "formula":
        f = prop.get("formula") or {}
        return extract({"type": f.get("type"), f.get("type"): f.get(f.get("type"))})
    if t == "rollup":
        r = prop.get("rollup") or {}
        if r.get("type") == "array":
            arr = r.get("array") or []
            return extract(arr[0]) if arr else None
        return extract({"type": r.get("type"), r.get("type"): r.get(r.get("type"))})
    return None


def extract_relation_ids(prop):
    """Devuelve la lista de IDs de página referenciados por una propiedad relation."""
    if prop is None or prop.get("type") != "relation":
        return []
    return [r["id"] for r in (prop.get("relation") or [])]


def prop(page, name):
    return extract((page.get("properties") or {}).get(name))


def build_personas_map():
    """id de página de PERSONAS -> nombre completo."""
    pages = query_data_source(PERSONAS_DS_ID)
    out = {}
    for pg in pages:
        name = prop(pg, "Nombre completo")
        if name:
            out[pg["id"]] = name.split(" (DUPLICADO")[0]
    return out


def join_names(names):
    names = [n for n in names if n]
    if not names:
        return None
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " y " + names[-1]


def build_trabajos(personas_map):
    pages = query_data_source(TRABAJOS_DS_ID)
    out = []
    for pg in pages:
        codigo = prop(pg, "Código")
        if not codigo:
            continue
        estado = prop(pg, "Estado programa")
        if estado == "No aplica":
            continue
        autor_ids = extract_relation_ids((pg.get("properties") or {}).get("Autores"))
        autores = join_names([personas_map.get(pid) for pid in autor_ids])
        item = {
            "codigo": codigo,
            "titulo": prop(pg, "Título"),
            "autor": autores or prop(pg, "Primera autoría"),
            "dia": prop(pg, "Día (real)"),
            "inicio": prop(pg, "Hora intervención"),
            "fin": prop(pg, "Fin intervención"),
            "aula": prop(pg, "Aula (real)"),
            "eje": prop(pg, "Eje / Panel"),
            "tipo": prop(pg, "Tipo"),
            "estado": estado,
            "orden": prop(pg, "Orden en sesión"),
        }
        out.append(item)

    out.sort(key=lambda t: (
        DAY_ORDER.get(t.get("dia"), 99),
        t.get("inicio") or "99:99",
        t.get("aula") or "",
    ))
    return out


def build_sesiones():
    pages = query_data_source(SESIONES_DS_ID)
    out = []
    for pg in pages:
        codigo = prop(pg, "Código")
        if not codigo:
            continue
        out.append({
            "codigo": codigo,
            "sesion": prop(pg, "Sesión"),
            "dia": prop(pg, "Día"),
            "inicio": prop(pg, "Inicio"),
            "fin": prop(pg, "Fin"),
            "aula": prop(pg, "Aula / espacio"),
            "tipo": prop(pg, "Tipo"),
            "eje": prop(pg, "Panel / eje"),
            "estado": prop(pg, "Estado"),
        })
    out.sort(key=lambda s: (
        DAY_ORDER.get(s.get("dia"), 99),
        s.get("inicio") or "99:99",
        s.get("aula") or "",
    ))
    return out


def main():
    if not NOTION_TOKEN:
        sys.exit("Falta la variable de entorno NOTION_TOKEN.")

    import datetime
    personas_map = build_personas_map()
    data = {
        "trabajos": build_trabajos(personas_map),
        "sesiones": build_sesiones(),
        "generado": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)

    print(f"OK: {len(data['trabajos'])} trabajos, {len(data['sesiones'])} sesiones -> {out_path}")


if __name__ == "__main__":
    main()
