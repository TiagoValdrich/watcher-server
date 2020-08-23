from aiohttp import web
from subprocess import Popen
import uuid
import os

routes = web.RouteTableDef()
routes.static("/live", os.getcwd() + "/live")

running_processes = []


@routes.get("/")
async def root(req: web.Request):
    return web.Response(text="Server running")


@routes.post("/stream-url")
async def start_stream(req: web.Request):
    body = await req.json()
    rtsp = body["rtsp"]
    stream_id = str(uuid.uuid4())
    live = f"live/{stream_id}"
    os.mkdir(live)

    p = Popen(
        [
            "ffmpeg",
            "-i",
            rtsp,
            "-y",
            "-c:a",
            "aac",
            "-b:a",
            "160000",
            "-ac",
            "2",
            "-s",
            "854x480",
            "-c:v",
            "libx264",
            "-b:v",
            "800000",
            "-hls_time",
            "5",
            "-hls_list_size",
            "5",
            "-start_number",
            "1",
            f"{live}/playlist.m3u8",
        ]
    )

    running_processes.append((stream_id, p))

    return web.json_response(
        {"stream_url": f"http://localhost:8081/live/{stream_id}/playlist.m3u8"},
        status=200,
    )


@routes.delete("/close-stream-url/{stream_id}")
async def close_stream(req: web.Request):
    stream_id = req.match_info["stream_id"]

    for (i, process) in running_processes:
        if process[0] == stream_id:
            process[1].kill()
            running_processes.pop(i)

    return web.Response(status=200)

