# -*- coding: utf-8 -*-
#以06_dependency_seikei文件为对象，删除PUNCT，SYM，X的同时，调整dependent ID和head ID
#在2023.11.15.py的基础上，使用try, except，忽略那些有问题的句子
#copyright @liwenping

import re
import os
#folder_input = '02_txt'
#folder_output = '04_text'

folder_input = '02_stanza'
folder_output = '03_stanza_no_punct'

header = True

#定义一些需要的变量
dependent_id_list = []
dependent_list = []
dependent_lemma_list = []
upos_list = []
xpos_list = []
head_id_list = []
dependency_type_list = []
#new_dependent_list = []
#dependency_distance_list = []
#dd_abs_list = []
original_id_head_dict = {}    #原ID和原head字典
new_id_original_id_dict = {}    #新ID和原ID的字典
reverse_new_id_original_id_dict = {}    #原ID和新ID的字典

sentence_counter = 1

#head_list = []



# 读入数据并制作单词列表
filenames = os.listdir(folder_input)
for filename in filenames:
  
  header = True
  filename1 = filename.replace('_stanza.txt', '_stanza_nopunct.txt')

#  wo_forword_head_id = 0
#  ni_forword_head_id = 0
#  ga_forword_head_id = 0
#  wo_dep_id = 0
#  ni_dep_id = 0
#  ga_dep_id = 0
  
  sentence_counter = 1
  new_dependent_counter = 1
  
  words = []
  datafile = open(folder_input+'/'+filename, encoding='utf-8')
  outputfile1 = open(folder_output+'/'+filename1, 'w', encoding = 'utf-8')
  
  print(
      #'filename',
      'sentence_ID',
      'dependent_ID',
      'dependent',
      'dependent_lemma',
      'dependent_UPOS',
      'dependent_XPOS',
      'head_ID',
#      'head',
#      'head_lemma',
#      'head_UPOS',
#      'head_XPOS',
      'dependency_type',
#      'dependency_distance',
#      'dd_abs',
      sep = '\t',
      file = outputfile1
  )


  for line in datafile:

    line = line.rstrip()
  
    if header:     #取首行作为字典列表的关键词keys
      header = False
      continue
      
    values = line.split('\t')     #取首行以外的行作为值values
    
    marker = values[0]
    
    

    if not values[0] == "EOS":    #判断句子是否结束，如果未结束，则构建句子字典。
      #filename_in = values[0]
      #sentence_id = values[1]
      dependent_id = int(values[1])
      dependent = values[2]
      dependent_lemma = values[3]
      dependent_upos = values[4]
      dependent_xpos = values[5]
      head_id = int(values[6])
      dependency_type = values[7]
      #dependency_distance = int(values[8])
      #dd_abs = int(values[9])
      
      original_id_head_dict[dependent_id] = head_id
      
      if dependent_upos == 'PUNCT' or dependent_upos == 'SYM' or dependent_upos == 'X':
      #if dependent_upos == 'PUNCT':
        continue
      else:
        dependent_id_list.append(dependent_id)
        dependent_list.append(dependent)
        dependent_lemma_list.append(dependent_lemma)
        upos_list.append(dependent_upos)
        xpos_list.append(dependent_xpos)
        head_id_list.append(head_id)
        dependency_type_list.append(dependency_type)
        
        new_id_original_id_dict[new_dependent_counter] = dependent_id
        reverse_new_id_original_id_dict[dependent_id] = new_dependent_counter
        
        new_dependent_counter+= 1
        
      
    try:
      if values[0] == "EOS":    #如果句子结束，则进行条件判断
        #MDD = sentence_dd_sum/count
      
        for j in range(len(dependent_list)):
          
          if not original_id_head_dict[new_id_original_id_dict[j+1]] == 0:
            print(
              #filename,
              sentence_counter,
              j + 1,
              dependent_list[j],
              dependent_lemma_list[j],
              upos_list[j],
              xpos_list[j],
              reverse_new_id_original_id_dict[original_id_head_dict[new_id_original_id_dict[j+1]]],    #原来head ID对应的新的dependent ID
              dependency_type_list[j],
              sep = '\t',
              file=outputfile1
            )
          else:
            print(
              #filename,
              sentence_counter,
              j + 1,
              dependent_list[j],
              dependent_lemma_list[j],
              upos_list[j],
              xpos_list[j],
              0,    #原来head ID对应的新的dependent ID
              dependency_type_list[j],
              sep = '\t',
              file=outputfile1
            )
          
        print(
          #filename,
          'EOS',
          sep = '\t',
          file=outputfile1
        )

      
        dependent_id_list = []
        dependent_list = []
        dependent_lemma_list = []
        upos_list = []
        xpos_list = []
        head_id_list = []
        dependency_type_list = []
        dependency_distance_list = []
        original_id_head_dict = {}    #原ID和原head字典
        new_id_original_id_dict = {}    #新ID和原ID的字典
        reverse_new_id_original_id_dict = {}    #原ID和新ID的字典
        new_dependent_counter = 1
        sentence_counter+= 1

    except:
      dependent_id_list = []
      dependent_list = []
      dependent_lemma_list = []
      upos_list = []
      xpos_list = []
      head_id_list = []
      dependency_type_list = []
      dependency_distance_list = []
      original_id_head_dict = {}    #原ID和原head字典
      new_id_original_id_dict = {}    #新ID和原ID的字典
      reverse_new_id_original_id_dict = {}    #原ID和新ID的字典
      new_dependent_counter = 1
      
      
      
