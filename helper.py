from requests import get, Response
import xmlparser as xp
import pprint as pp
import xml.etree.ElementTree as ET


def fetch_sitemap(url: str, file_name: str) -> Response:
    """
    Fetches the sitemap from the given URL.

    :param url: The URL of the sitemap to fetch.
    :return: Response object containing the sitemap content.
    """
    params = {"sitemap": "true"}
    response = get(url, params=params)

    with open(file_name, "wb") as f:
        f.write(response.content)
    if response.status_code != 200:
        raise ValueError(
            f"Failed to fetch sitemap from {url}, status code: {response.status_code}"
        )
    return response


def fetch_urls_from_sitemap(url: str, start: int, end: int, top: int = -1) -> list[str]:
    """
    Fetch URLs from the sitemap within the specified range and limit.
    :param url: The URL of the sitemap.
    :param start: The starting index for the URLs to fetch.
    :param end: The ending index for the URLs to fetch.
    :param top: The maximum number of URLs to return. If -1, return all in the range.
    :return: A list of URLs from the sitemap.
    """
    file_name = "sitemap.xml"
    fetch_sitemap(url, file_name)

    tree = ET.parse(file_name)
    root = tree.getroot()

    list_urls = []

    # Define namespace
    ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    for url in root.findall("ns:url", ns):
        loc = url.find("ns:loc", ns)
        if loc is not None and loc.text:
            list_urls.append(loc.text)

    if top == -1:
        return list_urls[start:end]
    else:
        return list_urls[:top]
