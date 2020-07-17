import csv
import orjson
import gc
from sys import argv


def selected_paper_fos(t=0.003):
    count = 0
    fos = dict()
    print("Threshold:", t)
    with open("dblp.v11/dblp_papers_v11.txt", "r") as dblp_file:
        print("File opened")
        N = 4107341
        print(N)
        for line in dblp_file:
            paper_dict = orjson.loads(line)

            try:
                fields = paper_dict["fos"] #[(item["name"].replace('"', ""), item["w"]) for item in paper_dict["fos"]]
            except KeyError:
                # fos key missing in data
                continue

            del paper_dict
            # Increment the no of appearencs count / no of papers in dataset
            for f in fields:
                field, weight = f.values()
                if float(weight) > 0.5:
                    try:
                        fos[field] += 1 / N# Around N papers in graph
                    except KeyError:
                        # Key not in  dict, therefore should be added
                        fos[field] = 1 / N

            if count % 100000 == 0:
                # print(len(filtered_items), len(items))
                gc.collect()

                print(count)
            count += 1

    # Filter out fields that appear less a certain frequency
    filtered_fos = list(filter(lambda x: x[1] > t, fos.items()))  # 0.0015 :- 804, 948 in prev year, 0.0004 - 1842
    print("Filtering done", len(filtered_fos), len(fos))
    print("Writing fos")
    with open(f"dblp.v11/citation_selected_attr.txt", "w", newline='') as co_author_partial_attr_file:
        writer = csv.writer(co_author_partial_attr_file, delimiter=" ")
        for f in filtered_fos:
            writer.writerow(f)


if __name__ == "__main__":
    if len(argv) > 1:
        threshold = float(argv[1])
        selected_paper_fos(threshold)
    else:
        selected_paper_fos()
