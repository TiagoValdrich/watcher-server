from aiohttp import web
from potato_stream_server.routes import add_routes_to_app
import aiohttp_cors

app = web.Application()

add_routes_to_app(app)

web.run_app(app, port=8081)
