import datetime as dt
from tqdm import tqdm
import os
import json
import csv
import shutil
import pickle
import secrets
from typing import List, Dict, Tuple, Sequence,  Set, Optional, Any, Callable, Union

root = os.path.dirname(os.path.abspath(__file__))
used_id_file = "id_file.pkl"
data_file_in = os.path.join(root, "data.csv")
data_in = os.path.join(root, "data")
data_out_file = os.path.join(root, "loaded_files.pkl")
try:
    with open(data_out_file, "rb") as f:
        loaded_files = pickle.load(f)
except:
    loaded_files = {}

try:
    with open(used_id_file, "rb") as f:
        id_data = pickle.loads(f)
except:    
    id_data = {"used_ids": []}


def save_file(new_data: dict) -> None: 
    with open(data_out_file, "wb") as f:
        key = new_data["filename"]
        loaded_files[key] = new_data
        pickle.dump(file=f, obj=loaded_files)

PagesStructure = List[List[List[Dict[str, str]]]]


def get_id() -> str:
    cur_id = secrets.token_hex(16)
    while True:
        if cur_id not in id_data["used_ids"]:
            break
        cur_id = secrets.token_hex(16)
    id_data["used_ids"].append(cur_id)
    with open(used_id_file, "wb") as f:
        pickle.dump(file=f, obj=id_data)
    return cur_id


def load_csv(file: str) -> PagesStructure:
    output = []
    with open(file) as in_f:
        csv_reader = list(csv.DictReader(in_f))
        csv_reader = sorted(csv_reader, key=lambda x: x["created_at"])
    runs = 0
    tempa = []
    tempb = []
    counta, countb = 0, 0
    for line in tqdm(csv_reader):
        if line["filename"] in loaded_files.keys():
            new_line = loaded_files[line["filename"]]
        else:
            new_line = {
                "filename": line["filename"],
                "created_at": line["created_at"],
                "id": get_id()
            }
            save_file(new_line)
        tempa.append(new_line)
        counta += 1
        countb += 1
        runs += 1
        if counta >= 2:
            tempb.append(tempa)
            tempa = []
            counta = 0
        if countb >= 50:
            output.append(tempb)
            tempb = []
            countb = 0
    if counta != 0:
        tempb.append(tempa)
    if not tempb:
        output.append(tempb)
    return output


def gen_home_html(page_len: int) -> None:
    html_file = "catalog-page"
    if page_len <= 0:
        raise ValueError
    with open("cataloghome-base-0.html") as f:
        output = f.read()
    with open("cataloghome-base-1.html") as f:
        end = f.read()
    output = f"""{output}
    <div class="contaier-lg my-5 justify-content-between text-center">
        <div class="row justify-content-between text-center">
            <div class="col-md-12 col-lg-1 col-xl-1 justify-content-between></div>"""
    step = 0
    for i in range(page_len):
        output = f"""{output}
            <div class="col-md-12 col-lg-1 col-xl-1 justify-content-between text-center">
                <a href="catalog-pages/{html_file}-{i}.html" class="btn btn-primary">Catalog Page {i}</a>
            </div>"""
        step += 1
        if step == 5:
            output = f"""{output}
            <div class="col-md-12 col-lg-1 col-xl-1 justify-content-between></div>
        </div>
        <div class="row justify-content-between text-center">
            <div class="col-md-12 col-lg-1 col-xl-1 justify-content-between></div>"""
            step = 0
    output = f"""{output}
            <div class="col-md-12 col-lg-1 col-xl-1 justify-content-between></div></div>
        {end}"""

    with open("catalog-home.html", "w") as f:
        f.write(output)


def gen_page_html(pages: PagesStructure) -> int:
    html_file = "catalog-page"
    len_pages = len(pages)
    for index, z_img in enumerate(pages):
        output = ""
        with open("./pages-base-0.html") as f:
            output = f.read()
        with open("./pages-base-1.html") as f:
            output = f"{output}{index}{f.read()}"
        with open("./pages-base-2.html") as f:
            output = f"{output}{index}{f.read()}"
        with open("./pages-base-3.html") as f:
            end = f.read()
        with open(f"catalog-pages/{html_file}-{index}.html", "w") as f:
            output = f"""{output}
            <div class="contaier-lg my-5 justify-content-between text-center">
                <div class="row justify-content-between text-center">
                    <div class=col-2 justify-content-between></div>"""
            if index != 0:
                output = f"""{output}
                    <div class="col-md-12 col-lg-2 col-xl-1 justify-content-between text-center">
                        <a href="../catalog-pages/{html_file}-{index-1}.html" class="btn btn-primary">Previous Page</a>
                    </div>"""
            output = f"""{output}
                    <div class="col-md-12 col-lg-2 col-xl-1 justify-content-between text-center">
                        <a href="../catalog-home.html" class="btn btn-primary">Catalog Home</a>
                    </div>"""
            if index != len_pages:
                output = f"""{output}
                    <div class="col-md-12 col-lg-2 col-xl-1 justify-content-between text-center">
                        <a href="../catalog-pages/{html_file}-{index+1}.html" class="btn btn-primary">Next Page</a>
                    </div>"""
            output = f"""{output}
                    <div class=col-2 justify-content-between></div>
                </div>
            </div>
        </div>"""
            output = f"""{output}
        <div class="container-fluid my-1">"""
            for imgs in z_img:
                output = f"""{output}
            <div class="row justify-content-between text-center">
                <div class=col-2 justify-content-between></div>"""
                for _img in imgs:
                    img_id = _img["id"]
                    img_file = _img["filename"]
                    output = f"""{output}
                <div class="m-5 col-md-12 col-lg-2 col-xl-2 justify-content-between text-center">
                    <table class="align-middle">
                        <thead>
                            <tr>
                                <th> {img_id} </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><img class="img-fluid align-center" src="../data/{img_file}" alt="{img_id}"></td>
                            </tr>
                        </tbody>
                    </table>
                    <p><hr class="border-2 border-top border-dark bg-dark"/></p>
                </div>
                <div class=col-2 justify-content-between></div>"""
                output = f"""{output}
            </div>"""
            output = f"""{output}
            <div class="contaier-lg my-5 justify-content-between text-center">
                <div class="row justify-content-between text-center">
                    <div class=col-2 justify-content-between></div>"""
            if index != 0:
                output = f"""{output}
                    <div class="col-md-12 col-lg-2 col-xl-1 justify-content-between text-center">
                        <a href="../catalog-pages/{html_file}-{index-1}.html" class="btn btn-primary">Previous Page</a>
                    </div>"""
            output = f"""{output}
                    <div class="col-md-12 col-lg-2 col-xl-1 justify-content-between text-center">
                        <a href="../catalog-home.html" class="btn btn-primary">Catalog Home</a>
                    </div>"""
            if index != len_pages:
                output = f"""{output}
                    <div class="col-md-12 col-lg-2 col-xl-1 justify-content-between text-center">
                        <a href="../catalog-pages/{html_file}-{index+1}.html" class="btn btn-primary">Next Page</a>
                    </div>"""
            output = f"""{output}
                    <div class=col-2 justify-content-between></div>
                </div>
            </div>
        </div>"""
            output = f"""{output}
    {end}"""
            f.write(output)
    return len_pages

if __name__ == "__main__":
    gen_home_html(gen_page_html(load_csv(data_file_in)))