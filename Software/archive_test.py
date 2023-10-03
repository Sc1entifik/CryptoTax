from pathlib import Path
import pytest
import csv

from archive import Archive

@pytest.fixture
def archive_object():
    tax_archive = Archive()
    return tax_archive


def generate_testfiles():
    header = ["Crypto", "Amount", "Tx Type"]
    data_rows = [("BTC", .03, "Swap"), ("ETH", .04, "Bridge"), ("BNB", 2, "Swap")]
    num_testfiles = len(data_rows)

    for row in data_rows:
        test_file_path = f"./Tax/TestOutputs/{row[0]}.csv"

        with open(test_file_path, "w") as output_file:
            output_csv = csv.writer(output_file)
            output_csv.writerow(header)
            output_csv.writerows(data_rows)

    return num_testfiles


def delete_old_testfiles():
    path = Path(Archive.test_path)

    if not path.is_dir():
        path.mkdir()
    
    for file in path.iterdir():
        if file.is_file():
            file.unlink()


def test_archive_taxfiles(archive_object):
    delete_old_testfiles()
    assert len(tuple(Path(Archive.test_path).iterdir())) == 0 
    num_testfiles = generate_testfiles()
    archive_object.archive_tax_files("Test")
    assert len(tuple(Path(Archive.test_path).iterdir())) == num_testfiles




