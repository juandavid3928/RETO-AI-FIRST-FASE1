from datetime import date

import pytest

from app.application.errors import InvalidPagination
from app.application.use_cases.list_current_opportunities import (
    ListCurrentOpportunities,
    Opportunity,
    OpportunityPage,
)


class DateProviderStub:
    def today_colombia(self) -> date:
        return date(2026, 7, 23)


class SourceStub:
    def __init__(self, page: OpportunityPage | None = None) -> None:
        self.page = page or OpportunityPage(items=[], page=1, page_size=20, has_more=False)
        self.calls: list[tuple[date, int, int]] = []

    def list_current(self, *, current_date: date, page: int, page_size: int) -> OpportunityPage:
        self.calls.append((current_date, page, page_size))
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


def test_lists_current_opportunities_using_colombia_date_and_pagination() -> None:
    expected = OpportunityPage(items=[opportunity()], page=2, page_size=10, has_more=True)
    source = SourceStub(expected)

    result = ListCurrentOpportunities(source, DateProviderStub()).execute(page=2, page_size=10)

    assert result == expected
    assert source.calls == [(date(2026, 7, 23), 2, 10)]


@pytest.mark.parametrize("page,page_size", [(0, 20), (1, 0), (1, 51), (-1, 20)])
def test_rejects_invalid_pagination_before_calling_secop(page: int, page_size: int) -> None:
    source = SourceStub()

    with pytest.raises(InvalidPagination):
        ListCurrentOpportunities(source, DateProviderStub()).execute(page=page, page_size=page_size)

    assert source.calls == []
