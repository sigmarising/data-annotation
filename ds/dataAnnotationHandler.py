"""
class: DataAnnotationHandler
Author: Zhang Yun
Date: 2019/3/18
Desc:
    用于检查原始标注文件的各种错误，并统计词频、朝代、作者
    可检查的错误包括：
        1. 是否符合 题目-朝代-作者-正文 四段格式
        2. 标点是否正确被单独分词
        3. 词性标签位置是否正确
"""


class DataAnnotationHandler:

    def __init__(self, file_path: str, marks: list, tags: list):
        """
        构造函数 - public
        用于构造 handler 对象
        :param file_path: 原始标注文件的文件名（含路径和扩展名）
        :param marks: 所有可能会出现的标点
        :param tags: 所有可能的词性标记
        """
        self.marks: list = marks        # 标点
        self.tags: list = tags          # 词性标记
        self.words_sum: dict = dict()   # 词频统计
        self.dynasty: set = set()       # 朝代记录
        self.poets: set = set()         # 诗人记录

        print("CHECKING FILE " + file_path)
        print("--------------------[START CHECKING]--------------------")
        result: bool = self.__file_checker(file_path)
        print("---------------------[END CHECKING]---------------------")
        print("RESULT: " + ("SUCCEED" if result else "FAILED"))

    def __file_checker(self, file_path: str) -> bool:
        """
        文件检查函数 - private
        逐行分析检查
        :param file_path: 需要打开的文件
        :return: 检查成功或失败
        """
        flag: bool = True

        with open(file_path, encoding='utf-8') as file:
            line_number: int = 0
            for line in file:
                line_number += 1
                if not self.__line_checker(line, line_number):
                    flag = False

        return flag

    def __line_checker(self, line: str, lineno: int) -> bool:
        """
        行检查函数 - private
        去掉行尾标记，并检查诗四段格式，统计朝代和作者
        :param line: 要检查的行 str
        :param lineno: 检查的行所在的行号
        :return: 检查成功或失败
        """
        if line.startswith('----------'):
            return True

        flag: bool = True

        paragraph_arr: list = line.rstrip('\n').rstrip('\r').rstrip('\n\r').rstrip('\r\n').split('\t')
        if len(paragraph_arr) != 4:
            flag = False
            print("ERR - LINE " + str(lineno) + ": 诗格式未按照 “诗名-朝代-作者-正文” 划分四部分")
        else:
            self.dynasty.add(paragraph_arr[1])
            self.poets.add(paragraph_arr[2])

            if not self.__paragraph_checker(paragraph_arr[0], lineno):
                flag = False
            if not self.__paragraph_checker(paragraph_arr[3], lineno):
                flag = False

        return flag

    def __paragraph_checker(self, paragraph: str, lineno: int) -> bool:
        """
        段落检查函数 - private
        检查标题和正文的格式
        :param paragraph: 要检查的段落 str
        :param lineno: 检查的段落所在行号
        :return: 检查成功或失败
        """
        flag: bool = True

        words_arr: list = paragraph.split(' ')

        for word in words_arr:
            if word in self.marks:
                continue
            else:
                if not self.__word_checker(word, lineno):
                    flag = False

        return flag

    def __word_checker(self, word: str, lineno: int) -> bool:
        """
        词检查函数 - private
        检查分词是否符合格式要求，统计词频
        :param word: 要检查的词
        :param lineno: 检查的词所在行号
        :return: 检查成功或失败
        """
        flag: bool = True

        for i in range(len(word)):
            if word[i] in self.marks:
                flag = False
                print("ERR - LINE " + str(lineno) + ": 分词 “" + word + "” 中包含了标点符号")
            if i != len(word) - 1 or len(word) == 1:
                if word[i] in self.tags:
                    flag = False
                    print("ERR - LINE " + str(lineno) + ": 分词 “" + word + "” 的词性标签位置错误")

        if flag:
            if word in self.words_sum:
                self.words_sum[word] += 1
            else:
                self.words_sum[word] = 1

        return flag
