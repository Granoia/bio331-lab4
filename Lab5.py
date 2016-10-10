## Lab 5
from __future__ import print_function
import graphspace_utils, json_utils
from optparse import OptionParser
import itertools
import random
import sys
import copy


def main(edgefile,motif_type,numrandgraphs,numrewires,username,password):
    nodes,edges = read_edges(edgefile)
    
    ## WRITE YOUR FUNCTION CALLS HERE

    node_ls, edge_ls = read_edges(edgefile)
    adj_ls = make_adj_ls(node_ls,edge_ls)
    initial_counts, big_counts = do_everything(edge_ls, adj_ls, numrandgraphs, numrewires)
    ps = compute_p(initial_counts, big_counts)
    print(ps)
    #post_graph(node_ls,edge_ls,'test',username,password,'desc')
    
    ## (you can comment out the line below while developing your methods)
    for k in ps:
        post_graph(node_ls,edge_ls,k,username,password,"p-value is: " + str(ps[k]))

    return ## done with main function

## WRITE YOUR FUNCTION DEFINITIONS HERE

def make_adj_ls(nodes, edges):
    d = {}
    for n in nodes:
        d[n] = []

    for e in edges:
        d[e[0]].append(e[1])

    return d



def find_motifs(adj_ls):
    auto = set()
    FFL = set()
    FBL = set()

    #find all the autoregulatory motifs
    for n in adj_ls:
        if n in adj_ls[n]:
            auto.add(n)


    #now find the Feed Forward Loop and Feedback Loop motifs
    for n in adj_ls:
        for neighbor in adj_ls[n]:
            if not(n in adj_ls[neighbor]):
                for n2 in adj_ls[neighbor]:
                    if not(neighbor in adj_ls[n]):
                        if n in adj_ls[n2] and not (n2 in adj_ls[n]):
                            FBL.add(frozenset([n,neighbor,n2]))

                        elif n2 in adj_ls[n] and not (n in adj_ls[n2]):
                            FFL.add(frozenset([n,neighbor,n2]))

    counts = {}
    counts["SELF"] = len(auto)
    counts["FFL"] = len(FFL)
    counts["FBL"] = len(FBL)
    
    return counts


def scramble_graph(edge_ls, adj_ls, numrewires):
    i = 0
    while i < numrewires:
        e1 = random.choice(edge_ls)
        e2 = random.choice(edge_ls)

        if (e1[1] in adj_ls[e2[0]]) or (e2[1] in adj_ls[e1[0]]):
            pass
        else:
            rewire(e1,e2,edge_ls, adj_ls)
            i += 1

    return edge_ls, adj_ls

def rewire(e1,e2,edge_ls,adj_ls):
    new1 = (e1[0],e2[1])
    new2 = (e2[0],e1[1])

    edge_ls.remove(e1)
    edge_ls.remove(e2)
    edge_ls.append(new1)
    edge_ls.append(new2)

    adj_ls[e1[0]].remove(e1[1])
    adj_ls[e2[0]].remove(e2[1])
    adj_ls[e1[0]].append(e2[1])
    adj_ls[e2[0]].append(e1[1])



def do_everything(edge_ls, adj_ls, numrandgraphs, numrewires):
    initial_counts = find_motifs(adj_ls)
    initial_graph = (copy.copy(edge_ls), copy.deepcopy(adj_ls))
    big_counts = {}
    big_counts["SELF"] = []
    big_counts["FFL"] = []
    big_counts["FBL"] = []

    for i in range(numrandgraphs):
        newgraph = copy.deepcopy(initial_graph)
        scramble_graph(newgraph[0],newgraph[1],numrewires)
        counts = find_motifs(newgraph[1])
        for k,v in counts.items():
            big_counts[k].append(v)

    return initial_counts, big_counts
        

