from Graph import Graph
from girvannewman import girvannewman
import os
from random import randint, random


def random_graph(nb_communities : int, nb_vertices : int, e : float = 0.80, k :float = 0.20, additional_name: str|None = None):
    """
    Function to create a random graph with a determined number of communities and vertices. 
    e and k are parameters for the probability to have an edge between vertices. Returns the graph created and the communities.
    Args :
        nb_communities : Number of communities desired in the graph.
        nb_vertices : Number of vertices desired in the graph.
        e : Probility of an edge between two vertices of the same community. Default : 0.8
        k : Probability of an edge between two vertices in different communities. Default : 0.2
    """
    if nb_communities > nb_vertices :
        raise ValueError("The number of communities is superior to the number of vertices")

    name = f"RandomGraph_c={nb_communities}_v={nb_vertices}_e={e}_k={k}{'_'+additional_name if additional_name else ''}"
    graph = Graph(name)
    communities = {x :[] for x in range(1,(nb_communities+1))}
    i = 0
    while i<nb_vertices:
        graph.add_vertex(str(i))
        key = randint(1,nb_communities)
        communities[key].append(str(i))
        i += 1
    
    for l in communities.keys():
        # We ensure each community has at least 1 vertex, else we re-generate a random graph
        if len(communities[l]) == 0:
            return random_graph(nb_communities, nb_vertices,e,k)
        else :
            for v in communities[l]:
                for v2 in communities[l] :
                    p = random()
                    if p < e and v != v2:
                        graph.add_edge(v,v2)

    for l in communities.keys():
        for l2 in communities.keys():
            if l < l2 :
                for v in communities[l]:
                    for v2 in communities[l2]:
                        p = random()
                        if p < k :
                            graph.add_edge(v,v2)

    return graph, communities

def compute_precision_recall(communities: list | dict, expected_communities: list | dict):
    """
    Computes precision and recall for community detection
    Uses a greedy algorithm to match communities based on Jaccard Similarity

    Args:
        communities: Detected communities
        expected_communities: Known valid communities

    Returns:
        precision and recall
    """
    if isinstance(communities, list):
        communities = {i: set(v) for i, v in enumerate(communities)}
    else:
        communities = {k: set(v) for k, v in communities.items()}

    if isinstance(expected_communities, list):
        expected_communities = {i: set(v) for i, v in enumerate(expected_communities)}
    else:
        expected_communities = {k: set(v) for k, v in expected_communities.items()}

    def jaccard_similarity(c, ec):
        union = len(c.union(ec))
        return len(c.intersection(ec)) / union if union > 0 else 0.0

    # Greedy matching
    all_scores = {(c, ec): jaccard_similarity(communities[c], expected_communities[ec])
                  for c in communities for ec in expected_communities}

    matched_detected = set()
    matched_expected = set()
    correct = invalid = missed = 0

    while all_scores:
        (c, ec), _ = max(all_scores.items(), key=lambda x: x[1])
        detected = communities[c]
        expected = expected_communities[ec]

        correct += len(detected & expected)
        invalid += len(detected - expected)
        missed += len(expected - detected)

        matched_detected.add(c)
        matched_expected.add(ec)
        all_scores = {k: v for k, v in all_scores.items() if k[0] not in matched_detected and k[1] not in matched_expected}

    # Account for unmatched communities
    for c in communities:
        if c not in matched_detected:
            invalid += len(communities[c])
    for ec in expected_communities:
        if ec not in matched_expected:
            missed += len(expected_communities[ec])

    precision = correct / (correct + invalid) if (correct + invalid) > 0 else 0.0
    recall = correct / (correct + missed) if (correct + missed) > 0 else 0.0
    return precision, recall       


def test_method(method = "communities", 
    communities_range: tuple[int, int, int] = (2, 5, 1), 
    vertices_range: tuple[int, int, int] = (10, 50, 10), 
    e_range: tuple[int, int, int] = (80, 90, 10),
    k_range: tuple[int, int, int] = (10, 30, 10),
    n = 10
    ):
    """
    Test provided method on n random graphs generated with certain parameters, saves results in csv format for further analysis

    Args:
        The following parameters specify values in which generated graphs will range
         communities_range
         vertices_range
         e_range: requires int between 0 and 100, will be converted to correct percentage between 0 and 1
         k_range: requires int between 0 and 100, will be converted to correct percentage between 0 and 1

         n: number of random graphs to generate and test for each set of unique parameters
    """

    # we ensure method is one that can be tested using this function
    # dendogram cannot be tested as it makes all vertices their own community
    assert method in ("communities", "modularity"), "Provided method can only be communities or modularity"

    os.makedirs("./test", exist_ok=True)

    fname = f"./test/test_results_{'-'.join([str(x) for x in communities_range])}_{'-'.join([str(x) for x in vertices_range])}_{'-'.join([str(x) for x in e_range])}_{'-'.join([str(x) for x in k_range])}_{n}_{method}.csv"

    with open(fname, "w") as f:
        f.write("nb_communities,nb_vertices,e,k,avg_precision,avg_recall\n")
        for c in range(*communities_range):
            for v in range(*vertices_range):
                # using strange list building since range() doesnt accept float steps
                for e in [x/100.0 for x in range(*e_range)]:
                    for k in [y/100.0 for y in range(*k_range)]:
                        precision, recall = 0.0, 0.0

                        for _ in range(n):
                            graph, expected_communities = random_graph(c, v, e, k)

                            # here the c describes the number of expected communities, used by the function if the method is set to "communities"
                            if method == "communities":
                                detected_communities = girvannewman(graph, method, c)
                            else:
                                detected_communities, _ = girvannewman(graph, method, c)

                            p, r = compute_precision_recall(detected_communities, expected_communities)

                            precision += p
                            recall += r

                        precision /= n
                        recall /= n

                        f.write(f"{c},{v},{int(e*100)},{int(k*100)},{precision},{recall}\n")

    return fname


if __name__ == '__main__':
    test_method()