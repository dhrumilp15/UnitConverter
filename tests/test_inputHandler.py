#!/usr/bin/env python3
from inputHandler import inputHandler
from csvConvTable import csvConvTable
from graph import graph

import os

graph = graph()
dataHandler = csvConvTable()

dataHandler.loadConvTable(os.getcwd() + '/conversionTable.csv')
graph.buildGraph(dataHandler.rows)

inputHandler = inputHandler(dataHandler, graph)

def test_parse_input():
    # Basic input:
    assert(inputHandler.parseInput(1,'m','mm')) == (1, [('m','mm')])
    assert(inputHandler.parseInput(1.0,'m','mm')) == (1.0, [('m','mm')])
    
    # Complex input
    assert(inputHandler.parseInput(1,'m/s','in/hr')) == (1, [('m','in'), ('s', 'hr')])
    
    # Combined Complex Input
    assert(inputHandler.parseInput(1,'W','kJ/s')) == (1, [('J','kJ'), ('s', 's')])