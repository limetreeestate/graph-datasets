# DBLP.v11 Citation Graph
This dataset is a directed dataset of paper citations formed from the original dblp.v11 citation dataset available at https://www.aminer.org/citation. The datafiel consist of an edgelist and an attribute file of papers

#### Edgelist
The edgelist is a text file archived and split into segments in citation_edgelist folder and  follows the structure `<paper 1 id> <paper 2 id>` where paper 1 has paper 2 in its references. Edges are directed

#### Attribute
The attribute data is in a text file archived and split into segments in citation_attr folder. The text data has the structure in each line as follows: `<paper 1 id> <feature 1 value> ... <feature n value>`. Here, `feature 1` is the number of citations the paper has and the rest of the values are the weight that paper has towards a particular field of study (fos). These fos are mentioned in the file citation_selected_attr.txt where the features follow the same order in the attribute file after `feature 1`.

