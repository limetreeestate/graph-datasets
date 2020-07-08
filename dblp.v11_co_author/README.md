# DBLP.v11 Co Author Graph

This dataset is an undirected graph dataset of co-authors (Authors who have written a paper together) extracted from the original dblp.v11 citation dataset available at https://www.aminer.org/citation. The data files consist of an edgelist as well as an attribute file of the authors.

#### Edgelist
The edgelist is a text file archived in co_author_edgelist folder, where the unpacked file following the structure `<author 1 id> <author 2 id>` where author 1 and author 2 are co-authors. The edges are undirected.

#### Attribute
The attribute data is in a text file archived and segmented in co_author_attr folder, where each line in the unpacked file follows the structure of `<author id> <feature 1 value> <feature 2 value> .... <feature n value>`. Here, `feature 1` is the number of citations the author has and the rest of the values are the weight an author has towards a particular field of study (fos). These fos are mentioned in the file co_author_selected_attr.txt where the features follow the same order in the attribute file after `feature 1`.
