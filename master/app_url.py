import os

import tornado.web
from tornado_swagger.setup import setup_swagger
from handler.api.query.summaryHandler import summaryHandler
from handler.api.query.filterSummaryHandler import filterSummaryHandler


api_base_url = os.getenv("nginx_proxy_path", "/")
proxy_type = os.getenv("proxy_type", "http")


class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(r"/worker/gpt_summary", summaryHandler),
        tornado.web.url(r"/worker/word_summary", filterSummaryHandler)
    ]

    def __init__(self, **settings):
        setup_swagger(
            self._routes,
            swagger_url="/docs",
            api_base_url=api_base_url,
            description="",
            api_version="1.0.0",
            title="NLU API",
            contact="name@domain",
            schemes=['https', 'http'],
            security_definitions={
                "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-Key"}
            },
        )
        super(Application, self).__init__(self._routes, **settings)


# tornado_opentracing.init_tracing()
app = Application()
