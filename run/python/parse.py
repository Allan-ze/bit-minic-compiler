# !/usr/bin/python
# -*- coding: utf-8 -*-
# 语法分析，通过语法规则构建LR(1)的DFA，通过LR(1)项目集确定分析表
import os
import sys
from xml.dom import minidom
import xml.etree.cElementTree as ET

class DFA(object):
    def __init__(self, alphabets):
        super(DFA, self).__init__()
        self.status = {}
        self.alphabets = alphabets

class LRDFANode(object):

    def __init__(self, set_id):
        self.set_id = set_id
        self.object_set = set()
        self.edge = {}

    def add_object_set(self, id, left, right, index, tail):
        tmp = (id, left, right, index, tail)
        if tmp not in self.object_set:
            self.object_set.add(tmp)

    def add_object_set_by_set(self, object_set):
        self.object_set |= object_set



class SyntaxAnalyze(object):

    def __init__(self):
        super(SyntaxAnalyze, self).__init__()
        # first集合
        self.first_set = {}
        # 产生式
        self.productions = []
        # 所有元素
        self.all_elem = set()
        # 终结符
        self.terminate = set()
        # 非终极符
        self.noterminate = set()
        # 产生式表
        self.productions_dict = {}
        # LR1分析表
        self.lr_analyze_table = {}

    def read_syntax_grammar(self, file_name):
        for line in open(file_name, 'r'):
            line = line[:-1]
            cur_left = line.split(':')[0]
            cur_right = line.split(':')[1]
            right_list = []
            if cur_right.find(' ') != -1:
                right_list = cur_right.split(' ')
            else:
                right_list.append(cur_right)
            production = {cur_left: right_list}
            self.productions.append(production)

    def get_terminate_noterminate(self):
        for production in self.productions:
            for left in production.keys():
                if left not in self.productions_dict:
                    self.productions_dict[left] = []
                self.productions_dict[left].append((
                    tuple(production[left]),
                    self.productions.index(production)))
                self.all_elem.add(left)
                self.noterminate.add(left)
                for right in production[left]:
                    self.all_elem.add(right)
        self.terminate = self.all_elem - self.noterminate

    def __get_first_set(self, cur_status, all_elem):
        # 求fisrt集合
        #print cur_status
        if cur_status in self.first_set:
            return self.first_set[cur_status]
        all_elem.add(cur_status)
        cur_status_set = set()
        for right_list in self.productions_dict[cur_status]:
            for right in right_list[0]:
                # right代表第一个符号
                right_set = None
                # print all_elem
                if right in all_elem:
                    # 如果已经存在
                    continue
                if right in self.first_set:
                    # 如果已经求过
                    right_set = self.first_set[right]
                else:
                    # 如果没有求过，便递归求解
                    right_set = self.__get_first_set(right, all_elem)
                cur_status_set |= right_set
                if '$' not in right_set:
                    # 没有空串
                    break
        return cur_status_set

    def init_first_set(self):
        for terminate in self.terminate:
            self.first_set[terminate] = set([terminate])
        for noterminate in self.noterminate:
            self.first_set[noterminate] = self.__get_first_set(
                noterminate, set())

    def create_lr_dfa(self):
        all_status = {}
        all_object_set = {}
        self.DFA = DFA(set())

        def create_get_lr_dfa_node(set_id):
            if set_id in all_status:
                return all_status[set_id]
            return LRDFANode(set_id=set_id)

        def expand_production(self, cur_production, ex_object_set):
            ex_object_set.add(cur_production)
            right = cur_production[2]
            point_index = cur_production[3]
            tail_set = cur_production[4]
            if point_index < len(right) and\
                    (right[point_index] in self.noterminate):
                for pro_right in self.productions_dict[right[point_index]]:
                    new_tail_set = set()
                    flag = True
                    for i in range(point_index + 1, len(right)):
                        cur_first_set = self.first_set[right[i]]
                        if '$' in cur_first_set:
                            new_tail_set = tuple(
                                set(new_tail_set) | (cur_first_set - set('$')))
                        else:
                            flag = False
                            new_tail_set = tuple(
                                set(new_tail_set) | cur_first_set)
                            break
                    if flag:
                        new_tail_set = tuple(set(new_tail_set) | set(tail_set))
                    ex_new_production = (
                        pro_right[1],
                        right[point_index], pro_right[0], 0, new_tail_set)
                    if ex_new_production not in ex_object_set:
                        ex_object_set |= expand_production(
                            self, ex_new_production, ex_object_set)
                new_ex_object_set = {}
                for eos in ex_object_set:
                    pro_key = (eos[0], eos[1], eos[2], eos[3])
                    if tuple(pro_key) not in new_ex_object_set:
                        new_ex_object_set[tuple(pro_key)] = set()
                    new_ex_object_set[pro_key] |= set(eos[4])
                ex_object_set = set()
                for key in new_ex_object_set:
                    production = (key[0], key[1], key[2], key[
                                  3], tuple(new_ex_object_set[key]))
                    ex_object_set.add(tuple(production))
            return ex_object_set

        set_id = 0
        new_node = create_get_lr_dfa_node(set_id)
        object_set = expand_production(
            self, (0, 'start1', ('start',), 0, '#'), set())
        new_node.add_object_set_by_set(object_set)
        all_object_set[tuple(object_set)] = set_id
        all_status[set_id] = new_node
        object_set_queue = list()
        object_set_queue.append(new_node)
        while object_set_queue:
            top_object_node = object_set_queue.pop(0)
            old_set = top_object_node.object_set
            old_set_id = top_object_node.set_id
            # print 'object_set_id =', old_set_id
            for cur_production in old_set:
                # print cur_production
                pro_id = cur_production[0]
                left = cur_production[1]
                right = cur_production[2]
                point_index = cur_production[3]
                tail_set = cur_production[4]
                if point_index >= len(right) or '$' in right:
                    if old_set_id not in self.lr_analyze_table:
                        self.lr_analyze_table[old_set_id] = {}
                    for tail in tail_set:
                        if tail in self.lr_analyze_table[old_set_id]:
                            print 'the grammar is not a LR(1) grammar!!!'
                            return
                        self.lr_analyze_table[old_set_id][tail] = ('r', pro_id)
                else:
                    tar_set_id = 0
                    new_production = (pro_id, left, right,
                                      point_index + 1, tail_set)
                    new_object_set = expand_production(
                        self, new_production, set())
                    if tuple(new_object_set) in all_object_set.keys():
                        tar_set_id = all_object_set[tuple(new_object_set)]
                    else:
                        set_id += 1
                        tar_set_id = set_id
                        all_object_set[tuple(new_object_set)] = set_id
                        new_node = create_get_lr_dfa_node(tar_set_id)
                        new_node.add_object_set_by_set(new_object_set)
                        all_status[tar_set_id] = new_node
                        object_set_queue.append(new_node)
                    if old_set_id not in self.lr_analyze_table:
                        self.lr_analyze_table[old_set_id] = {}
                    if right[point_index] in self.terminate:
                        self.lr_analyze_table[old_set_id][
                            right[point_index]] = ('s', tar_set_id)
                    else:
                        self.lr_analyze_table[old_set_id][
                            right[point_index]] = ('g', tar_set_id)
        self.DFA.status = all_status

    def run_on_lr_dfa(self, tokens,tokens_value,output_file_name):
        f = open(output_file_name, "w")
        doc = minidom.Document()
        rootNode = doc.createElement("Program")
        doc.appendChild(rootNode)
        status_stack = [0]
        symbol_stack = ['#']
        token_tree_stack=[]
        symbol_tree_stack=[]
        top = 0
        success = False
        #字符串反向变为堆栈，栈顶为最后一个元素，方便出栈
        tokens.reverse()
        tokens_value.reverse()
        for i in range(0,len(tokens)):
            childNode =doc.createElement(tokens[i])
            childvalueNode = doc.createTextNode(tokens_value[i])
            childNode.appendChild(childvalueNode)
            token_tree_stack.append(childNode)
        while not success:
            top = status_stack[-1]
            # 字符串栈顶元素
            #print 'token =', tokens[-1]
            # 打印 符号栈
            #print symbol_stack
            #print self.lr_analyze_table[top]
            # 打印 状态栈
            #print status_stack

            if tokens[-1] in self.lr_analyze_table[top]:
                action = self.lr_analyze_table[top][tokens[-1]]
                if action[0] == 's':
                    #如果是移进，符号栈和状态栈都移进
                    status_stack.append(action[1])
                    symbol_stack.append(tokens[-1])
                    symbol_tree_stack.append(token_tree_stack[-1])
                    #终结谷出栈
                    token_tree_stack=token_tree_stack[:-1]
                    tokens = tokens[:-1]
                elif action[0] == 'r':
                    if action[1] == 0:
                        #如果为接受,通过堆栈输出xml文件
                        rootNode.appendChild(symbol_tree_stack[-1])
                        doc.writexml(f, '\t', '\t', '\n', "utf-8")
                        print ' Syntax anaysis successfully!'
                        success = True
                        break
                    #如果是规约项目，进行规约
                    production = self.productions[action[1]]
                    #print production
                    left = production.keys()[0]
                    right_len = len(production[left])
                    tokens.append(left)
                    #print left
                    fatherNode = doc.createElement(left)
                    if production[left] == ['$']:
                        token_tree_stack.append(fatherNode)
                        rootNode.appendChild(fatherNode)
                        continue
                    #同时，符号栈和状态栈均出栈
                    temp_stack = []
                    for i in range(0,right_len):
                        temp_stack.append(symbol_tree_stack[-1])
                        symbol_tree_stack = symbol_tree_stack[:-1]
                    for i in range(0,right_len):
                        fatherNode.appendChild(temp_stack.pop())
                    token_tree_stack.append(fatherNode)
                    status_stack = status_stack[:-right_len]
                    symbol_stack = symbol_stack[:-right_len]
                else:
                    #goto 表
                    status_stack.append(action[1])
                    symbol_stack.append(tokens[-1])
                    symbol_tree_stack.append(token_tree_stack[-1])
                    #非终结符出栈
                    token_tree_stack=token_tree_stack[:-1]
                    tokens = tokens[:-1]
                # print status_stack, symbol_stack
            else:
                #如果分析表中没有，就报错，并输出错误信息
                print tokens
                print status_stack
                print symbol_stack
                print self.lr_analyze_table[top]
                print 'Syntax error!\n'
                break

    def read_and_analyze(self, input_path,output_path):
        dom = minidom.parse(input_path)
        table  =  dom.getElementsByTagName( "tokens" )[0].getElementsByTagName("token")
        tokens_type = []
        tokens_value=[]
        for tokenlist in table:
            tokens_type.append(tokenlist.getElementsByTagName( "type" )[0].childNodes[0].data)
            tokens_value.append(tokenlist.getElementsByTagName( "value" )[0].childNodes[0].data)
        tokens_type.append("#")
        tokens_value.append("#")
        self.run_on_lr_dfa(tokens_type,tokens_value,output_path)



