from dataclasses import dataclass
from datetime import date
from typing import Protocol

from app.application.errors import InvalidPagination


@dataclass(frozen=True)
class Opportunity:
    id: str
    reference: str | None
    entity_name: str
    title: str
    description: str | None
    status: str | None
    summary_status: str | None
    opening_status: str
    published_at: str | None
    closing_at: str
    estimated_amount_cop: int | None
    source_url: str | None


@dataclass(frozen=True)
class OpportunityPage:
    items: list[Opportunity]
    page: int
    page_size: int
    has_more: bool


class ColombiaDateProvider(Protocol):
    def today_colombia(self) -> date: ...


class OpportunitySource(Protocol):
    def list_current(self, *, current_date: date, page: int, page_size: int) -> OpportunityPage: ...


class ListCurrentOpportunities:
    def __init__(self, source: OpportunitySource, date_provider: ColombiaDateProvider) -> None:
        self._source = source
        self._date_provider = date_provider

    def execute(self, *, page: int = 1, page_size: int = 20) -> OpportunityPage:
        if page < 1 or page_size < 1 or page_size > 50:
            raise InvalidPagination
        return self._source.list_current(
            current_date=self._date_provider.today_colombia(),
            page=page,
            page_size=page_size,
        )
