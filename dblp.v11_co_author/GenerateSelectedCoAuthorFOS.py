import csv
import json
import orjson
import os
import gc
from sys import argv

def selected_paper_fos(t = 0.003): #344
    count = 1
    fos = dict()
    with open("dblp.v11/dblp_papers_v11.txt", "r") as dblp_file:
        print("File opened")
        N = 4107341
        print(N)
        for line in dblp_file:
            paper_dict = orjson.loads(line)

            try:
                fields = [item["name"].replace('"', "") for item in paper_dict["fos"]]
            except(KeyError):
                # fos key missing in data
                continue

            del paper_dict
            # Increment the no of appearencs count / no of authors in the partial file
            for field in fields:
                try:
                    fos[field] += 1 / N  # Around N papers in graph
                except(KeyError):
                    fos[field] = 1 / N


            #Filter out fields that appear less a certain frequency

            if count % 100000 == 0:
                # output the current stored author attributes into a json and clear memory
                gc.collect()

                print(count)
            count += 1

    filtered_fos = list(filter(lambda x: x[1] > t, fos.items())) #0.0015 804
    print("Filtering done", len(filtered_fos), len(fos))
    print("Writing fos")
    with open(f"dblp.v11/co_author_selected_attr.txt", "w", newline='') as co_author_partial_attr_file:
        writer = csv.writer(co_author_partial_attr_file, delimiter=" ")
        for f in filtered_fos:
            writer.writerow(f)

if __name__ == "__main__":
    if len(argv) > 1:
        threshold = float(argv[1])
        selected_paper_fos(threshold)
    else:
        selected_paper_fos()



