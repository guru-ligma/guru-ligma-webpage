import csv
import json
import secrets
import os
import shutil
from typing import List, Dict, Tuple, Sequence, Generator, Set, Optional, Any, Callable, Union
import zipfile

root = os.path.dirname(os.path.abspath(__file__))

id_file = os.path.join(root, "ids.json")
data_file = os.path.join(root, "data.csv")
import_dir = os.path.join(root, "import")
import_data_file = os.path.join(import_dir, "data.csv")
import_data_dir = os.path.join(import_dir, "data")
output_data_dir = os.path.join(root, "data")
import_zips_dir = os.path.join(root, "import-zips")
id_size = 16
id_data = {"id_list": [], "id_size": id_size}

if not os.path.exists(id_file):
    with open(id_file, "w") as f:
        json.dump(fp=f, obj=id_data, indent=True)
try:
    with open(id_file, "r") as f:
        id_data = json.load(f)
        id_size = id_data["id_size"]
except json.JSONDecodeError:
    with open(id_file, "w") as f:
        json.dump(fp=f, obj={"id_list": [], "id_size": id_size}, indent=True)
        id_data = {"id_list": {}, "id_size": id_size}


def read_csv_in(file: str) -> Generator[Dict[str, str], None, None]:
    with open(import_data_file) as f:
        for line in csv.DictReader(f):
            if not existance_test(line["creation_id"]):
                data = {
                    "creation_id": line["creation_id"],
                    "filename": line["filename"],
                    "created_at": line["created_at"],
                    "prog_id": get_id()
                }
                yield data


def extract_temp_files_from_zip(zfp: str) -> None:
    z = zipfile.ZipFile(zfp)
    for file in z.namelist():
        if file.startswith("data/"):
            z.extract(file, import_dir)
        else:
            z.extract(file, import_dir)
    


def move_img(file_in: str, file_out: str) -> None:
    # os.rename(file_in, file_out)
    shutil.move(file_in, file_out)


def get_id() -> str:
    _id = secrets.token_hex(id_size)
    while _id in id_data["id_list"]:
        _id = secrets.token_hex(id_size)
    id_data["id_list"].append(_id)
    with open(id_file, "w") as f:
        json.dump(id_data, f)
    return _id


def existance_test(creation_id: str) -> bool:
    with open(data_file) as f:
        for line in csv.DictReader(f):
            if creation_id == line["creation_id"]:
                return True
        return False


def update_data() -> None:
    with open(data_file) as f:
        data = list(csv.DictReader(f))
    for line in read_csv_in(import_data_file):
        in_file = os.path.join(import_data_dir, line["filename"])
        out_file = os.path.join(output_data_dir, line["filename"])
        move_img(in_file, out_file)
        data.append(line)
    os.remove(import_data_file)
    with open(data_file, "w") as f:
        fieldnames = ["creation_id", "filename", "created_at", "prog_id"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for line in data:
            writer.writerow(line)

if __name__ == "__main__":
    for roots, dirs, files in os.walk(import_zips_dir):
        for file in files:
            try:
                extract_temp_files_from_zip(os.path.join(roots, file))
                update_data()
            except Exception as e:
                pass