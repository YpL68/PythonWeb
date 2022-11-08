import logging
import asyncio
from aiopath import AsyncPath
from pathlib import Path
from time import time


class FolderSorter:
    def __init__(self, folder_path: str):
        self.folder = folder_path

        self.__file_types = {"images": {"file_ext": (".JPEG", ".PNG", ".JPG", ".SVG")},
                             "video": {"file_ext": (".AVI", ".MP4", ".MOV", ".MKV")},
                             "documents": {"file_ext": (".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX")},
                             "audio": {"file_ext": (".MP3", ".OGG", ".WAV", ".AMR")},
                             "archives": {"file_ext": (".ZIP", ".GZ", ".TAR", ".RAR")},
                             "unknown_files": {"file_ext": ()}}

        self.__file_ext_links = {file_ext: folder for folder, params in self.__file_types.items()
                                 for file_ext in params["file_ext"]}

    @property
    def folder(self) -> str:
        return str(self.__folder)

    @folder.setter
    def folder(self, folder_path: str):
        if not folder_path.strip():
            raise ValueError("Specify a folder for sorting.")
        if not (Path(folder_path).exists() and Path(folder_path).is_dir()):
            raise ValueError("Specified folder not found.")
        self.__folder = AsyncPath(folder_path)

    async def __file_action(self, file: AsyncPath):
        folder_name = self.__file_ext_links.get(file.suffix.upper(), "unknown_files")
        new_file = AsyncPath(self.__folder, folder_name, file.name)
        # await asyncio.sleep(5)  # for async test
        try:
            if not await new_file.exists():
                await file.replace(new_file)
        except (OSError, PermissionError) as err:
            logging.error(f"An error occurred when copy file {file}:\n{err}")

    async def __base_folders_create(self):
        cors = [AsyncPath(self.__folder, folder).mkdir(exist_ok=True)
                for folder in self.__file_types.keys()]
        tasks = []
        for item in cors:
            try:
                tasks.append(asyncio.create_task(item))
            except (OSError, PermissionError) as err:
                logging.error(f"An error occurred when creating base folder:\n{err}")
        [await task for task in tasks]

    async def __get_sub_folders(self, _folder: AsyncPath) -> list:
        try:
            if self.__folder == _folder:
                return [item async for item in _folder.iterdir()
                        if await item.is_dir() and item.name not in self.__file_types.keys()]
            else:
                return [item async for item in _folder.iterdir() if await item.is_dir()]
        except (OSError, PermissionError) as err:
            logging.error(f"An error occurred when receiving sub folders:\n{err}")

    async def __folder_handler(self, folder: AsyncPath):
        file_list = [item async for item in folder.iterdir() if not await item.is_dir()]

        if file_list:
            cors = [self.__file_action(file) for file in file_list]
            tasks = [asyncio.create_task(item) for item in cors]
            [await task for task in tasks]

    @staticmethod
    async def __sub_folders_layer(path: AsyncPath) -> list:
        return [item async for item in path.iterdir() if await item.is_dir()]

    async def __get_all_folders(self):  # recursion free
        yield [self.__folder]

        results = [item async for item in self.__folder.iterdir()
                   if await item.is_dir() and item.name not in self.__file_types.keys()]
        if results:
            yield results

            while results:
                cors = [self.__sub_folders_layer(folder) for folder in results]
                # await asyncio.sleep(1)  # for async test
                result = await asyncio.gather(*cors)
                results = [folder for _folder_list in result for folder in _folder_list]
                if results:
                    yield results

    async def run(self):
        processed_folders_stack = []

        await self.__base_folders_create()

        # files processing
        async for layer_folders in self.__get_all_folders():
            cors = [self.__folder_handler(folder) for folder in layer_folders]
            tasks = [asyncio.create_task(item) for item in cors]
            [await task for task in tasks]

            processed_folders_stack.insert(0, layer_folders)

        # deleting empty folders
        for layer_folders in processed_folders_stack:
            cors = [self.__delete_empty_folder(folder) for folder in layer_folders]
            tasks = [asyncio.create_task(item) for item in cors]
            [await task for task in tasks]

    @staticmethod
    async def __delete_empty_folder(_folder: AsyncPath):
        if not [item async for item in _folder.iterdir()]:
            try:
                await _folder.rmdir()
            except (OSError, PermissionError) as err:
                logging.error(f"An error occurred when deleting folder {_folder}:\n{err}")


if __name__ == '__main__':
    sorter = FolderSorter(r"c:\PythonPrj\TestFolder")
    s_time = time()
    asyncio.run(sorter.run())
    print(time() - s_time)
