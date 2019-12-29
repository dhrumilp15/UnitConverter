from csvConvTable import csvConvTable
from graph import graph

import os

datahandler = csvConvTable()
datahandler.loadConvTable(os.getcwd() + '/conversionTable.csv')

graph = graph()
graph.buildGraph(datahandler.rows)

def test_bfs():
    assert(graph.bfs(start = 'bingbong', target= 'cm')) == False

    assert(graph.bfs(start = 'm', target= 'm')[0]) == True

    assert(isinstance(graph.bfs(start = 'm', target = 'in')[1], dict)) == True

def test_shortest_path():
    assert(graph.getShortestPath(target = 'm', parent = {'m': None})) == ['m']
    assert(isinstance(graph.getShortestPath(target= 'cm', parent = {'m': None, 'cm' : 'm'}), list)) == True

def test_update_graph():
    graph.updateGraph(source = 'cm', target = 'ft')
    assert('ft' in graph.graph['cm'] and 'cm' in graph.graph['ft']) == True