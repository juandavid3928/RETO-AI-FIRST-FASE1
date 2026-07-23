from datetime import date
from uuid import UUID

from fastapi.testclient import TestClient

from app.application.errors import ExternalOpportunitySourceUnavailable
from app.application.use_cases.list_current_opportunities import Opportunity, OpportunityPage
from app.application.use_cases.validate_access_token import AuthenticatedPrincipal
from app.interfaces.api.app import create_app
from app.application.errors import InvalidAccessToken


USER_ID = UUID("8bb45e10-84cb-4b89-8f75-c27bbb319fe8")


class RegisterStub:
    def execute(self, email: str, password: str):
        raise AssertionError("registration is out of this test")


class ValidateStub:
    def execute(self, token: str) -> AuthenticatedPrincipal:
        if token != "valid.jwt":
            raise InvalidAccessToken
        return AuthenticatedPrincipal(USER_ID)


class OpportunitiesStub:
    def __init__(self, page: OpportunityPage | None = None, error: Exception | None = None) -> None:
        self.page = page or OpportunityPage(items=[], page=1, page_size=20, has_more=False)
        self.error = error
        self.calls: list[tuple[int, int]] = []

    def execute(self, *, page: int, page_size: int) -> OpportunityPage:
        self.calls.append((page, page_size))
        if self.error:
            raise self.error
        return self.page


def opportunity() -> Opportunity:
    return Opportunity(
        id="CO1.REQ.10658713",
        reference="SA-SIE-016-2026",
        entity_name="MUNICIPIO DE BRICEÑO",
        title="Arrendamiento de vehículo",
        description="Contratar el arrendamiento de vehículo",
        status="Publicado",
        summary_status="Presentación de oferta",
        opening_status="Abierto",
        published_at="2026-07-15T00:00:00.000",
        closing_at="2026-07-23T00:00:00.000",
        estimated_amount_cop=77500000,
        source_url="https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10512397",
    )


def client(stub: OpportunitiesStub | None = None) -> tuple[TestClient, OpportunitiesStub]:
    stub = stub or OpportunitiesStub(OpportunityPage(items=[opportunity()], page=1, page_size=20, has_more=False))
    app = create_app(register_user=RegisterStub(), validate_access_token=ValidateStub(), list_current_opportunities=stub)
    return TestClient(app, raise_server_exceptions=False), stub


def assert_private(response) -> None:
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["pragma"] == "no-cache"
    assert response.headers["vary"] == "Authorization"


def test_get_opportunities_returns_private_normalized_page() -> None:
    api, stub = client()

    response = api.get("/api/v1/opportunities", headers={"authorization": "Bearer valid.jwt"})

    assert response.status_code == 200
    assert response.json() == {
        "items": [opportunity().__dict__],
        "page": 1,
        "page_size": 20,
        "has_more": False,
    }
    assert stub.calls == [(1, 20)]
    assert_private(response)


def test_opportunities_requires_valid_bearer() -> None:
    api, stub = client()

    missing = api.get("/api/v1/opportunities")
    invalid = api.get("/api/v1/opportunities", headers={"authorization": "Bearer invalid.jwt"})

    assert missing.status_code == invalid.status_code == 401
    assert missing.headers["www-authenticate"] == invalid.headers["www-authenticate"] == "Bearer"
    assert_private(missing)
    assert_private(invalid)
    assert stub.calls == []


def test_opportunities_validates_pagination_query_parameters() -> None:
    api, stub = client()

    response = api.get("/api/v1/opportunities?page=0&page_size=51", headers={"authorization": "Bearer valid.jwt"})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["message"] == "Opportunity query is invalid."
    assert "page" in response.json()["error"]["fields"]
    assert "page_size" in response.json()["error"]["fields"]
    assert stub.calls == []
    assert_private(response)


def test_opportunities_translates_external_failure_to_503_without_details() -> None:
    api, _ = client(OpportunitiesStub(error=ExternalOpportunitySourceUnavailable("private payload")))

    response = api.get("/api/v1/opportunities", headers={"authorization": "Bearer valid.jwt"})

    assert response.status_code == 503
    assert response.json() == {"error": {"code": "external_service_unavailable", "message": "Opportunities are temporarily unavailable."}}
    assert "private payload" not in response.text
    assert_private(response)
