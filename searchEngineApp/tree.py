class TreeNode:
    def __init__(self):
        self.children = {}  # char -> TreeNode
        self.is_word = False
    def hasChild(self):
        return len(self.children) > 0

class Tree:
    def __init__(self, words=None):
        self.root = TreeNode()
        if words:
            for word in words:
                self.insert(word)
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TreeNode()
            node = node.children[char]
        node.is_word = True
    
    def serialize(self):
        """Convert tree to JSON-serializable dictionary"""
        def serialize_node(node):
            return {
                "is_word": node.is_word,
                "children": {char: serialize_node(child) for char, child in node.children.items()}
            }
        return serialize_node(self.root)
    
    def deserialize(self, data):
        """Rebuild tree from serialized dictionary"""
        def deserialize_node(data):
            node = TreeNode()
            node.is_word = data["is_word"]
            for char, child_data in data["children"].items():
                node.children[char] = deserialize_node(child_data)
            return node
        self.root = deserialize_node(data)
    
    def print_visual(self):
        def dfs_visual(node, prefix, is_last):
            if node.is_word:
                # Mark complete words with [*]
                print(prefix + "[*]")
            
            children = list(node.children.items())
            for i, (char, child) in enumerate(children):
                is_last_child = (i == len(children) - 1)
                
                # Create branch characters
                branch = "└── " if is_last_child else "├── "
                extension = "    " if is_last_child else "│   "
                
                print(prefix + branch + char)
                dfs_visual(child, prefix + extension, is_last_child)
        
        print("ROOT")
        dfs_visual(self.root, "", True)
    
#test
# wt = Tree(["hello", "world", "hi", "her", "hero", "heron"])
# wt.print_visual()