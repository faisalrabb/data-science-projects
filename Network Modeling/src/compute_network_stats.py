import json
import argparse
import os, sys
import networkx as nx


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',required=True, dest='i', help="input file path")
    parser.add_argument('-o', required=True, dest='o', help="output file path")
    args=parser.parse_args()
    if not os.path.dirname(args.o) == "":
        os.makedirs(os.path.dirname(args.o), exist_ok=True)
    output = get_interaction_network(args.i)
    with open(args.o, 'w') as o:
        json.dump(output, o)

def get_interaction_network(fpath):
    with open(fpath, 'r') as f: 
        interactions = json.load(f)
    result = {}
    result["most_connected_by_num"] = []
    result["most_connected_by_weight"] = []
    result["most_central_by_betweenness"] = []
    G = nx.Graph()
    for key, value in interactions.items():
        for k, v in value.items():
            G.add_edge(key,k,weight=v)
    sorted_degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)[:3]
    for (x,y) in sorted_degrees:
        result["most_connected_by_num"].append(x)
    sorted_weight = sorted(G.degree(weight="weight"), key=lambda x: x[1], reverse=True)[:3]
    for (x,y) in sorted_weight:
        result["most_connected_by_weight"].append(x)
    sorted_betweenness = sorted(nx.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:3]
    for (x,y) in sorted_betweenness:
        result["most_central_by_betweenness"].append(x)
    return result

if __name__=="__main__":
    main()
