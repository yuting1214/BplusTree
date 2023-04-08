# Inserting at the parent
def insert_in_parent(self, n, key, ndash):
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
            if (len(parentNode.values) > parentNode.order):
                parentdash = Node(parentNode.order)
                parentdash.parent = parentNode.parent
                mid = parentNode.order//2 -1 #int(math.ceil(parentNode.order / 2)) - 1
                parentdash.values = parentNode.values[mid + 1:]
                parentdash.keys = parentNode.keys[mid + 1:]
                key_ = parentNode.keys[mid]
                if (mid == 0):
                    parentNode.keys = parentNode.keys[:mid + 1]
                else:
                    parentNode.keys = parentNode.keys[:mid]
                parentNode.values = parentNode.values[:mid + 1]
                for j in parentNode.values:
                    j.parent = parentNode
                for j in parentdash.values:
                    j.parent = parentdash
                self.insert_in_parent(parentNode, key_, parentdash)
