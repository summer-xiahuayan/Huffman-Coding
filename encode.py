import heapq
import os
from collections import defaultdict, Counter
from graphviz import Digraph


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # 定义比较操作，用于优先队列中按频率比较节点
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_dict(text):
    return Counter(text)

def build_huffman_tree(frequency):
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def assign_codes_to_characters(node, prefix="", code_book={}):
    if node is not None:
        if node.char is not None:
            code_book[node.char] = prefix
        assign_codes_to_characters(node.left, prefix + "0", code_book)
        assign_codes_to_characters(node.right, prefix + "1", code_book)
    return code_book

def encode_text(text, code_book):
    return ''.join(code_book[char] for char in text)

def decode_text(encoded_text, root):
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root

    return decoded_text

def write_to_file(file_path, data):
    with open(file_path, 'w',encoding='utf-8') as file:
        file.write(data)

def huffman_coding(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # 指定UTF-8编码
        text = file.read()



    frequency = build_frequency_dict(text)
    # 按照值（频率）由高到低排序，值相同的情况下按键的ASCII码排序
    sorted_items = sorted(
        frequency.items(),
    key=lambda item: (-item[1], ord(item[0]))
    )
    # 将排序后的项转换回字典
    sorted_dict = dict(sorted_items)

    huffman_tree = build_huffman_tree(sorted_dict)
    # 可视化霍夫曼树
    visualize_huffman_tree(huffman_tree, 'Huffman Tree')
    huffman_codes = assign_codes_to_characters(huffman_tree)
    encoded_text = encode_text(text, huffman_codes)

    # 保存编码后的二进制文件
    binary_file_path = os.path.splitext(file_path)[0] + '.binary'
    print(f"bits_num:{len(encoded_text)}")
    if len(encoded_text)%8!=0:
        for i in range(8-len(encoded_text)%8):
            encoded_text+='0';

    print(f"bits_num:{len(encoded_text)}")
    with open(binary_file_path, 'wb') as binary_file:
        text_num= sum(item[1] for item in sorted_items)
        print(f"字符数：{text_num}")
        #前4个字节为字符个数
        binary_file.write(text_num.to_bytes(4, byteorder='big'))  # 大端序写入字符个数
        # 每8位二进制字符串转换为一个字节
        for i in range(0, len(encoded_text), 8):
            byte_string = encoded_text[i:i+8]  # 获取8位二进制字符串
            byte = int(byte_string, 2)  # 将二进制字符串转换为整数
            binary_file.write(byte.to_bytes(1, byteorder='big'))  # 写入文件

    #print(decode_text(encoded_text, huffman_tree))
    # 保存霍夫曼编码映射
    map_file_path = os.path.splitext(file_path)[0] + '.map'
    write_to_file(map_file_path, str(frequency))

    return binary_file_path, map_file_path



def visualize_huffman_tree(root, tree_name):
    """
    可视化霍夫曼树
    :param root: 霍夫曼树的根节点
    :param tree_name: 树的名称
    """
    dot = Digraph(comment=tree_name)
    dot.attr('node', fontname='Microsoft YaHei')  # 设置节点字体
    dot.attr('edge', fontname='Microsoft YaHei')  # 设置边字体

    def add_nodes(node, parent_name='', edge_label=''):
        if node is not None:
            if node.char is not None:  # 叶子节点
                dot.node(str(id(node)), node.char)
            else:  # 内部节点
                dot.node(str(id(node)), str(node.freq))
            if parent_name:
                dot.edge(str(parent_name), str(id(node)), label=edge_label)
            add_nodes(node.left, str(id(node)), '0')
            add_nodes(node.right, str(id(node)), '1')
    add_nodes(root)
    dot.render('huffman_tree', view=True)  # 保存并打开PNG文件
    #dot.view()




if __name__=="__main__":
    txt_file_path = 'raw.txt'  # 你的TXT文件路径
    binary_file, map_file = huffman_coding(txt_file_path)
    print(f'Encoded binary file: {binary_file}')
    print(f'Huffman code map file: {map_file}')



