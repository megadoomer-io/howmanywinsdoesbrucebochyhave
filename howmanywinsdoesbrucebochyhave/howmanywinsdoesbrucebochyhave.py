import cachetools.func
import fastapi
import fastapi.responses
import fastapi.staticfiles
import fastapi.templating
import lxml.html
import requests

MANAGER_URL = "https://www.baseball-reference.com/managers/bochybr01.shtml"

templates = fastapi.templating.Jinja2Templates(directory="templates")


@cachetools.func.ttl_cache(ttl=(15 * 60))
def get_document(url: str = MANAGER_URL) -> str:
    return requests.get(url, timeout=30).text


def extract_table(doc: lxml.html.HtmlElement, table_id: str) -> lxml.html.HtmlElement:
    result = doc.find(f'.//table[@id="{table_id}"]')
    if result is None:
        raise ValueError(f"Table '{table_id}' not found")
    return result


def extract_table_footer(table: lxml.html.HtmlElement) -> lxml.html.HtmlElement:
    result = table.find("./tfoot")
    if result is None:
        raise ValueError("Table footer not found")
    return result


def extract_field(row: lxml.html.HtmlElement, field: str) -> str:
    element = row.find(f'.//td[@data-stat="{field}"]')
    if element is None or element.text is None:
        raise ValueError(f"Field '{field}' not found")
    return element.text


def extract_row(rows: lxml.html.HtmlElement, index: str) -> lxml.html.HtmlElement:
    result = rows.find(f".//tr[{index}]")
    if result is None:
        raise ValueError(f"Row at index '{index}' not found")
    return result


def get_wins(doc: lxml.html.HtmlElement) -> str:
    table = extract_table(doc, "manager_stats")
    footer = extract_table_footer(table)
    row = extract_row(footer, "last()")
    return extract_field(row, "W")


def get_championships(doc: lxml.html.HtmlElement) -> int:
    table = extract_table(doc, "manager_stats")
    rows = table.find(".//tbody")
    if rows is None:
        return 0
    count = 0
    for tr in rows.findall(".//tr"):
        comments = tr.find('.//td[@data-stat="comments"]')
        if comments is not None and comments.text_content().strip() == "WS Champs":
            count += 1
    return count


def get_revised(doc: lxml.html.HtmlElement) -> str:
    meta = doc.find("./head/meta[@name='revised']")
    if meta is None:
        raise ValueError("Revised meta tag not found")
    return str(meta.attrib["content"])


def create_app() -> fastapi.FastAPI:
    app = fastapi.FastAPI(title="HowManyWinsDoesBruceBochyHave")
    app.mount("/static", fastapi.staticfiles.StaticFiles(directory="static"), name="static")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", response_class=fastapi.responses.HTMLResponse)
    def index(request: fastapi.Request) -> fastapi.responses.HTMLResponse:
        doc = lxml.html.fromstring(get_document(MANAGER_URL))
        wins = get_wins(doc)
        revised = get_revised(doc)
        championships = get_championships(doc)
        content = templates.TemplateResponse(
            request, "index.html", {"wins": wins, "revised": revised, "championships": championships}
        )
        return content

    return app
