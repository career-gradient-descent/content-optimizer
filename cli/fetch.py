""" Deterministic job-description extraction. """

import trafilatura

# Real JDs run to several thousand characters. Partial-render and boilerplate-only
# extractions were observed at <=751 (JS-rendered pages whose static HTML carries only
# an app shell or footer). Below this floor we refuse rather than emit low-confidence
# content, biasing toward manual paste.
MIN_EXTRACT_CHARS = 1000


class FetchError(Exception):
    """ JD extraction failed, or fell below the confidence floor. """


def fetch_jd_markdown(url: str) -> str:
    """ Fetch a JD page and extract its main content as markdown, deterministically.

    Raises FetchError when the page can't be fetched, yields no content, or yields too
    little to trust. The last case is typically a JS-rendered page whose static HTML
    carries only an app shell or boilerplate. """

    html = trafilatura.fetch_url(url)
    if html is None:
        raise FetchError(f"could not fetch {url}")

    markdown = trafilatura.extract(html, output_format="markdown", include_comments=False)
    if not markdown:
        raise FetchError(f"no content extracted from {url} (likely JS-rendered; paste manually)")

    if len(markdown) < MIN_EXTRACT_CHARS:
        raise FetchError(
            f"only {len(markdown)} chars extracted from {url}, below the {MIN_EXTRACT_CHARS}-char "
            f"confidence floor (likely partial render or boilerplate; paste manually)"
        )

    return markdown
