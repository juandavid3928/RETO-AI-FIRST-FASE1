import json
from datetime import date

import httpx
import pytest

from app.application.errors import ExternalOpportunitySourceUnavailable
from app.infrastructure.external.secop_opportunity_source import SecopOpportunitySource


VALID_ROW = {
    "id_del_proceso": "CO1.REQ.10658713",
    "referencia_del_proceso": "SA-SIE-016-2026",
    "entidad": "MUNICIPIO DE BRICEÑO",
    "nombre_del_procedimiento": "Arrendamiento de vehículo",
    "descripci_n_del_procedimiento": "Contratar el arrendamiento de vehículo",
    "estado_del_procedimiento": "Publicado",
    "estado_resumen": "Presentación de oferta",
    "estado_de_apertura_del_proceso": "Abierto",
    "fecha_de_publicacion_del": "2026-07-15T00:00:00.000",
    "fecha_de_recepcion_de": "2026-07-23T00:00:00.000",
    "precio_base": "77500000",
    "urlproceso": {"url": "https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10512397"},
}


def source_for(handler) -> SecopOpportunitySource:
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return SecopOpportunitySource(client=client, base_url="https://www.datos.gov.co/resource/p6dx-8zbt.json")


def test_queries_secop_with_bounded_soql_and_normalizes_payload() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["params"] = dict(request.url.params)
        return httpx.Response(200, json=[VALID_ROW, {**VALID_ROW, "id_del_proceso": "CO1.REQ.999"}])

    page = source_for(handler).list_current(current_date=date(2026, 7, 23), page=2, page_size=1)

    assert seen["params"]["$limit"] == "2"
    assert seen["params"]["$offset"] == "1"
    assert "estado_de_apertura_del_proceso='Abierto'" in seen["params"]["$where"]
    assert "fecha_de_recepcion_de >= '2026-07-23T00:00:00'" in seen["params"]["$where"]
    assert seen["params"]["$order"] == "fecha_de_recepcion_de ASC, fecha_de_publicacion_del DESC, id_del_proceso ASC"
    assert page.page == 2
    assert page.page_size == 1
    assert page.has_more is True
    assert page.items[0].id == "CO1.REQ.10658713"
    assert page.items[0].estimated_amount_cop == 77500000
    assert page.items[0].source_url.startswith("https://community.secop.gov.co/")


def test_empty_payload_is_successful_empty_page() -> None:
    page = source_for(lambda _: httpx.Response(200, json=[])).list_current(current_date=date(2026, 7, 23), page=1, page_size=20)

    assert page.items == []
    assert page.has_more is False


@pytest.mark.parametrize("status", [403, 429, 500, 503])
def test_http_failures_are_external_unavailable(status: int) -> None:
    with pytest.raises(ExternalOpportunitySourceUnavailable):
        source_for(lambda _: httpx.Response(status, text="private external payload")).list_current(current_date=date(2026, 7, 23), page=1, page_size=20)


def test_timeout_is_external_unavailable() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("slow", request=httpx.Request("GET", "https://example.test"))

    with pytest.raises(ExternalOpportunitySourceUnavailable):
        source_for(handler).list_current(current_date=date(2026, 7, 23), page=1, page_size=20)


def test_uses_configured_timeout_for_secop_request() -> None:
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["timeout"] = request.extensions["timeout"]
        return httpx.Response(200, json=[])

    SecopOpportunitySource(
        client=httpx.Client(transport=httpx.MockTransport(handler)),
        base_url="https://example.test/secop",
        timeout_seconds=2.5,
    ).list_current(current_date=date(2026, 7, 23), page=1, page_size=20)

    assert seen["timeout"]["connect"] == 2.5
    assert seen["timeout"]["read"] == 2.5


def test_invalid_json_and_malformed_rows_are_external_unavailable() -> None:
    invalid_json = source_for(lambda _: httpx.Response(200, content=b"not-json"))
    with pytest.raises(ExternalOpportunitySourceUnavailable):
        invalid_json.list_current(current_date=date(2026, 7, 23), page=1, page_size=20)

    malformed = source_for(lambda _: httpx.Response(200, json=[{**VALID_ROW, "id_del_proceso": ""}]))
    with pytest.raises(ExternalOpportunitySourceUnavailable):
        malformed.list_current(current_date=date(2026, 7, 23), page=1, page_size=20)