def compute_p(initial_counts, big_counts):
    ps = {}
    ps["SELF"] = 1.0
    ps["FFL"] = 1.0
    ps["FBL"] = 1.0
    for k in ps:
        num_k_motifs = initial_counts[k]
        i = 0  #counts number of times the randomized graph has num_motifs >= initial graph num_motifs
        for c in big_counts[k]:
            if c >= num_k_motifs:
                i += 1
        k_motifs_p = i/float(len(big_counts[k]))
        ps[k] = k_motifs_p

    return ps
        
            


############## Functions written by Anna

def read_edges(infile):
    """
    Reads an edge file with a delimiter
    """
    nodes = set()
    edges = []
    with open(infile) as fin:
        for line in fin:
            row = line.strip('\n').split('\t')
            nodes.add(row[0])
            nodes.add(row[1])
            edges.append((row[0],row[1]))
    print(len(nodes),'nodes and',len(edges),'edges')
    return nodes,edges




def rgb_to_hex(red,green,blue):
    """
    values between 0 and 1
    """
    return '#{:02x}{:02x}{:02x}'.format(int(red*255),int(green*255),int(blue*255))

def post_graph(nodes,edges,graphid,username,password,d="Lab 5"):
    """
    Gets attributes of graph and posts it to GS.
    """
    nodeAttrs,edgeAttrs = getAttributes(nodes,edges)
    data = json_utils.make_json_data(nodes,edges,nodeAttrs,edgeAttrs, \
        title="Lab5 "+graphid,description=d,tags=['Lab5'])
    json_utils.write_json(data,graphid+'.json')
    graphspace_utils.postGraph(graphid,graphid+'.json',username,password)
    return

def getAttributes(nodes,edges):
    """
    Gets attributes of both nodes and (directed) edges.
    Feel free to modify.
    """

    nodeAttrs = {}
    for name in nodes:
        nodeAttrs[name] = {}
        nodeAttrs[name]['content'] = name
        nodeAttrs[name]['background_color'] = rgb_to_hex(0.9,0.4,0.4)
        nodeAttrs[name]['border_color'] = 'black'
        nodeAttrs[name]['border_width'] = 1
        nodeAttrs[name]['height'] = 50
        nodeAttrs[name]['width'] = 50

    edgeAttrs = {}
    for e in edges:
        node1 = e[0]
        node2 = e[1]
        if node1 not in edgeAttrs:
            edgeAttrs[node1] = {}
        edgeAttrs[node1][node2] = {}
        edgeAttrs[node1][node2]['target_arrow_shape'] = 'triangle'
        edgeAttrs[node1][node2]['target_arrow_fill'] = 'filled'
        edgeAttrs[node1][node2]['target_arrow_color'] = 'black'

    return nodeAttrs,edgeAttrs


######## Parse input arguments.
if __name__ == '__main__':
    ## create parser
    usageStr = 'python Lab5.py [options] <EDGE_FILE> <GRAPHSPACE_NAME> <GRAPHSPACE_PASSWORD>'
    parser = OptionParser(usage=usageStr)

    ## add options
    parser.add_option('-m','--motif',type='string',default='SELF',metavar='STR',\
        help='Motif Type: one of SELF, FFL, or FBL.  Default=SELF.')
    parser.add_option('','--numrandgraphs',type='int',default=10,metavar='INT',\
        help='Number of random graphs to generate. Default=10.')
    parser.add_option('','--numrewires',type='int',default=10,metavar='INT',\
        help='Number of rewirings per random graph. Default=10.')

    # parse the command line arguments
    (opts, args) = parser.parse_args()
    if len(args) != 3:
        parser.print_help()
        sys.exit('\nERROR: required arguments <EDGE_FILE> <GRAPHSPACE_NAME> <GRAPHSPACE_PASSWORD> are missing.')

    edgefile = args[0]
    username = args[1]
    password = args[2]

    ## Quit if motif is not what we expect.    
    if opts.motif not in ['SELF','FFL','FBL']:
        sys.exit('ERROR: motif must be one of SELF, FFL, or FBL. Exiting.')

    ## Run the main function.
    main(edgefile,opts.motif,opts.numrandgraphs,opts.numrewires,username,password)
