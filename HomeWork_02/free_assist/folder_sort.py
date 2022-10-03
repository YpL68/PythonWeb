import re
from pathlib import Path

from free_assist.function import normalize


class FolderSorter:
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        if not (self.folder_path.exists() and self.folder_path.is_dir()):
            raise ValueError("Specified folder not found.")

        self.file_types = {"images":        {"file_ext": (".JPEG", ".PNG", ".JPG", ".SVG"), "file_list": []},
                           "video":         {"file_ext": (".AVI", ".MP4", ".MOV", ".MKV"), "file_list": []},
                           "documents":     {"file_ext": (".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX"),
                                             "file_list": []},
                           "audio":         {"file_ext": (".MP3", ".OGG", ".WAV", ".AMR"), "file_list": []},
                           "archives":      {"file_ext": (".ZIP", ".GZ", ".TAR"), "file_list": []},
                           "unknown_files": {"file_ext": (), "file_list": []}}

        self.file_ext_links = {file_ext: folder for folder, params in self.file_types.items()
                               for file_ext in params["file_ext"]}

        self.known_file_extensions = set()
        self.unknown_file_extensions = set()

    def known_files_sorting(self, file: Path, destination_folder: str):
        try:
            self.known_file_extensions.add(file.suffix.replace(".", ""))
            file.replace(Path(self.folder_path, destination_folder, normalize(file.stem) + file.suffix))
            self.file_types[destination_folder]["file_list"].append(file.name)
        except OSError as err:
            raise ValueError(f"Error:\n{err}")

    def unknown_files_sorting(self, file: Path, destination_folder: str):
        try:
            self.unknown_file_extensions.add(file.suffix.replace(".", ""))
            file.replace(Path(self.folder_path, destination_folder, file.name))
            self.file_types[destination_folder]["file_list"].append(file.name)
        except OSError as err:
            raise ValueError(f"Error:\n{err}")

    def file_action(self, file: Path):
        folder_name = self.file_ext_links.get(file.suffix.upper(), "unknown_files")
        if folder_name == "unknown_files":
            self.unknown_files_sorting(file, folder_name)
        else:
            self.known_files_sorting(file, folder_name)

    def create_folders(self):
        try:
            for folder in self.file_types.keys():
                Path(self.folder_path, folder).mkdir(exist_ok=True)
        except OSError as err:
            raise ValueError(f"An error occurred when creating folders:\n{err}")

    def folder_sorting(self, path_dir: Path = None):
        if not path_dir:
            path_dir = self.folder_path
        for item in path_dir.iterdir():
            if item.is_dir():
                if item.name not in self.file_types.keys():
                    self.folder_sorting(item)
            else:
                self.file_action(item)
        if self.is_folder_empty(path_dir):
            path_dir.rmdir()
        else:
            if self.is_wrong_folder_name(path_dir.name):
                path_dir.rename(Path(path_dir.parent, normalize(path_dir.name)))

    def result_sorting(self) -> list:
        result = []
        for key, value in sorted(self.file_types.items()):
            if len(value["file_list"]):
                result.append([key, ", ".join(value["file_list"])])
        return result

    @staticmethod
    def is_wrong_folder_name(folder_name: str) -> bool:
        return bool(re.search(r"[^0-9a-zA-Z_]", folder_name))

    @staticmethod
    def is_folder_empty(path_dir: Path) -> bool:
        return not (any(path_dir.iterdir()))


if __name__ == '__main__':
    sorter = FolderSorter(r"f:\PythonPrj\Test_Opachki")
    sorter.create_folders()
    sorter.folder_sorting()
