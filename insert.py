# Inserting at the parent
    def insert_in_parent(self, n, key, ndash):
        # When reaching to the root, create new root
        if (self.root == n):
            rootNode = Node(n.order)
            rootNode.keys = [key]
            rootNode.values = [n, ndash]
            self.root = rootNode
            n.parent = rootNode
            ndash.parent = rootNode
            return

        parentNode = n.parent
        temp3 = parentNode.values
        for i in range(len(temp3)):
            if (temp3[i] == n):
                parentNode.keys = parentNode.keys[:i] + \
                    [key] + parentNode.keys[i:]
                parentNode.values = parentNode.values[:i +
                                                1] + [ndash] + parentNode.values[i + 1:]
                # keep splitting
                if (len(parentNode.values) > parentNode.order):
                    parent_right_node = Node(parentNode.order)
                    parent_right_node.parent = parentNode.parent
                    mid = parentNode.order//2
                    parent_right_node.values = parentNode.values[mid:]
                    parent_right_node.keys = parentNode.keys[mid:]
                    key_ = parentNode.keys[mid]
                    if (mid == 0):
                        parentNode.keys = parentNode.keys[:mid]
                    else:
                        parentNode.keys = parentNode.keys[:mid-1]
                    parentNode.values = parentNode.values[:mid]
                    # Link sibilings
                    parentNode.nextKey = parent_right_node
                    parent_right_node.preKey = parentNode
                    # Link parents
                    for j in parentNode.values:
                        j.parent = parentNode
                    for j in parent_right_node.values:
                        j.parent = parent_right_node
                    self.insert_in_parent(parentNode, key_, parent_right_node)
