import networkx as nx
import numpy as np

def load_data(ds_name, use_node_labels, use_node_attributes):
    node2graph = {}
    Gs = []
    
    with open("datasets/%s/%s_graph_indicator.txt"%(ds_name,ds_name), "r") as f:
        c = 1
        for line in f:
            node2graph[c] = int(line[:-1])
            if not node2graph[c] == len(Gs):
                Gs.append(nx.Graph())
            Gs[-1].add_node(c)
            c += 1
    
    with open("datasets/%s/%s_A.txt"%(ds_name,ds_name), "r") as f:
        for line in f:
            edge = line[:-1].split(",")
            edge[1] = edge[1].replace(" ", "")
            Gs[node2graph[int(edge[0])]-1].add_edge(int(edge[0]), int(edge[1]))
    
    if use_node_labels:
        d = {}
        with open("datasets/%s/%s_node_labels.txt"%(ds_name,ds_name), "r") as f:
            c = 1
            for line in f:
                node_label = int(line[:-1])
                if node_label not in d:
                    d[node_label] = len(d)
                Gs[node2graph[c]-1].node[c]['label'] = node_label
                c += 1

        for G in Gs:
            for node in G.nodes():
                node_label_one_hot = np.zeros(len(d))
                node_label_one_hot[d[G.node[node]['label']]] = 1
                G.node[node]['label'] = node_label_one_hot

    if use_node_attributes:
        with open("datasets/%s/%s_node_attributes.txt"%(ds_name,ds_name), "r") as f:
            c = 1
            for line in f:
                node_attributes = line[:-1].split(',')
                node_attributes = [float(attribute) for attribute in node_attributes]
                Gs[node2graph[c]-1].node[c]['attributes'] = np.array(node_attributes)
                c += 1

    if (not use_node_attributes) and (not use_node_labels):
        for G in Gs:
            for node in G.nodes():
                G.node[node]['attributes'] = np.array(G.degree(node))

    class_labels = []
    with open("datasets/%s/%s_graph_labels.txt"%(ds_name,ds_name), "r") as f:
        for line in f:
            class_labels.append(int(line[:-1]))
    
    class_labels  = np.array(class_labels, dtype=np.float)
    return Gs, class_labels