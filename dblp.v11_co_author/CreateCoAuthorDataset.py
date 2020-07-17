import orjson
import networkx
import csv
import json
import gc


def create_edges(author_ids):
    global author_map
    temp_author_set = set()

    for id in author_ids:
        if id not in author_map:
            author_map[id] = len(author_map)

        temp_author_set.add(author_map[id])

    edges = []

    for author_id in temp_author_set:
        author_relations = temp_author_set - {author_id}

        edges += [(author_id, co_author) for co_author in author_relations]

    return temp_author_set, edges


def get_feature_vector(selected_attr, author, attr, N):
    global author_data, author_set
    if author not in author_set:
        author_set.add(author)
        feature_attr = [0] * (N)
        # feature_attr[0] = attr["n_citation"]
    else:
        feature_attr = author_data[author]
        # feature_attr[0] += attr["n_citation"]

    try:
        fields = {item[0].lower(): item[1] for item in attr["fos"]}
    except KeyError:
        # fos key missing in data
        return feature_attr

    # Increment the no of appearencs count / no of authors in the partial file
    for i in range(N):
        try:
            # Update with author fos weight
            feature_attr[i] = max(feature_attr[i], fields[selected_attr[i]])
        except KeyError:
            # Author doesnt have field
            continue

    return feature_attr


def create_attr(authors, paper_dict, selected_attr, N):
    global author_data
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

    for author_id in authors:

        attr["n_citation"] = citation_count
        if fos != []:
            attr["fos"] = fos

        author_data[author_id] = get_feature_vector(selected_attr, author_id, attr, N)


def create_dataset():
    """
    Generates generates partial json files of the following format
    {
        "<author id>" : {
            "<name>" : "<>"
            "<no of citations>" : <>
            "<fields of study>" : [["<>", <>],...]
        },...
    }
    :return:nano
    """
    global author_data
    count = 1

    with open("dblp.v11/co_author_selected_attr.txt", "r") as selected_attr_file:
        reader = csv.reader(selected_attr_file, delimiter=' ')
        selected_attr = [str(row[0]).replace('"', '').lower() for row in reader]

    N = len(selected_attr)

    G = networkx.Graph()

    with open("dblp.v11/dblp_papers_v11.txt", "r") as dblp_file:
        print("File opened")
        for line in dblp_file:
            paper_dict = orjson.loads(line)

            authors_temp = set([tuple(item.values()) for item in paper_dict["authors"]])
            author_ids = set([list(author)[1] for author in authors_temp])

            authors, edges = create_edges(author_ids)

            G.add_nodes_from(authors)
            G.add_edges_from(edges)

            del authors_temp, author_ids

            create_attr(authors, paper_dict, selected_attr, N)

            if count % 100000 == 0:
                # output the current stored author attributes into a json and clear memory
                gc.collect()
                print(count)

            count += 1
            del authors, paper_dict

    E = G.edges()
    print("Writing edgelist", len(E))
    with open("dblp.v11/co_author_edgelist.txt", "w", newline='') as co_author_edge_file:
        writer = csv.writer(co_author_edge_file, delimiter=" ")
        for edge in E:
            writer.writerow(edge)

    del E

    # output the last stored author attributes into a json and clear memory
    print(count)
    author_items = author_data.items()

    del author_data
    print("Writing fos", len(author_items))
    with open(f"dblp.v11/co_author_attr.txt", "w", newline='') as co_author_attr_file:
        writer = csv.writer(co_author_attr_file, delimiter=" ")
        for id, vector in author_items:
            data = [id] + vector
            writer.writerow(data)
    del author_items


if __name__ == "__main__":
    author_data = dict()
    author_set = set([])
    author_map = dict()
    create_dataset() #3655052 11697041
