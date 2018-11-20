class TrieNode:
    def __init__(self, value):
        '''Initializes a single node of a trie with a value'''
        self._value = value
        self._children = []
        self._end = 0


    def add_child(self, child: 'TrieNode'):
        '''Adds a child TrieNode to the children of this TrieNode'''
        self._children.append(child)


    def mark_end(self):
        '''Identifies that this node marks the end of a word or list'''
        self._end += 1


    def __str__(self):
        s = f'{str(self._value)}'
        if self._end:
            s += '*'
        return s


class Trie:
    def __init__(self):
        '''Creates a new trie containing a single root node'''
        self._root = TrieNode('ROOT')


    def trace(self, iterable):
        '''Generates a list of indices for each layer where each element of the given iterable is found'''
        node = self._root
        for item in iterable:
            for i, child in enumerate(node._children):
                if child._value == item:
                    node = child
                    yield i
                    break
            else:
                raise ValueError('Given iterable not found in Trie')


    def add(self, iterable):
        '''Adds an iterable to the trie, iterating down'''
        node = self._root
        for item in iterable:
            for child in node._children:
                if child._value == item:
                    node = child
                    break
            else:
                new_node = TrieNode(item)
                node.add_child(new_node)
                node = new_node
        node.mark_end()


    # TODO: Implement
    # General approach is to get the location of each node in the Trie, and go
    # to the bottom. Once you're at the bottom, delete a node if it doesn't
    # have any children, and move up a layer. Repeat
    def remove(self, iterable):
        raise NotImplementedError


    def find_prefix(self, iterable):
        '''Finds if a given iterable is found within the trie'''
        node = self._root
        if not self._root._children:
            return None
        # Breadth-first search
        for item in iterable:
            for child in node._children:
                if child._value == item:
                    node = child
                    break
            else:
                return None
        return node


    def has_iterable(self, iterable):
        '''Returns True if the iterable (as an entire sequence) is found within the trie, otherwise False'''
        node = self.find_prefix(iterable)
        if node is not None:
            return bool(node._end)
        return False


    def __contains__(self, iterable):
        '''Returns True if the iterable is found within the trie, otherwise False'''
        return self.find_prefix(iterable) is not None
