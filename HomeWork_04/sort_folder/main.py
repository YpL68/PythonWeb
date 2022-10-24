import argparse
from sort_folder.folder_sort import FolderSorter


def main():
    parser = argparse.ArgumentParser(description='Sorting folder')
    parser.add_argument("--source", "-s", help="Source folder", required=True)

    args = vars(parser.parse_args())

    source_folder = args.get("source")

    sorter = FolderSorter(source_folder)
    sorter.run()


if __name__ == '__main__':
    try:
        main()
        print("Done.")
    except ValueError as err:
        print(str(err))