def main(input_argv=None):
    '''
    主函数
    '''
    # 若定义了输入文件名
    input_path = os.path.abspath('./data/test.token.xml')
    output_path = os.path.abspath('./data/test.tree.xml')
    if len(input_argv) > 1:
        #获取绝对路径
        input_path = os.path.abspath(input_argv[1])
    else:
        if os.name == 'nt':
            input_path = os.path.abspath('.\\data\\test.token.xml')
        else:
            input_path = os.path.abspath('./data/test.token.xml')
    #若定义了输出文件名
        if len(input_argv) > 2:
            output_path = os.path.abspath(input_argv[2])
        else:
            if os.name == 'nt':
                output_path = os.path.abspath('.\\data\\test.tree.xml')
            else:
                output_path = os.path.abspath('./data/test.tree.xml')

    #语法分析的类
    syn_ana = SyntaxAnalyze()
    #通过‘syn_grammar.txt构建语法规则
    syn_ana.read_syntax_grammar('./data/c_syntax.txt')
    # 得到文法的非终结符和终结符
    syn_ana.get_terminate_noterminate()
    # 初始化文法的first集合
    syn_ana.init_first_set()
    # 构建项目集DFA，并且构建分析表
    syn_ana.create_lr_dfa()
    #print syn_ana.lr_analyze_table
    # 通过分析表进行分析
    syn_ana.read_and_analyze(input_path,output_path)


    return


if __name__ == "__main__":
    # 调用主函数
    main(sys.argv)
