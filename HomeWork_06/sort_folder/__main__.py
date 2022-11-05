from sort_folder.main import main

try:
    main()
    print("Done.")
except ValueError as err:
    print(str(err))
