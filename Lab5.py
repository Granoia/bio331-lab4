## Lab 5
from __future__ import print_function
import graphspace_utils, json_utils
from optparse import OptionParser
import itertools
import random
import sys


def main(edgefile,motif_type,numrandgraphs,numrewires,username,password):
    nodes,edges = read_edges(edgefile)
    
    ## WRITE YOUR FUNCTION CALLS HERE

    ## (you can comment out the line below while developing your methods)
    post_graph(nodes,edges,motif_type,username,password)

    return ## done with main function

## WRITE YOUR FUNCTION DEFINITIONS HERE

############## Functions written by Anna

def read_edges(infile):
    """
    Reads an edge file with a delimiter
    """
    nodes = set()
    edges = []
    with open(infile) as fin:
        for line in fin:
            row = line.strip().split(';')
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

def post_graph(nodes,edges,graphid,username,password):
    """
    Gets attributes of graph and posts it to GS.
    """
    nodeAttrs,edgeAttrs = getAttributes(nodes,edges)
    data = json_utils.make_json_data(nodes,edges,nodeAttrs,edgeAttrs, \
        title="Lab5 "+graphid,description="Lab5",tags=['Lab5'])
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