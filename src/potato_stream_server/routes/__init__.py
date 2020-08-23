from aiohttp import web
from . import live
import aiohttp_cors


def add_routes_to_app(app: web.Application) -> None:
    app.add_routes(live.routes)

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*",
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)
