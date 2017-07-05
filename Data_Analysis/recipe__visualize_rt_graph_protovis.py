# -*- coding: utf-8 -*-

import os
import sys
import json
import webbrowser
import twitter
from recipe__create_rt_graph import create_rt_graph
from recipe__oauth_login import oauth_login
from recipe__search import search

# An HTML page that we'll inject Protovis consumable data into

HTML_TEMPLATE = 'etc/twitter_retweet_graph.html'
OUT = os.path.basename(HTML_TEMPLATE)

# Writes out an HTML page that can be opened in the browser
# that displays a graph 

def write_protovis_output(g, out_file, html_template):
    nodes = g.nodes()
    indexed_nodes = {}

    idx = 0
    for n in nodes:
        indexed_nodes.update([(n, idx,)])
        idx += 1

    links = []
    for n1, n2 in g.edges():
        links.append({'source' : indexed_nodes[n2], 
                      'target' : indexed_nodes[n1]})

    json_data = json.dumps({"nodes" : [{"nodeName" : n} for n in nodes], \
                            "links" : links}, indent=4)

    html = open(html_template).read() % (json_data,)

    if not os.path.isdir('out'):
        os.mkdir('out')

    f = open(out_file, 'w')
    f.write(html)
    f.close()

    print >> sys.stderr, 'Data file written to: %s' % f.name

if __name__ == '__main__':

    # Your query

    Q = ' '.join(sys.argv[1])

    # How many batches of data to grab for the search results

    MAX_BATCHES = 2

    # How many search results per page

    COUNT = 200

    # Get some search results for a query
    t = oauth_login()
    search_results = search(t, q=Q, max_batches=MAX_BATCHES, count=COUNT)
    g = create_rt_graph(search_results)

    # Write Protovis output and open in browser

    if not os.path.isdir('out'):
        os.mkdir('out')

    f = os.path.join(os.getcwd(), 'out', OUT)

    write_protovis_output(g, f, HTML_TEMPLATE)

    webbrowser.open('file://' + f)
