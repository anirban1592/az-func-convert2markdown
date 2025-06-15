import azure.functions as func
import logging
import helper as h
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="extract", methods=["GET", "POST"])
def extract_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    start = req.params.get("start")
    end = req.params.get("end")
    top = req.params.get("top")
    url = req.params.get("url")

    if not url:
        return func.HttpResponse(
            "Please pass a URL on the query string or in the request body..",
            status_code=400,
        )
    if not start or not end:
        return func.HttpResponse(
            "Please pass both start and end parameters on the query string...",
            status_code=400,
        )

    return func.HttpResponse(
        json.dumps(
            h.fetch_urls_from_sitemap(
                url=url, start=int(start), end=int(end), top=int(top) if top else -1
            )
        ),
        mimetype="application/json",
        status_code=200,
    )
