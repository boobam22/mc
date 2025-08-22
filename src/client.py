import os
import tempfile
import shutil
import asyncio
import typing as t

from httpx import Client, AsyncClient

if t.TYPE_CHECKING:
    from pathlib import Path

    URI = tuple[str, Path, int | None]

if (ua := os.getenv("USER_AGENT")) is not None:
    headers = {"User-Agent": ua}
else:
    headers = None

client = Client(
    headers=headers,
    follow_redirects=True,
    http2=True,
)
aclient = AsyncClient(
    headers=headers,
    follow_redirects=True,
    http2=True,
)

loop = asyncio.get_event_loop()


def download(url: str, dst: "Path", size: int | None = None):
    if dst.exists():
        return

    with client.stream("GET", url) as res:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
            n = 0
            for chunk in res.iter_bytes():
                n += tmp.write(chunk)
            if size is not None:
                assert n == size

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp.name, dst)


async def adownload(url: str, dst: "Path", size: int | None = None):
    if dst.exists():
        return

    async with aclient.stream("GET", url) as res:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
            n = 0
            async for chunk in res.aiter_bytes():
                n += tmp.write(chunk)
            if size is not None:
                assert n == size

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp.name, dst)


def download_all(items: t.Iterable["URI"]):
    loop.run_until_complete(adownload_all(items))


async def adownload_all(items: t.Iterable["URI"]):
    q: asyncio.Queue["URI"] = asyncio.Queue()

    async def worker():
        while True:
            uri = await q.get()
            await adownload(*uri)
            q.task_done()

    tasks = [asyncio.create_task(worker()) for _ in range(32)]

    for item in items:
        await q.put(item)

    await q.join()

    for task in tasks:
        task.cancel()
