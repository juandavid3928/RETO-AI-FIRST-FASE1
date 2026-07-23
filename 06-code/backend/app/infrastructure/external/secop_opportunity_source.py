from datetime import date
from typing import Any

import httpx

from app.application.errors import ExternalOpportunitySourceUnavailable
from app.application.use_cases.list_current_opportunities import Opportunity, OpportunityPage

SELECT_FIELDS = ",".join(
    [
        "id_del_proceso",
        "referencia_del_proceso",
        "entidad",
        "nombre_del_procedimiento",
        "descripci_n_del_procedimiento",
        "estado_del_procedimiento",
        "estado_de_apertura_del_proceso",
        "estado_resumen",
        "fecha_de_publicacion_del",
        "fecha_de_recepcion_de",
        "precio_base",
        "urlproceso",
    ]
)
ORDER = "fecha_de_recepcion_de ASC, fecha_de_publicacion_del DESC, id_del_proceso ASC"
DEFAULT_BASE_URL = "https://www.datos.gov.co/resource/p6dx-8zbt.json"


class SecopOpportunitySource:
    def __init__(self, *, client: httpx.Client | None = None, base_url: str = DEFAULT_BASE_URL) -> None:
        self._client = client or httpx.Client(timeout=5.0)
        self._base_url = base_url

    def list_current(self, *, current_date: date, page: int, page_size: int) -> OpportunityPage:
        params = {
            "$select": SELECT_FIELDS,
            "$where": f"estado_de_apertura_del_proceso='Abierto' AND fecha_de_recepcion_de >= '{current_date.isoformat()}T00:00:00'",
            "$order": ORDER,
            "$limit": str(page_size + 1),
            "$offset": str((page - 1) * page_size),
        }
        try:
            response = self._client.get(self._base_url, params=params, timeout=5.0)
        except httpx.TimeoutException as exc:
            raise ExternalOpportunitySourceUnavailable from exc
        except httpx.HTTPError as exc:
            raise ExternalOpportunitySourceUnavailable from exc
        if response.status_code in {403, 429} or response.status_code >= 500:
            raise ExternalOpportunitySourceUnavailable
        if response.status_code >= 400:
            raise ExternalOpportunitySourceUnavailable
        try:
            payload = response.json()
        except ValueError as exc:
            raise ExternalOpportunitySourceUnavailable from exc
        if not isinstance(payload, list):
            raise ExternalOpportunitySourceUnavailable
        rows = payload[: page_size]
        return OpportunityPage(
            items=[_normalize_row(row) for row in rows],
            page=page,
            page_size=page_size,
            has_more=len(payload) > page_size,
        )


def _normalize_row(row: Any) -> Opportunity:
    if not isinstance(row, dict):
        raise ExternalOpportunitySourceUnavailable
    process_id = _required_text(row, "id_del_proceso")
    entity = _required_text(row, "entidad")
    title = _required_text(row, "nombre_del_procedimiento")
    opening_status = _required_text(row, "estado_de_apertura_del_proceso")
    closing_at = _required_text(row, "fecha_de_recepcion_de")
    source_url = None
    url_value = row.get("urlproceso")
    if isinstance(url_value, dict) and isinstance(url_value.get("url"), str) and url_value["url"].strip():
        source_url = url_value["url"].strip()
    amount = _optional_int(row.get("precio_base"))
    return Opportunity(
        id=process_id,
        reference=_optional_text(row.get("referencia_del_proceso")),
        entity_name=entity,
        title=title,
        description=_optional_text(row.get("descripci_n_del_procedimiento")),
        status=_optional_text(row.get("estado_del_procedimiento")),
        summary_status=_optional_text(row.get("estado_resumen")),
        opening_status=opening_status,
        published_at=_optional_text(row.get("fecha_de_publicacion_del")),
        closing_at=closing_at,
        estimated_amount_cop=amount,
        source_url=source_url,
    )


def _required_text(row: dict[str, Any], key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ExternalOpportunitySourceUnavailable
    return value.strip()


def _optional_text(value: Any) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _optional_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ExternalOpportunitySourceUnavailable from exc
