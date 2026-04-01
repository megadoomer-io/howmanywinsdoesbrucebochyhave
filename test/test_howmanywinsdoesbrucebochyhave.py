from collections.abc import AsyncIterator
from unittest import mock

import httpx
import lxml.html
import pytest

import howmanywinsdoesbrucebochyhave.howmanywinsdoesbrucebochyhave as app_module
from howmanywinsdoesbrucebochyhave import app


@pytest.fixture
async def client(sample_html: str) -> AsyncIterator[httpx.AsyncClient]:
    with mock.patch.object(app_module, "get_document", return_value=sample_html):
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            yield client


class TestParsing:
    def test_get_wins(self, sample_html: str) -> None:
        doc = lxml.html.fromstring(sample_html)
        assert app_module.get_wins(doc) == "2003"

    def test_get_revised(self, sample_html: str) -> None:
        doc = lxml.html.fromstring(sample_html)
        assert app_module.get_revised(doc) == "01:23, 15 March 2026"

    def test_extract_table_not_found(self, sample_html: str) -> None:
        doc = lxml.html.fromstring(sample_html)
        with pytest.raises(ValueError, match="Table 'nonexistent' not found"):
            app_module.extract_table(doc, "nonexistent")

    def test_get_championships(self, sample_html: str) -> None:
        doc = lxml.html.fromstring(sample_html)
        assert app_module.get_championships(doc) == 4

    def test_get_championships_none(self) -> None:
        html = """<html><body><table id="manager_stats">
        <thead><tr><th>Year</th></tr></thead>
        <tbody>
        <tr><td data-stat="year_ID">2024</td><td data-stat="W">94</td><td data-stat="comments"></td></tr>
        </tbody>
        <tfoot><tr><td data-stat="W">94</td></tr></tfoot>
        </table></body></html>"""
        doc = lxml.html.fromstring(html)
        assert app_module.get_championships(doc) == 0

    def test_extract_field_not_found(self, sample_html: str) -> None:
        doc = lxml.html.fromstring(sample_html)
        table = app_module.extract_table(doc, "manager_stats")
        footer = app_module.extract_table_footer(table)
        row = app_module.extract_row(footer, "last()")
        with pytest.raises(ValueError, match="Field 'nonexistent' not found"):
            app_module.extract_field(row, "nonexistent")


class TestCaching:
    def test_cache_returns_same_result(self) -> None:
        call_count = 0

        def fake_get(url: str, timeout: int = 30) -> mock.Mock:
            nonlocal call_count
            call_count += 1
            resp = mock.Mock()
            resp.text = f"<html><body>call {call_count}</body></html>"
            return resp

        with mock.patch("requests.get", side_effect=fake_get):
            first = app_module.get_document("http://example.com")
            second = app_module.get_document("http://example.com")

        assert first == second
        assert call_count == 1


class TestRoute:
    @pytest.mark.anyio
    async def test_index_returns_wins(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/")
        assert response.status_code == 200
        assert "2003" in response.text
        assert "Bruce Bochy" in response.text

    @pytest.mark.anyio
    async def test_index_returns_html(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/")
        assert "text/html" in response.headers["content-type"]

    @pytest.mark.anyio
    async def test_index_includes_revised(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/")
        assert "01:23, 15 March 2026" in response.text

    @pytest.mark.anyio
    async def test_index_includes_championships(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/")
        assert response.status_code == 200
        # 4 WS Champs rows in sample HTML = 4 trophies
        assert response.text.count("\U0001f3c6") == 4

    @pytest.mark.anyio
    async def test_healthz(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/healthz")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    @pytest.mark.anyio
    async def test_static_css(self, client: httpx.AsyncClient) -> None:
        response = await client.get("/static/css/styles.css")
        assert response.status_code == 200
        assert "background-color" in response.text
