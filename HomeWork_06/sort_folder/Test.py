import asyncio
from aiopath import AsyncPath
from time import time


async def a_read_folder(path: AsyncPath) -> None:
    # await asyncio.sleep(0.1)
    cor = []
    async for el in path.iterdir():
        if await el.is_dir():
            await asyncio.sleep(0.1)
            print(el.name)


async def main():
    print("Start main")
    cor = [a_read_folder(AsyncPath(r"c:\PythonPrj\TestFolder")) for _ in range(10)]
    tasks = [asyncio.create_task(c) for c in cor]
    [await t for t in tasks]

    print("End main")


if __name__ == '__main__':
    s_time = time()
    asyncio.run(main())
    print(time() - s_time)
