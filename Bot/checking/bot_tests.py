import pytest 
import json

def test1():
    pass

def test2():
    pass


def test_info_coverage_json(filename='coverage.json'):
    file = open(filename, "r")
    data = json.loads(file.read())
    assert data['totals']['percent_covered'] == 100