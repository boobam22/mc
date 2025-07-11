import os
import tempfile
import shutil
import asyncio
import typing as t

from httpx import AsyncClient

if t.TYPE_CHECKING:
    from pathlib import Path

    URI = tuple[str, Path, int | None]

if (ua := os.getenv("USER_AGENT")) is not None:
    headers = {"User-Agent": ua}
else:
    headers = None

client = AsyncClient(
    headers=headers,
    follow_redirects=True,
    http2=True,
)

loop = asyncio.get_event_loop()


def download_sync(url: str, dst: "Path", size: int | None = None):
    loop.run_until_complete(download(url, dst, size))


async def download(url: str, dst: "Path", size: int | None = None):
    if dst.exists():
        return

    async with client.stream("GET", url) as res:
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp:
            n = 0
            async for chunk in res.aiter_bytes():
                n += tmp.write(chunk)

            if size is not None:
                assert n == size

        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(tmp.name, dst)


def download_all_sync(items: t.Iterable["URI"]):
    loop.run_until_complete(download_all(items))


async def download_all(items: t.Iterable["URI"]):
    q: asyncio.Queue["URI"] = asyncio.Queue()

    async def worker():
        while True:
            uri = await q.get()
            await download(*uri)
            q.task_done()

    tasks = [asyncio.create_task(worker()) for _ in range(32)]

    for item in items:
        await q.put(item)

    await q.join()

    for task in tasks:
        task.cancel()
