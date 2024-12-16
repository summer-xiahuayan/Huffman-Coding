import heapq
import struct
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

def decode(encoded_bin_file):
    with open(encoded_bin_file, 'rb') as binary_file:
        # 读取前2个字节并转换为整数，以获取字符个数
        map_count_bytes = binary_file.read(2)
        map_count = int.from_bytes(map_count_bytes, byteorder='big')

        # 初始化一个空字典来存储解码后的数据
        decoded_dict = {}

        # 循环读取每个字符和其频度
        for _ in range(map_count):
            # 读取1个字节并转换为字符
            char_byte = binary_file.read(4)
           # char = int.from_bytes(char_byte, byteorder='big')
            # 将4个字节的数据转换为整数（Unicode码点）
            char_code_point = struct.unpack('I', char_byte)[0]

            # 将码点转换为对应的字符
            char = chr(char_code_point)

            # 读取2个字节并转换为频度
            freq_bytes = binary_file.read(2)
            freq = int.from_bytes(freq_bytes, byteorder='big')

            # 将字符和频度添加到字典中
            decoded_dict[char] = freq

        # 读取4个字节并转换为整数，以获取字符个数
        char_count_bytes = binary_file.read(4)
        char_count = int.from_bytes(char_count_bytes, byteorder='big')

        # 读取剩余的二进制数据
        encoded_bytes = binary_file.read()
        # 将每个字节转换为8位二进制字符串
        encoded_text = ''.join(format(byte, '08b') for byte in encoded_bytes)



    # 按照值（频率）由高到低排序，值相同的情况下按键的ASCII码排序
    sorted_items = sorted(
    decoded_dict.items(),
    key=lambda item: (-item[1], ord(item[0]))
    )

    # 将排序后的项转换回字典
    sorted_dict = dict(sorted_items)

    # 打印排序后的字典
    print(sorted_dict)



    root = build_huffman_tree(sorted_dict)



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
output_file = 'rawdecode.txt'  # 解码后的文件路径

decoded_text = decode(encoded_bin_file)
save_decoded_text(decoded_text, output_file)
print(f'Decoded text saved to {output_file}')


