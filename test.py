from bisect import bisect_left
class Node:
    def __init__(self, order):
        self.order = order
        self.values = []
        self.keys = []
        self.nextKey = None
        self.preKey = None
        self.parent = None
        self.check_leaf = False
        
    def insert_at_leaf(self, leaf, key, value):
        if (self.keys):
            temp1 = self.keys
            for i in range(len(temp1)):
                if (key == temp1[i]):
                    self.values[i].append(value)
                    break
                elif (key < temp1[i]):
                    self.keys = self.keys[:i] + [key] + self.keys[i:]
                    self.values = self.values[:i] + [[value]] + self.values[i:]
                    break
                elif (i + 1 == len(temp1)):
                    self.keys.append(key)
                    self.values.append([value])
                    break
        else:
            self.keys = [key]
            self.values = [[value]]

class BplusTree:
    def __init__(self, order):
        self.root = Node(order)
        self.root.check_leaf = True
        self.key_type = None

    # Insert operation
    def insert(self, key, value):
        old_node = self.search(key)
        old_node.insert_at_leaf(old_node, key, value)
        '''
        Splitting by mediam when full, creating two new child nodes:
        right_node inherited right parts of full leaf node
        left_node(old_node) inherited left parts of full leaf node
        old_node = fully inserted leaf node
        '''
        if (len(old_node.keys) == old_node.order):
            right_node = Node(old_node.order)
            right_node.check_leaf = True
            right_node.parent = old_node.parent
            mid = old_node.order//2
            # create a new right_node
            right_node.keys = old_node.keys[mid:]
            right_node.values = old_node.values[mid:]
            temp_right = old_node.nextKey
            right_node.nextKey = temp_right
            if temp_right:
                temp_right.preKey = right_node
            # update old_node as new left node
            old_node.values = old_node.values[:mid]
            old_node.keys = old_node.keys[:mid] 
            # Link sibling
            old_node.nextKey = right_node
            right_node.preKey = old_node
            self.insert_in_parent(old_node, right_node.keys[0], right_node)

    # Search toward leaf node
    def search(self, key):
        '''
        Search all the way down to leaf node, might not have the node with key
        but the node with the key fit in that range
        '''
        current_node = self.root
        while(current_node.check_leaf == False):
            temp2 = current_node.keys
            for i in range(len(temp2)):
                if (key == temp2[i]):
                    current_node = current_node.values[i + 1]
                    break
                elif (key < temp2[i]):
                    current_node = current_node.values[i]
                    break
                elif (i + 1 == len(current_node.keys)):
                    current_node = current_node.values[i+1]
                    break
        return current_node

    # Find the node
    def find(self, key, value):
        l = self.search(key)
        print('key')
        print(l.keys)
        for i, item in enumerate(l.keys):
            if item == key:
                if value in l.values[i]:
                    return True
                else:
                    return False
        return False

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
                    parent_right_node = Node(parentNode.order)
                    parent_right_node.parent = parentNode.parent
                    mid = parentNode.order//2 -1 
                    parent_right_node.values = parentNode.values[mid + 1:]
                    parent_right_node.keys = parentNode.keys[mid + 1:]
                    # Link next
                    temp_parent_right = parentNode.nextKey
                    parent_right_node.nextKey = temp_parent_right
                    if temp_parent_right:
                        temp_parent_right.preKey = parent_right_node
                    key_ = parentNode.keys[mid]
                    if (mid == 0):
                        parentNode.keys = parentNode.keys[:mid + 1]
                    else:
                        parentNode.keys = parentNode.keys[:mid]
                    parentNode.values = parentNode.values[:mid + 1]
                    # Link sibilings
                    parentNode.nextKey = parent_right_node
                    parent_right_node.preKey = parentNode
                    # Link Parents
                    for j in parentNode.values:
                        j.parent = parentNode
                    for j in parent_right_node.values:
                        j.parent = parent_right_node
                    self.insert_in_parent(parentNode, key_, parent_right_node)

    # Delete a node
    def delete(self, key, value):
        node_ = self.search(key)
        temp = 0
        for i, item in enumerate(node_.keys):
            if item == key:
                temp = 1

                if value in node_.values[i]:
                    # len(node_.values[i]) for nested list structure
                    # If duplicate just remove
                    if len(node_.values[i]) > 1:
                        node_.values[i].pop(node_.values[i].index(value))
                    elif node_ == self.root:
                        node_.values.pop(i)
                        node_.keys.pop(i)
                    # In case no duplicate, delete first then adjust
                    else:
                        node_.values[i].pop(node_.values[i].index(value))
                        del node_.values[i]
                        node_.keys.pop(node_.keys.index(key))
                        self.deleteEntry(node_, key, value)
                else:
                    print("Value not in Key")
                    return
        if temp == 0:
            print("Key not in Tree")
            return

    # Delete an entry
    def deleteEntry(self, node_, key, value):
        # If node is internal node, values={node}, keys={key_str}
        if not node_.check_leaf:
            for i, item in enumerate(node_.values):
                if item == value:
                    node_.values.pop(i)
                    break
            for i, item in enumerate(node_.keys):
                if item == key:
                    node_.keys.pop(i)
                    break

        if self.root == node_ and len(node_.values) == 1:
            self.root = node_.values[0]
            node_.values[0].parent = None
            del node_
            return
        elif (len(node_.values) < (node_.order//2 +1) and node_.check_leaf == False) or (len(node_.keys) < (node_.order//2) and node_.check_leaf == True):
            '''
            Adjust when 
            1. In internal node,  len(node_.values):number of child < (node_.order//2 +1)
            2. In leaf node, len(node_.keys):number of key < (node_.order//2)
            '''
            is_predecessor = 0
            parentNode = node_.parent
            PrevNode = -1
            NextNode = -1
            PrevK = -1
            NextK = -1
            # parentNode.values:[children_nodes], parentNode.keys:[key_str]
            print(f'When delte, parent is: {parentNode.keys}')
            for i, item in enumerate(parentNode.values):
                if item == node_:
                    if i > 0:
                        PrevNode = parentNode.values[i - 1]
                        PrevK = parentNode.keys[i - 1]

                    if i < len(parentNode.values) - 1:
                        NextNode = parentNode.values[i + 1]
                        NextK = parentNode.keys[i]

            if PrevNode == -1:
                ndash = NextNode
                key_ = NextK
            elif NextNode == -1:
                is_predecessor = 1
                ndash = PrevNode
                key_ = PrevK
            else:
                if len(node_.keys) + len(NextNode.keys) < node_.order:
                    ndash = NextNode
                    key_ = NextK
                else:
                    is_predecessor = 1
                    ndash = PrevNode
                    key_ = PrevK
            if isinstance(ndash, int):
                print('Delete all index')
                return None
            if len(node_.keys) + len(ndash.keys) < node_.order:
                if is_predecessor == 0:
                    node_, ndash = ndash, node_
                ndash.values += node_.values
                if not node_.check_leaf:
                    ndash.keys.append(key_)
                else:
                    ndash.nextKey = node_.nextKey
                ndash.keys += node_.keys

                if not ndash.check_leaf:
                    for j in ndash.values:
                        j.parent = ndash

                self.deleteEntry(node_.parent, key_, node_)
                del node_
            else:
                if is_predecessor == 1:
                    if not node_.check_leaf:
                        ndashpm = ndash.values.pop(-1)
                        ndashkm_1 = ndash.keys.pop(-1)
                        node_.values = [ndashpm] + node_.values
                        node_.keys = [key_] + node_.keys
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == key_:
                                parentNode.keys[i] = ndashkm_1
                                break
                    else:
                        ndashpm = ndash.values.pop(-1)
                        ndashkm = ndash.keys.pop(-1)
                        node_.values = [ndashpm] + node_.values
                        node_.keys = [ndashkm] + node_.keys
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == key_:
                                parentNode.keys[i] = ndashkm
                                break
                else:
                    if not node_.check_leaf:
                        ndashp0 = ndash.values.pop(0)
                        ndashk0 = ndash.keys.pop(0)
                        node_.values = node_.values + [ndashp0]
                        node_.keys = node_.keys + [key_]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == key_:
                                parentNode.keys[i] = ndashk0
                                break
                    else:
                        ndashp0 = ndash.values.pop(0)
                        ndashk0 = ndash.keys.pop(0)
                        node_.values = node_.values + [ndashp0]
                        node_.keys = node_.keys + [ndashk0]
                        parentNode = node_.parent
                        for i, item in enumerate(parentNode.keys):
                            if item == key_:
                                parentNode.keys[i] = ndash.keys[0]
                                break

                if not ndash.check_leaf:
                    for j in ndash.values:
                        j.parent = ndash
                if not node_.check_leaf:
                    for j in node_.values:
                        j.parent = node_
                if not parentNode.check_leaf:
                    for j in parentNode.values:
                        j.parent = parentNode

    # Use BFS to check B+tree structure
    def show(self):
        level = 0
        current_level_nodes = [self.root]
        while current_level_nodes:
            next_level_nodes = []
            print("Level", level, ": ")
            for idx, node in enumerate(current_level_nodes):
                print(f'{node.keys}', end=" ")
                if not node.check_leaf:
                    next_level_nodes += node.values
            if node.check_leaf:
                print()
                break
            print()
            current_level_nodes = next_level_nodes
            level += 1
        return None

    def retreive_new(self, key, cmp):
            leaf_node = self.search(key)
            leaf_node_keys = leaf_node.keys
            value_list = []
            if cmp == 'gt':
                # Handle target node
                if key in leaf_node_keys:
                    key_location = leaf_node_keys.index(key)
                    start_location = key_location+1
                else:
                    start_location = bisect_left(leaf_node_keys, key)
                value_list += leaf_node.values[start_location:]
                head = leaf_node.nextKey
                
                # Handle sibling
                while head:
                    value_list += head.values
                    head = head.nextKey
                # Flatten list
                return_list = [element for sublist in value_list for element in sublist]
                return return_list
            
            elif cmp == 'gte':
                # Handle target node
                if key in leaf_node_keys:
                    key_location = leaf_node_keys.index(key)
                    start_location = key_location
                else:
                    start_location = bisect_left(leaf_node_keys, key)
                value_list += leaf_node.values[start_location:]
                head = leaf_node.nextKey
                
                # Handle sibling
                while head:
                    value_list += head.values
                    head = head.nextKey
                # Flatten list
                return_list = [element for sublist in value_list for element in sublist]
                return return_list
            
            elif cmp == 'lt':
                # Handle target node
                if key in leaf_node_keys:
                    key_location = leaf_node_keys.index(key)
                    start_location = key_location
                else:
                    start_location = bisect_left(leaf_node_keys, key)
                value_list += leaf_node.values[:start_location]
                head = leaf_node.preKey
                
                # Handle sibling
                while head:
                    value_list += head.values
                    head = head.preKey
                # Flatten list
                return_list = [element for sublist in value_list for element in sublist]
                return return_list

            elif cmp == 'lte':
                # Handle target node
                if key in leaf_node_keys:
                    key_location = leaf_node_keys.index(key)
                    start_location = key_location+1
                else:
                    start_location = bisect_left(leaf_node_keys, key)
                value_list += leaf_node.values[:start_location]
                head = leaf_node.preKey
                
                # Handle sibling
                while head:
                    value_list += head.values
                    head = head.preKey
                # Flatten list
                return_list = [element for sublist in value_list for element in sublist]
                return return_list
            
            elif cmp == '':
                leaf_node_values = leaf_node.values
                for i, item in enumerate(leaf_node_keys):
                    if item == key:
                        value_list += leaf_node_values[i]
                return_list = [element for sublist in value_list for element in sublist]
                return return_list
            elif cmp == 'ne':
                if key in leaf_node_keys:
                    key_location = leaf_node_keys.index(key)
                    del leaf_node.values[key_location]
                value_list += leaf_node.values
                
                # Handle sibling
                backward = forward = leaf_node
                while backward:
                    value_list += backward.values
                    backward = backward.preKey
                while forward:
                    value_list += forward.values
                    forward = forward.preKey    
                # Flatten list
                return_list = [element for sublist in value_list for element in sublist]
                return return_list
            else:
                raise('Not support in current function!')
