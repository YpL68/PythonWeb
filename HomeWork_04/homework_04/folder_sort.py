from pathlib import Path


class FolderSorter:
    def __init__(self, folder_path: str):
        if not folder_path.strip():
            raise ValueError("Specify a folder for sorting.")
        self.folder_path = Path(folder_path)
        if not (self.folder_path.exists() and self.folder_path.is_dir()):
            raise ValueError("Specified folder not found.")

        self._file_types = {"images":        {"file_ext": (".JPEG", ".PNG", ".JPG", ".SVG"), "file_list": []},
                            "video":         {"file_ext": (".AVI", ".MP4", ".MOV", ".MKV"), "file_list": []},
                            "documents":     {"file_ext": (".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX"),
                                              "file_list": []},
                            "audio":         {"file_ext": (".MP3", ".OGG", ".WAV", ".AMR"), "file_list": []},
                            "archives":      {"file_ext": (".ZIP", ".GZ", ".TAR"), "file_list": []},
                            "unknown_files": {"file_ext": (), "file_list": []}}

        self.__file_ext_links = {file_ext: folder for folder, params in self._file_types.items()
                                 for file_ext in params["file_ext"]}

        self.__known_file_extensions = set()
        self.__unknown_file_extensions = set()

    def __known_files_sorting(self, file: Path, destination_folder: str):
        try:
            self.__known_file_extensions.add(file.suffix.replace(".", ""))
            file.replace(Path(self.folder_path, destination_folder, file.name))
            self._file_types[destination_folder]["file_list"].append(file.name)
        except OSError as err:
            raise ValueError(f"Error:\n{err}")

    def __unknown_files_sorting(self, file: Path, destination_folder: str):
        try:
            self.__unknown_file_extensions.add(file.suffix.replace(".", ""))
            file.replace(Path(self.folder_path, destination_folder, file.name))
            self._file_types[destination_folder]["file_list"].append(file.name)
        except OSError as err:
            raise ValueError(f"Error:\n{err}")

    def file_action(self, file: Path):
        folder_name = self.__file_ext_links.get(file.suffix.upper(), "unknown_files")
        if folder_name == "unknown_files":
            self.__unknown_files_sorting(file, folder_name)
        else:
            self.__known_files_sorting(file, folder_name)

    def __create_folders(self):
        try:
            for folder in self._file_types.keys():
                Path(self.folder_path, folder).mkdir(exist_ok=True)
        except OSError as err:
            raise ValueError(f"An error occurred when creating folders:\n{err}")

    def __folder_sorting(self, path_dir: Path):
        for item in path_dir.iterdir():
            if item.is_dir():
                if item.name not in self._file_types.keys():
                    self.__folder_sorting(item)
            else:
                self.file_action(item)
        if self.is_folder_empty(path_dir):
            path_dir.rmdir()

    def __result_sorting(self) -> list:
        result = []
        for key, value in sorted(self._file_types.items()):
            if len(value["file_list"]):
                result.append([key, ", ".join(value["file_list"])])
        return result

    def execute(self) -> list:
        self.__create_folders()
        self.__folder_sorting(self.folder_path)
        return self.__result_sorting()

    @staticmethod
    def is_folder_empty(path_dir: Path) -> bool:
        return not (any(path_dir.iterdir()))


if __name__ == '__main__':
    # sorter = FolderSorter(r"f:\PythonPrj\Test_Opachki")
    sorter = FolderSorter("   ")

