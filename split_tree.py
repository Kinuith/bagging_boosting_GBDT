# coding = utf-8


class TreeNode(object):

    def __init__(self,split_value,split_feature,is_leaf = False):

        self.split_value = split_value
        self.split_feature = split_feature
        self.is_leaf = is_leaf

    def extend(self,left_node,right_node):
        self.left_node = left_node
        self.right_node = right_node

    def set_type(self,type):
        assert self.is_leaf

        self.type = type

    def classifier(self,data):
        if self.is_leaf:
            return self.type
        elif data[self.split_feature] < self.split_value:
            return self.left_node.classifier(data)
        else:
            return self.right_node.classifier(data)


class RandomForest(object):

    def __init__(self):
        self.TreeSet = []

    def Add_Tree(self,Node):
        self.TreeSet.append(None)

    def classifier(self,data):

        type_list = [ node.classifier for node in self.TreeSet]



