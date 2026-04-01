import pytest

import howmanywinsdoesbrucebochyhave.howmanywinsdoesbrucebochyhave as app_module


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    """Clear the TTL cache between tests so mocked responses are used."""
    app_module.get_document.cache_clear()


SAMPLE_HTML = """\
<html>
<head>
<meta name="revised" content="01:23, 15 March 2026" />
</head>
<body>
<table id="manager_stats">
<thead><tr><th>Year</th><th>W</th><th>L</th></tr></thead>
<tbody>
<tr>
  <td data-stat="year_ID">2010</td>
  <td data-stat="team_ID">San Francisco Giants</td>
  <td data-stat="W">92</td><td data-stat="L">70</td>
  <td data-stat="comments">WS Champs</td>
</tr>
<tr>
  <td data-stat="year_ID">2012</td>
  <td data-stat="team_ID">San Francisco Giants</td>
  <td data-stat="W">94</td><td data-stat="L">68</td>
  <td data-stat="comments">WS Champs</td>
</tr>
<tr>
  <td data-stat="year_ID">2014</td>
  <td data-stat="team_ID">San Francisco Giants</td>
  <td data-stat="W">88</td><td data-stat="L">74</td>
  <td data-stat="comments">WS Champs</td>
</tr>
<tr>
  <td data-stat="year_ID">2023</td>
  <td data-stat="team_ID">Texas Rangers</td>
  <td data-stat="W">90</td><td data-stat="L">72</td>
  <td data-stat="comments">WS Champs</td>
</tr>
<tr>
  <td data-stat="year_ID">2024</td>
  <td data-stat="team_ID">Texas Rangers</td>
  <td data-stat="W">94</td><td data-stat="L">68</td>
  <td data-stat="comments"></td>
</tr>
</tbody>
<tfoot>
<tr><td data-stat="year_ID">Career</td><td data-stat="W">2003</td><td data-stat="L">1789</td></tr>
</tfoot>
</table>
</body>
</html>
"""


@pytest.fixture
def sample_html() -> str:
    return SAMPLE_HTML
