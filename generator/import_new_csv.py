import csv
import json
import secrets
import os
import shutil
from typing import List, Dict, Tuple, Sequence, Generator, Set, Optional, Any, Callable, Union
import atexit

root = os.path.dirname(os.path.abspath(__file__))

id_file = os.path.join(root, "ids.json")
data_file = os.path.join(root, "data.csv")
import_dir = os.path.join(root, "import")
import_data_file = os.path.join(import_dir, "data.csv")
import_data_dir = os.path.join(import_dir, "data")
output_data_dir = os.path.join(root, "data")
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
<<<<<<< Updated upstream
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
=======
        id_data = {"id_list": [], "id_size": id_size}


def read_csv_in(file: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and returns a list of dictionaries representing the data.

    Parameters:
    - file (str): The path to the CSV file.

    Returns:
    - List[Dict[str, str]]: A list of dictionaries, where each dictionary represents a row in the CSV file. The keys of the dictionaries are the column names in the CSV file, and the values are the corresponding values in each row.

    Example:
    data = read_csv_in("data.csv")
    for row in data:
        print(row["creation_id"], row["filename"], row["created_at"], row["prog_id"])
"""
    output = []
    with open(file) as f:
        for line in csv.DictReader(f):
            data = {
                "creation_id": line["creation_id"],
                "filename": line["filename"],
                "created_at": line["created_at"],
                "prog_id": get_id()
            }
            output.append(data)
    yield from output


def move_img(file_in: str, file_out: str) -> None:
    os.rename(file_in, file_out)


def store_id(id: str) -> None:
    id_data["id_list"].append(id)

def get_id() -> str:
    """
    Generate a unique ID.

    Returns:
        str: A unique ID.

"""
    global id_size, id_data
    _id = secrets.token_hex(id_size)
    while _id in id_data["id_list"]:
        _id = secrets.token_hex(id_size)
    id_data["id_list"].add(_id)
    store_id(_id)
>>>>>>> Stashed changes
    return _id


def existance_test(creation_id: str) -> bool:
<<<<<<< Updated upstream
=======
    """
    Reads a CSV file and returns a list of dictionaries representing the data.

    Parameters:
    - file (str): The path to the CSV file.

    Returns:
    - List[Dict[str, str]]: A list of dictionaries, where each dictionary represents a row in the CSV file. The keys of the dictionaries are the column names in the CSV file, and the values are the corresponding values in each row.

    Example:
    data = read_csv_in("data.csv")
    for row in data:
        print(row["creation_id"], row["filename"], row["created_at"], row["prog_id"])

"""
>>>>>>> Stashed changes
    with open(data_file) as f:
        for line in csv.DictReader(f):
            if creation_id == line["creation_id"]:
                return True
        return False


<<<<<<< Updated upstream
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
    update_data()
=======
atexit.register
def exit_handler():
    with open(id_file, "w") as f:
        json.dump(fp=f, obj=id_data)
>>>>>>> Stashed changes
