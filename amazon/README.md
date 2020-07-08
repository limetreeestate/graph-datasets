# Amazon Product Co-Purchasing Network Dataset

This is an directed graph dataset created from the original source dataset available at https://snap.stanford.edu/data/amazon-meta.html. The files consist of an attribute file of one-hot encoded vectors as well as an edgelist file.

#### Edgelist
Edges follow the structure of `<item 1 id> <item 2 id>` where users who bought `item 1` also bought `item 2`. Item ids are space separated in the edgelist.

#### Attrinutes
Attribute files follow the structure of `<item id> <feature 1 value> ... <feature n value>` where features are space separated and are binary feature attributes extracted from the original dataset. 
