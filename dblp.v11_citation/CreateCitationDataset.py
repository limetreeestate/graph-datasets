import orjson
import networkx
import csv
import json
import gc


# 36545646
# 36624464 new
def create_edges(pid, paper_dict):
    global paper_map
    paper_ids = {pid}

    if pid not in paper_map:
        paper_map[pid] = len(paper_map)
    paper_id = paper_map[pid]

    try:
        references = paper_dict["references"]
    except KeyError:
        return paper_id, [], []

    temp_ref_set = set()

    for ref_id in references:
        if ref_id not in paper_map:
            paper_map[ref_id] = len(paper_map)

        temp_ref_set.add(paper_map[ref_id])

    edges = [(paper_id, ref) for ref in temp_ref_set]

    return paper_id, temp_ref_set, edges


def get_feature_vector(selected_attr, attr, N):
    feature_attr = [0] * (N)
    # feature_attr[0] = attr["n_citation"]

    try:
        fields = {str(item[0]).replace('"', '').lower(): item[1] for item in attr["fos"]}
    except KeyError:
        # fos key missing in data
        return feature_attr

    # print(fields)

    # Increment the no of appearencs count / no of authors in the partial file
    for i in range(N):
        try:
            # Update with paper_id fos weight
            feature_attr[i] = fields[selected_attr[i]]
        except KeyError:
            # Author doesnt have field
            continue

    return feature_attr


def create_attr(paper_id, paper_dict, selected_attr, N):
    global paper_data
    try:
        fos = [list(item.values()) for item in paper_dict["fos"]]
    except KeyError:
        # Fos key missing in data
        fos = []

    try:
        citation_count = paper_dict["n_citation"]
    except KeyError:
        # n_citation key missing in data
        citation_count = 0

    attr = dict()

    attr["n_citation"] = citation_count
    if fos != []:
        attr["fos"] = fos

    paper_data[paper_id] = get_feature_vector(selected_attr, attr, N)

    del fos


def create_dataset():
    """
    Generates generates partial json files of the following formatnano
    {
        "<paper_id pid>" : {
            "<name>" : "<>"
            "<no of citations>" : <>
            "<fields of study>" : [["<>", <>],...]
        },...
    }
    :return:
    """
    global paper_data
    count = 1
    fos_missing_count = 0
    # full_data = dict()

    with open("dblp.v11/citation_selected_attr.txt", "r") as selected_attr_file:
        reader = csv.reader(selected_attr_file, delimiter=' ')
        selected_attr = [str(row[0]).replace('"', '').lower() for row in reader]

    N = len(selected_attr)
    print(N)

    G = networkx.DiGraph()

    with open("dblp.v11/dblp_papers_v11.txt", "r") as dblp_file:
        print("File opened")
        for line in dblp_file:
            paper_dict = orjson.loads(line)

            pid = paper_dict["id"]

            paper_id, references, edges = create_edges(pid, paper_dict)

            G.add_node(paper_id)
            G.add_nodes_from(references)
            G.add_edges_from(edges)

            create_attr(paper_id, paper_dict, selected_attr, N)

            if count % 100000 == 0:
                # output the current stored paper_id attributes into a json and clear memory
                gc.collect()
                print(count)

            count += 1

    E = G.edges()
    print("Writing edgelist", len(E))
    with open("dblp.v11/citation_edgelist.txt", "w", newline='') as co_author_edge_file:
        writer = csv.writer(co_author_edge_file, delimiter=" ")
        for edge in E:
            writer.writerow(edge)

    # output the last stored paper_id attributes into a json and clear memory
    print(count)
    paper_items = paper_data.items()

    # del paper_data
    print("Writing fos", len(paper_data[0]))  # 4107340
    with open(f"dblp.v11/citation_attr.txt", "w", newline='') as co_author_attr_file:
        writer = csv.writer(co_author_attr_file, delimiter=" ")
        for id, vector in paper_items:
            data = [id] + vector
            writer.writerow(data)
    del paper_items


if __name__ == "__main__":
    paper_data = dict()
    paper_map = dict()
    create_dataset()  # 3655052 11697041
