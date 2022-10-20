from pathlib import Path
from time import time
import concurrent.futures


MAX_WORKERS = 4


class FolderSorter:
    def __init__(self, folder_path: str):
        if not folder_path.strip():
            raise ValueError("Specify a folder for sorting.")
        self._folder = Path(folder_path)
        if not (self._folder.exists() and self._folder.is_dir()):
            raise ValueError("Specified folder not found.")

        self._file_types = {"images": {"file_ext": (".JPEG", ".PNG", ".JPG", ".SVG")},
                            "video": {"file_ext": (".AVI", ".MP4", ".MOV", ".MKV")},
                            "documents": {"file_ext": (".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX")},
                            "audio": {"file_ext": (".MP3", ".OGG", ".WAV", ".AMR")},
                            "archives": {"file_ext": (".ZIP", ".GZ", ".TAR")},
                            "unknown_files": {"file_ext": ()}}

        self.__file_ext_links = {file_ext: folder for folder, params in self._file_types.items()
                                 for file_ext in params["file_ext"]}

    def __file_action(self, file: Path):
        folder_name = self.__file_ext_links.get(file.suffix.upper(), "unknown_files")
        try:
            file.replace(Path(self._folder, folder_name, file.name))
        except OSError as err:
            raise ValueError(f"Error:\n{err}")

    def __base_folders_create(self):
        try:
            for folder in self._file_types.keys():
                Path(self._folder, folder).mkdir(exist_ok=True)
        except OSError as err:
            raise ValueError(f"An error occurred when creating folders:\n{err}")

    def __folder_handler(self, folder: Path):
        file_list = [item for item in folder.iterdir() if not item.is_dir()]

        if file_list:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.map(self.__file_action, file_list)

    def __sub_folders_layer(self):
        list_folders = [self._folder]

        def inner_layer() -> list:
            nonlocal list_folders
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                results = list(executor.map(self.__get_sub_folders, list_folders))
            list_folders = [folder for _folder_list in results for folder in _folder_list]
            return list_folders

        return inner_layer

    def __get_all_folders(self) -> list:  # recursion free !!!
        folders_layer = self.__sub_folders_layer()
        layer_folders = [self._folder]
        layer_folders.extend(folders_layer())
        yield layer_folders

        while layer_folders:
            layer_folders = folders_layer()
            if layer_folders:
                yield layer_folders

    def run(self):
        processed_folders = []

        self.__base_folders_create()

        for layer_folders in self.__get_all_folders():  # folder layer processing with threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.map(self.__folder_handler, layer_folders)
            processed_folders.insert(0, layer_folders)

        for layer_folders in processed_folders:
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                executor.map(self.__delete_empty_folder, layer_folders)

    @staticmethod
    def __get_sub_folders(_folder: Path) -> list:
        return [item for item in _folder.iterdir() if item.is_dir()]

    @staticmethod
    def __delete_empty_folder(_folder: Path):
        if not (any(_folder.iterdir())):
            _folder.rmdir()


if __name__ == '__main__':
    t_start = time()
    sorter = FolderSorter(r"f:\PythonPrj\Test_Opachki")
    sorter.run()
    print(time() - t_start)
