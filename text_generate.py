import random
import string


def generate_random_text_file(filename, char_count):
    # 定义中文字符范围
    chinese_chars = ''.join(chr(i) for i in range(0x4e00, 0x9fff))
    # 定义中文标点符号
    chinese_punctuation = '，。？！；：‘’“”（）《》【】、…'
    # 定义ASCII字符和标点符号
    ascii_chars = string.ascii_letters + string.digits + string.punctuation
    # 定义换行和空格
    whitespace_chars = ' \n\r'

    # 合并所有可能的字符
    possible_chars = chinese_chars + chinese_punctuation + ascii_chars + whitespace_chars

    # 生成随机文本
    random_text = ''.join(random.choice(possible_chars) for _ in range(char_count))

    # 将随机文本写入文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(random_text)

# 使用函数生成测试文档
filename = 'test_document.txt'
char_count = 1000000  # 你可以根据需要修改这个值
generate_random_text_file(filename, char_count)
