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
import html
import json
import os
import re
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

# Nombres de país que aparecen, de forma inconsistente, entre paréntesis
# dentro del valor real de "Institución" en Notion (p. ej. "Universidad de
# Málaga (España)" junto a "Universidad de Zaragoza" sin nada parecido; o,
# en casos más enrevesados, en medio de la cadena: "Universitat de
# València (España) | Universidad de Valencia"). Lista CERRADA verificada
# contra los 301 valores reales (2026-09-13, mismo criterio que
# SIDLL_GENERADOR/src/sidll/models/person.py): NO es un strip genérico de
# paréntesis, porque eso borraría paréntesis con información real que
# también aparecen ahí, como "(adscrito a UPSA)" o nombres de ciudad
# ("(Cuenca)", "(Riba-roja de Túria)").
SUFIJOS_PAIS = {
    "Alemania", "Argelia", "Brasil", "Brasil/ Chile", "Chile", "Colombia",
    "Ecuador", "España", "Espanya", "México", "Portugal", "Spain",
}
PARENTESIS_PAIS_RE = re.compile(
    r"\s*\((?:" + "|".join(re.escape(p) for p in SUFIJOS_PAIS) + r")\)"
)


def quitar_sufijo_pais(institucion):
    limpio = PARENTESIS_PAIS_RE.sub("", institucion)
    return re.sub(r"\s{2,}", " ", limpio).strip()


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
    """id de página de PERSONAS -> "Nombre completo (Institución)".

    Si la persona no tiene "Institución" rellena en Notion (6 de 301,
    comprobado 2026-09-13), se usa solo el nombre, sin paréntesis vacíos.
    """
    pages = query_data_source(PERSONAS_DS_ID)
    out = {}
    for pg in pages:
        name = prop(pg, "Nombre completo")
        if not name:
            continue
        name = name.split(" (DUPLICADO")[0]
        institucion = prop(pg, "Institución")
        institucion = quitar_sufijo_pais(institucion) if institucion else institucion
        out[pg["id"]] = f"{name} ({institucion})" if institucion else name
    return out


def join_names(names):
    names = [n for n in names if n]
    if not names:
        return None
    return " · ".join(names)


def titulo_con_cursiva_html(titulo, cursiva_bruto):
    """HTML del título con los fragmentos de "Cursiva" (uno por línea,
    subcadenas EXACTAS de titulo) envueltos en <i>. None si no hay
    fragmentos -- en ese caso el JS usa el título plano tal cual, sin
    tocar el flujo existente. Mismo criterio que
    SIDLL_GENERADOR/src/sidll/renderers/program_renderer.py::_titulo_con_cursiva:
    un fragmento que no aparece literalmente en el título se ignora en
    vez de romper nada.
    """
    fragmentos = [linea.strip() for linea in (cursiva_bruto or "").splitlines() if linea.strip()]
    if not fragmentos or not titulo:
        return None
    posiciones = []
    for frag in fragmentos:
        i = titulo.find(frag)
        if i != -1:
            posiciones.append((i, i + len(frag)))
    if not posiciones:
        return None
    posiciones.sort()
    partes = []
    cursor = 0
    for inicio, fin in posiciones:
        if inicio < cursor:
            continue
        if inicio > cursor:
            partes.append(html.escape(titulo[cursor:inicio]))
        partes.append("<i>" + html.escape(titulo[inicio:fin]) + "</i>")
        cursor = fin
    if cursor < len(titulo):
        partes.append(html.escape(titulo[cursor:]))
    return "".join(partes)


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
        titulo = prop(pg, "Título")
        item = {
            "codigo": codigo,
            "titulo": titulo,
            "tituloHtml": titulo_con_cursiva_html(titulo, prop(pg, "Cursiva")),
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


def build_sesiones(personas_map):
    pages = query_data_source(SESIONES_DS_ID)
    out = []
    for pg in pages:
        codigo = prop(pg, "Código")
        if not codigo:
            continue
        moderacion_ids = extract_relation_ids((pg.get("properties") or {}).get("Moderación / coordinación"))
        moderacion = join_names([personas_map.get(pid) for pid in moderacion_ids])
        participantes_bruto = prop(pg, "Participantes")
        participantes = sorted(
            (linea.strip() for linea in (participantes_bruto or "").splitlines() if linea.strip()),
            key=str.casefold,
        )
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
            "moderacion": moderacion,
            "ponente": prop(pg, "Ponente"),
            "participantes": participantes,
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
        "sesiones": build_sesiones(personas_map),
        "generado": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "data.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=0)

    print(f"OK: {len(data['trabajos'])} trabajos, {len(data['sesiones'])} sesiones -> {out_path}")


if __name__ == "__main__":
    main()
