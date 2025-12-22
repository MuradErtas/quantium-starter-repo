# test file to check if the sales_app dash file is working correctly
# Uses pytest for testing

import sys
import os
import pytest

# add the current directory to the path so we can import sales_app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sales_app import app
from dash import html, dcc


def test_header_present():
    """Test that the header (H1) is present in the layout"""
    layout = app.layout
    
    # find the H1 element by traversing the layout
    def find_h1(component):
        if isinstance(component, html.H1):
            return component
        if hasattr(component, 'children'):
            if isinstance(component.children, list):
                for child in component.children:
                    result = find_h1(child)
                    if result:
                        return result
            else:
                result = find_h1(component.children)
                if result:
                    return result
        return None
    
    h1 = find_h1(layout)
    assert h1 is not None, "Header (H1) not found in layout"
    assert h1.children == 'Pink Morsel Sales Dashboard', f"Header text incorrect: {h1.children}"


def test_visualization_present():
    """Test that the visualization (Graph component) is present"""
    layout = app.layout
    
    # convert layout to string representation to check for component
    layout_str = str(layout)
    
    # check if sales-graph id is present in the layout
    assert 'sales-graph' in layout_str, "Graph component with id='sales-graph' not found in layout"
    
    # also try to find it by traversing
    def find_by_id(component, target_id):
        # check if this component has the target id
        if hasattr(component, 'id'):
            try:
                if component.id == target_id:
                    return component
            except:
                pass
        
        # recursively search children
        if hasattr(component, 'children'):
            children = component.children
            if children is not None:
                if isinstance(children, list):
                    for child in children:
                        result = find_by_id(child, target_id)
                        if result:
                            return result
                elif children is not None:
                    result = find_by_id(children, target_id)
                    if result:
                        return result
        return None
    
    graph = find_by_id(layout, 'sales-graph')
    if graph is not None:
        assert hasattr(graph, 'id'), "Graph component missing id attribute"
        assert graph.id == 'sales-graph', f"Graph ID incorrect: {graph.id}"


def test_region_picker_present():
    """Test that the region picker (Dropdown) is present"""
    layout = app.layout
    
    # convert layout to string representation to check for component
    layout_str = str(layout)
    
    # check if region-filter id is present in the layout
    assert 'region-filter' in layout_str, "Region picker (Dropdown) with id='region-filter' not found in layout"
    
    # also try to find it by traversing
    def find_by_id(component, target_id):
        # check if this component has the target id
        if hasattr(component, 'id'):
            try:
                if component.id == target_id:
                    return component
            except:
                pass
        
        # recursively search children
        if hasattr(component, 'children'):
            children = component.children
            if children is not None:
                if isinstance(children, list):
                    for child in children:
                        result = find_by_id(child, target_id)
                        if result:
                            return result
                elif children is not None:
                    result = find_by_id(children, target_id)
                    if result:
                        return result
        return None
    
    dropdown = find_by_id(layout, 'region-filter')
    if dropdown is not None:
        assert hasattr(dropdown, 'id'), "Dropdown component missing id attribute"
        assert dropdown.id == 'region-filter', f"Dropdown ID incorrect: {dropdown.id}"
        assert hasattr(dropdown, 'value'), "Dropdown component missing value attribute"
        assert dropdown.value == 'all', f"Default dropdown value incorrect: {dropdown.value}"
        
        # check that all expected options are present
        assert hasattr(dropdown, 'options'), "Dropdown component missing options attribute"
        expected_options = ['all', 'north', 'south', 'east', 'west']
        option_values = [opt['value'] for opt in dropdown.options]
        for expected in expected_options:
            assert expected in option_values, f"Option '{expected}' not found in dropdown"


def test_custom_css_present():
    """Test that the custom CSS header is present"""
    assert app.index_string is not None, "Custom index_string not found"
    assert 'Pink Morsel Sales Dashboard' in app.index_string, "Title not found in index_string"
    assert 'background: linear-gradient' in app.index_string, "Custom CSS not found in index_string"

