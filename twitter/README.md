# Twitter Graph Dataset

This is an directed graph dataset created from the original source dataset available at https://snap.stanford.edu/data/ego-Twitter.html. The files consist of an attribute file of one-hot encoded vectors as well as an edgelist file.

#### Edgelist
Edges follow the structure of `<user 1 id> <user 2 id>` where `user 1` follows `user 2` and their ids are space separated.

#### Attrinutes
Attribute files follow the structure of `<user id> <feature 1 value> ... <feature n value>` where features are space separated and are binary feature attributes extracted from the original ego dataset. There are 1007 attributes which are selected based on frequency of appearance and a predetermined threshold. 
