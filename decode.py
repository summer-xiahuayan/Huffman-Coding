import heapq
from collections import defaultdict, Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

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

def decode(encoded_bin_file, huffman_map_file):
    with open(huffman_map_file, 'r',encoding='utf-8') as file:
        huffman_codes = eval(file.read())  # 将字符串形式的字典转换为字典对象

    # 构建霍夫曼树
    char_freq = {char: freq for char, freq in huffman_codes.items() if freq}

    # 按照值（频率）由高到低排序，值相同的情况下按键的ASCII码排序
    sorted_items = sorted(
    char_freq.items(),
    key=lambda item: (-item[1], ord(item[0]))
    )

    # 将排序后的项转换回字典
    sorted_dict = dict(sorted_items)

    # 打印排序后的字典
    print(sorted_dict)



    root = build_huffman_tree(sorted_dict)

    # 读取二进制文件并解码
    with open(encoded_bin_file, 'rb') as binary_file:
        # 读取前4个字节并转换为整数，以获取字符个数
        char_count_bytes = binary_file.read(4)
        char_count = int.from_bytes(char_count_bytes, byteorder='big')

        # 读取剩余的二进制数据
        encoded_bytes = binary_file.read()
        # 将每个字节转换为8位二进制字符串
        encoded_text = ''.join(format(byte, '08b') for byte in encoded_bytes)

    decoded_text = ''
    current_node = root

    decode_count=0
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text += current_node.char
            decode_count+=1
            current_node = root
            if decode_count==char_count:
                break
    return decoded_text

def save_decoded_text(decoded_text, output_file):
    with open(output_file, 'w',encoding='utf-8') as file:
        file.write(decoded_text)

# 使用示例
encoded_bin_file = 'raw.binary'  # 编码后的二进制文件路径
huffman_map_file = 'raw.map'  # 霍夫曼编码映射文件路径
output_file = 'rawdecode.txt'  # 解码后的文件路径

decoded_text = decode(encoded_bin_file, huffman_map_file)
save_decoded_text(decoded_text, output_file)
print(f'Decoded text saved to {output_file}')


