import yaml
import wrapt
from yaml import Loader, Dumper

class Tagged(wrapt.ObjectProxy):
    # tell wrapt to set the attribute on the proxy, not the wrapped object
    tag = None

    def __init__(self, tag, wrapped):
        super().__init__(wrapped)
        self.tag = tag

    def __repr__(self):
        return f"{type(self).__name__}({self.tag!r}, {self.__wrapped__!r})"

def construct_undefined(self, node):
    if isinstance(node, yaml.nodes.ScalarNode):
        value = self.construct_scalar(node)
    elif isinstance(node, yaml.nodes.SequenceNode):
        value = self.construct_sequence(node)
    elif isinstance(node, yaml.nodes.MappingNode):
        value = self.construct_mapping(node)
    else:
        assert False, f"unexpected node: {node!r}"
    return Tagged(node.tag, value)

Loader.add_constructor(None, construct_undefined)

def represent_tagged(self, data):
    assert isinstance(data, Tagged), data
    node = self.represent_data(data.__wrapped__)
    node.tag = data.tag
    return node

Dumper.add_representer(Tagged, represent_tagged)