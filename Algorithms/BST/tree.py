class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None 
        self.right = None


class Solution:
    """
    二叉树遍历非递归实现
    """
    @staticmethod
    def pre_order(root):
        if not root:
            return []
        stack, ret = [], []
        stack.append(root)
        while len(stack) != 0:
            node = stack.pop()
            ret.append(node.val)
            # 栈的弹出顺序与入栈顺序相反，因此先入右再入左
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return ret


    @staticmethod
    def in_order(root):
        """
        当前节点如果有左节点就不断压栈，无左节点就出栈打印
        打印出栈的节点若有右子树则将右节点执行上一步
        """
        if not root:
            return []
        stack, ret = [], []
        node = root
        # 循环条件：1. 栈非空则还可以输出； 2. 栈空但是节点非空，说明还有节点可以压栈
        while node or len(stack) != 0:
            if not node:
                # 如果节点为空，证明没有左子树，弹出
                node = stack.pop()
                ret.append(node.val)
                node = node.right # 尝试是否有右子树
            else:
                # 节点非空，压栈 尝试是否有左子树
                stack.append(node)
                node = node.left
        return ret


    @staticmethod
    def post_order(root):
        """
        return ret[::-1] 逆序
        """
        if not root:
            return []
        stack, ret = [], []
        stack.append(root)
        while len(stack) != 0:
            node = stack.pop() # 当作先序 先输出
            ret.append(node.val)
            # 先压左再压右 所以输出就是先右后左
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return ret[::-1] # 将中-右-左 逆序为 左-右-中


    def pre_order_traversal(self, root):
        if not root:
            return []
        return [root.val] + self.pre_order_traversal(root.left) + self.pre_order_traversal(root.right)


    @staticmethod
    def level_order(root):
        queue = [root]
        ret = []
        while queue:
            node = queue.pop()
            if not node:
                ret.append(None)
                continue
            ret.append(node.val)
            queue.insert(0, node.left)
            queue.insert(0, node.right)
        print(ret)
        return ret


class BSTNode(object):
    def __init__(self, key, val, left=None, right=None):
        self.key, self.val, self.left, self.right = key, val, left, right


class BST(object):
    def __init__(self, root=None):
        self.root=root

    @classmethod
    def build_from(cls, node_list):
        cls.size=0
        key_to_node_dict={}
        for node_dict in node_list:
            key=node_dict['key']
            key_to_node_dict[key]=BSTNode(key, val=key)
        
        for node_dict in node_list:
            key=node_dict['key']
            node=key_to_node_dict[key]
            if node_dict['is_root']:
                root=node
            node.left=key_to_node_dict.get(node_dict['left'])
            node.right=key_to_node_dict.get(node_dict['right'])
            cls.size+=1

        return cls(root)

    def _bst_search(self, subtree, key):
        """
        辅助函数
        """
        if subtree is None:
            return None
        elif key < subtree.key:
            return self._bst_search(subtree.left, key)
        elif key > subtree.key:
            return self._bst_search(subtree.right, key)
        else:
            return subtree

    def get(self, key, default=None):
        node=self._bst_search(self.root, key)
        if node is None:
            return default
        else:
            return node.val

    def __contains__(self, key):
        return self._bst_search(self.root, key) is not None

    def _bst_min_node(self, subtree):
        """
        辅助函数，查找包含最小key的结点
        """
        if subtree is None:
            return None
        elif subtree.left is None:
            # 说明搜索到左子树的尽头
            return subtree
        else:
            return self._bst_min_node(subtree.left)

    def bst_min(self):
        node=self._bst_min_node(self.root)
        return node.val if node else None

    def _bst_insert(self, subtree, key, val):
        """
        辅助函数 插入操作，当做叶子结点插入BST中。插入并返回根节点
        """
        if subtree is None:
            subtree = BSTNode(key, val)
        elif key < subtree.key:
            subtree.left = self._bst_insert(subtree.left, key, val)
        elif key > subtree.key:
            subtree.right = self._bst_insert(subtree.right, key, val)
        return subtree

    def add(self, key, val):
        node=self._bst_search(self.root, key)
        if node is not None:
            node.val = val
            return False
        else:
            self.root=self._bst_insert(self.root, key, val)
            self.size += 1
            return True

    def _bst_remove(self, subtree, key):
        # https://www.bilibili.com/video/BV1jT4y1G7e2?p=34
        if subtree is None:
            return subtree
        elif key < subtree.key:
            subtree.left = self._bst_remove(subtree.left, key)
            return subtree
        elif key > subtree.key:
            subtree.right = self._bst_remove(subtree.right, key)
        else:  # 找到需要删除的结点
            if subtree.left is None and subtree.right is None:  # 叶子结点
                return None
            elif subtree.left is None or subtree.right is None:  # 有一个子结点
                if subtree.left is not None:
                    return subtree.left  # 返回它的孩子结点
                else:
                    return subtree.right
            else:  # 两个子结点，寻找后继结点，并替换
                successor_node=self._bst_min_node(subtree.right)
                subtree.key, subtree.val=successor_node.key, successor_node.val
                subtree.right=self._bst_remove(subtree.right, successor_node.key)
                return subtree

    def remove(self, key):
        assert key in self
        self.size -= 1
        return self._bst_remove(self.root, key)



def main():
    t1 = TreeNode(10)
    t2 = TreeNode(9)
    t3 = TreeNode(5)
    t4 = TreeNode(3)
    t5 = TreeNode(1)
    t6 = TreeNode(8)
    t7 = TreeNode(7)

    t1.left = t2
    t1.right = t3
    t2.left = t4
    t2.right = t5
    t3.right = t6
    t5.right = t7

    print('pre_order: ',Solution.pre_order(t1))
    Solution.level_order(t1)


    node_list=[
        {'key':60, 'left':12, 'right':90, 'is_root':True},
        {'key':12, 'left':4, 'right':41, 'is_root':False},
        {'key':4, 'left':1, 'right':None, 'is_root':False},
        {'key':1, 'left':None, 'right':None, 'is_root':False},
        {'key':41, 'left':29, 'right':None, 'is_root':False},
        {'key':29, 'left':23, 'right':37, 'is_root':False},
        {'key':23, 'left':None, 'right':None, 'is_root':False},
        {'key':37, 'left':None, 'right':None, 'is_root':False},
        {'key':90, 'left':71, 'right':100, 'is_root':False},
        {'key':71, 'left':None, 'right':84, 'is_root':False},
        {'key':100, 'left':None, 'right':None, 'is_root':False},
        {'key':84, 'left':None, 'right':None, 'is_root':False},
    ]

    bst=BST.build_from(node_list)
    


if __name__=="__main__":
    #main()
    print('asdf')
    print(dir())
