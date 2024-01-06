# -*- coding: utf-8 -*-
#以CaboCha输出结果为对象，计算句子结构特征值
#自己用输出每层几个节点；输出节点最多层，及其节点数；满足批处理
#第一层为0层的输出形式
#需要添加标点符号的判断
#copyright @ LIWenping

class Node:
    def __init__(self, index):
        self.index = index
        self.children = []


def generate_syntax_tree(dependencies):
    nodes = [Node(i) for i in range(len(dependencies) + 1)]

    for dep in dependencies:
        child_index = dep
        parent_index = dependencies[dep]
        nodes[int(parent_index)].children.append(nodes[int(child_index)])

    return nodes[0]


def get_level_counts(root):
    level_counts = []
    queue = [root]

    max_node_count = 0  # 最多节点数
    max_node_level = 0  # 最多节点数的层级

    level = 0

    while queue:
        level_count = len(queue)
        level_counts.append((level_count, [node.index for node in queue]))

        if level_count > max_node_count:
            max_node_count = level_count
            max_node_level = level

        for _ in range(level_count):
            node = queue.pop(0)
            queue.extend(node.children)

        level += 1

    return level_counts, max_node_level, max_node_count


def get_max_depth(root):
    if not root.children:
        return 0

    max_depth = 0
    for child in root.children:
        max_depth = max(max_depth, get_max_depth(child))

    return max_depth + 1

###########################################

import os

folder_input = '03_stanza_no_punct'
folder_output = '05_SSCV_MHD2016'

filenames = os.listdir(folder_input)
for filename in filenames:

  filename1 = filename.replace('_stanza_nopunct.txt', '_sscv.txt')
  
  sentence_counter = 1
  words = ''
  hd_sum = 0
  dependency_relation = 0
  sscv_sentence = 0
  mhd_2016_sentence = 0
  dependencies = {}
  
  header = True
  
  datafile = open(folder_input+'/'+filename, encoding='utf-8-sig')
  outputfile1 = open(folder_output+'/'+filename1, 'w', encoding = 'utf-8')
  
  print(
    "filename",
    "sentence_id",
    "sentence",
    "hd_sum",
    "dependent_relations",
    "SSCV",
    "mhd_2016_sentence",
    sep = '\t',
    file = outputfile1
  )
  
  for line in datafile:
    line = line.strip()
    
    #如果包含列名，则跳过文件首行
    if header:         
      header = False
      continue

    colmuns = line.split('\t')
    marker = colmuns[0]

      
    if marker == 'EOS':
      #print(dependencies)
      try:
        syntax_tree = generate_syntax_tree(dependencies)
        level_counts, max_node_level, max_node_count = get_level_counts(syntax_tree)
        
        level_counts.pop(0)     #level_counts多了0节点，将其弹出
        #print(level_counts)
        for i, (count, indices) in enumerate(level_counts):
          hd_sum += i * count    #第一层为0层；第一层为1层的话，需要i+1
          dependency_relation += count
        
        if not dependency_relation == 0:
          sscv_sentence = hd_sum/dependency_relation
        else:
          sscv_sentence = ''
        
        if not dependency_relation == 1:
          mhd_2016_sentence = hd_sum/(dependency_relation - 1)
        else:
          mhd_2016_sentence = ''
        print(
          filename,
          sentence_counter,
          words,
          hd_sum,
          dependency_relation,
          sscv_sentence,
          mhd_2016_sentence,
          sep = '\t',
          file = outputfile1
        )
        words = ''
        hd_sum = 0
        dependency_relation = 0
        sscv_sentence = 0
        mhd_2016_sentence = 0
        sentence_counter += 1
        
#        for i, (count, indices) in enumerate(level_counts):
#          indices_str = '\t'.join(str(idx) for idx in indices)
#          print(f"Level {i}: {count} nodes - {indices_str}", sep = '\t',file = outputfile1)    #第一层为0层的输出形式
        
        # 输出最多节点数的层级和节点数
#        print(f"Max nodes: Level {max_node_level - 1} - {max_node_count} nodes", sep = '\t',file = outputfile1)    #第一层为0层的输出形式
        
        # 输出最大深度
#        max_depth = get_max_depth(syntax_tree)
#        print(f"Max depth: {max_depth - 1}", sep = '\t',file = outputfile1)    #第一层为0层的输出形式
  
        #清空字典
        dependencies = {}

      except:
        words = ''
        hd_sum = 0
        dependency_relation = 0
        sscv_sentence = 0
        mhd_2016_sentence = 0
        dependencies = {}
        
  
    else:
#      if colmuns[1] == "":
#        continue
        
#      if colmuns[4] == "PUNCT":
#        continue
      
      dependent_id = colmuns[1]
      dependent = colmuns[2]
      head_id = colmuns[6]
      #head = colmuns[7]
  
      #使用words变量保存原句信息
      words += dependent
      #使用dependencies字典列表构建句法树
      dependencies[dependent_id] = head_id

