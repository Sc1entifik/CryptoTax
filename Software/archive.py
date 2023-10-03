from pathlib import Path

class Archive:
    test_path = "./Archive/Test/"

    def archive_tax_files(self, destination_folder):
        archival_files = Path("./Tax/").glob("**/*.csv") if destination_folder != "Test" else Path("./Tax/TestOutputs/").glob("**/*.csv")
        destination = Path(f"./Archive/{destination_folder}/")

        if not destination.is_dir():
            destination.mkdir()

        for file in archival_files:
            if file.is_file():
                file.rename(destination / file.name)



        

