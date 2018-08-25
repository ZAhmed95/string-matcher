class matcher(object):
    """
    This class is used for efficiently finding occurences of multiple patterns in a given text string.
    It uses an implementation of the Aho-Corasick algorithm to perform the pattern matching.
    """
    class trie_node(object):
        """
        This class represents a single node in the trie representing the patterns to search.
        """
        def __init__(self, string, parent=None):
            self.string = string # the string that this node represents 
            self.goto = {} # dict representing the valid characters that lead to a child node
            self.suffix = None # link to suffix node to go to upon failure
            self.output = None # link to output node to go to
            self.accept = False # bool that indicates if this node is an accept state (i.e. matches a pattern)
            self.parent = parent # parent node

        def __repr__(self):
            return self.string

        # below are override functions to make a trie_node behave more like a dict
        def __getitem__(self, key):
            return self.goto[key]

        def __setitem__(self, key, item):
            self.goto[key] = item

        def __contains__(self, key):
            return (key in self.goto)

        def __iter__(self):
            return iter(self.goto)

        def items(self):
            return self.goto.items()

        # shortcut method to get goto.keys()
        def keys(self):
            return self.goto.keys()
    
    # init for string_matcher
    def __init__(self, patterns=None):
        self.keywords = self.create_trie(patterns) if patterns else self.trie_node('')
        
    # create a trie from a given list of pattern strings
    def create_trie(self, patterns):
        root = self.trie_node('') # root node
        for pattern in patterns:
            current = root
            for i, c in enumerate(pattern):
                # if a node for this character doesn't exist, create it
                if c not in current.goto:
                    current[c] = self.trie_node(pattern[:i+1], current)
                # go into this node
                current = current[c]
                # if this node represents the final character in the pattern, it's an accept state
                if (i == len(pattern)-1):
                    current.accept = True
        
        # now that the structure has been created, create the suffix/output links
        self.create_links(root)
        return root
    
    # create suffix and output links for each node in trie
    def create_links(self, trie):
        # create queue to perform BFS on trie, populate with root's direct children
        queue = [(c,v) for c,v in trie.items()]
        while (len(queue) > 0):
            c, current = queue.pop(0) # get first character and node in queue
            # initially set suffix to root node
            current.suffix = trie
            # get parent's suffix
            suffix = current.parent.suffix
            while suffix:
                # suffix should only be 'None' for root
                # check if c is a child of suffix
                if c in suffix:
                    # set suffix link
                    current.suffix = suffix[c]
                    # check to see if we can create or follow an output link
                    if (current.suffix.accept):
                        # if suffix is an accept node, make an output link to it
                        current.output = current.suffix
                    else:
                        # otherwise, follow your suffix's output link (if it has one, otherwise None)
                        current.output = current.suffix.output

                    break # break loop
                # otherwise, get suffix's suffix
                suffix = suffix.suffix # say that five times fast
                # this loop will break if suffix becomes the root, whose suffix link is 'None'

            # put current's children in queue to continue the BFS
            for c,v in current.items():
                queue.append((c,v))
    
    # function to load a set of patterns and create a trie
    # saves searching time by creating and storing the trie beforehand
    def load_patterns(self, patterns):
        self.keywords = self.create_trie(patterns)
        
    # perform a search for the patterns represented by the trie on the given text
    def search(self, text, patterns=None):
        # create a trie from the argument patterns if passed in, else use stored trie
        trie = self.create_trie(patterns) if patterns else self.keywords
        # array of found matches
        matches = []
        # if trie is empty, return empty array
        if len(trie.keys()) == 0:
            return []
        
        # start at root node
        current = trie
        # loop through the characters in the text
        for i,c in enumerate(text):
            # 2 options: either there is a transition with c, or there isn't
            # if there is a transition, follow it
            if c in current:
                current = current[c]
            else:
                # if there's no transition, follow suffix links until you find a node with a proper transition,
                # OR you hit root
                while current.suffix:
                    # go to suffix link
                    current = current.suffix
                    # if a valid transition exists in the suffix, follow it
                    if c in current:
                        current = current[c]
                        break
                    # if suffix becomes None, that means we're at root, and no valid transitions exist for c
                    # just continue to the next character

            # check if this is an accept state
            if current.accept:
                matches.append((current.string, i+1-len(current.string)))
            # follow the chain of output links (if any)
            output = current.output
            while output:
                matches.append((output.string, i+1-len(output.string)))
                # follow the output chain
                output = output.output

        return matches
