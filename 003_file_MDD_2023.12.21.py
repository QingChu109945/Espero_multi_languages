# -*- coding: utf-8 -*-
#2022-4-29输出句子并计算句子的dependency distance
#2022-12.21在原来程序的基础上，增加输出每个文件的MDD，使用>保存
#copyright @liwenping

import re
import os
#folder_input = '02_txt'
#folder_output = '04_text'

folder_input = '03_stanza_no_punct'
folder_output = '04_MDD'

sentence_counter = 1

words = ''
dd_sum = 0
dependency_relation = 0
mdd_sentence = 0
head_initial = 0
head_final = 0

file_dd_sum = 0
file_dependency_relation = 0
file_mdd = 0
file_head_initial = 0
file_head_final = 0

outputfile2 = open('00_file_MDD.txt', 'w', encoding = 'utf-8')

print(
  'filename',
  'file_dd_sum',
  'file_dependency_relation',
  'file_mdd_sentence',
  'file_HI',
  'file_HF',
  'file_HI_per',
  'file_HF_per',
  sep = '\t',
  file = outputfile2,
)


# 读入数据并制作单词列表
filenames = os.listdir(folder_input)
for filename in filenames:
  
  filename1 = filename.replace('_stanza_nopunct.txt', '_dd.txt')

  sentence_counter = 1
  words = ''
  dd_sum = 0
  dependency_relation = 0
  mdd_sentence = 0
  head_final = 0
  head_initial = 0
  
  
  
  file_dd_sum = 0
  file_dependency_relation = 0
  file_mdd = 0
  file_head_initial = 0
  file_head_final = 0
  
  file_head_final_per = 0
  file_head_initial_per = 0
  
  header = True
  words = ''
  datafile = open(folder_input+'/'+filename, encoding='utf-8-sig')
  outputfile1 = open(folder_output+'/'+filename1, 'w', encoding = 'utf-8')
  
  
  print(
    'sentence_id',
    'sentence',
    'dd_sum',
    'dependency_relation',
    'mdd_sentence',
    'HI',
    'HF',
    'HI_per',
    'HF_per',
    sep = '\t',
    file = outputfile1,
  )
  
  for line in datafile:

    line = line.rstrip()
  
    if header:     #取首行作为字典列表的关键词keys
      header = False
      continue
      

    colmuns = line.split('\t')
    marker = colmuns[0]


    if marker == "EOS":
      print(
        sentence_counter,
        words,
        dd_sum,
        dependency_relation,
        mdd_sentence,
        head_initial,
        head_final,
        head_initial_per,
        head_final_per,
        sep = '\t',
        file = outputfile1,
      )
        
      sentence_counter+= 1
      words = ''
      dd_sum = 0
      dependency_relation = 0
      mdd_sentence = 0
      head_initial = 0
      head_final = 0
      head_initial_per = 0
      head_final_per = 0
      
      
    
    else:
      if colmuns[1] == "":
        continue
      

      elif colmuns[4] == "PUNCT":
        dependent = colmuns[2]
        words += dependent
      
#      elif colmuns[7] == "root":
#        dependent = colmuns[2]
#        words += dependent
        


      else:      
        dependent = colmuns[2]
        words += dependent
      
        dependent_id = int(colmuns[1])
        head_id = int(colmuns[6])
        dependency_distance = head_id - dependent_id
        dependency_distance_abs = abs(dependency_distance)
      
      
      
      
        if not head_id == 0:
          dd_sum += dependency_distance_abs
          dependency_relation += 1
          file_dd_sum += dependency_distance_abs
          file_dependency_relation += 1
          
          if dependency_distance > 0:
            head_final += 1
            file_head_final += 1
          
          if dependency_distance < 0:
            head_initial += 1
            file_head_initial += 1
            
        if not dependency_relation == 0:
          mdd_sentence = dd_sum/dependency_relation
          head_final_per = head_final/dependency_relation
          head_initial_per = head_initial/dependency_relation

  if not file_dependency_relation == 0:
    file_mdd = file_dd_sum/file_dependency_relation
    file_head_final_per = file_head_final/file_dependency_relation
    file_head_initial_per = file_head_initial/file_dependency_relation
  
  print(
    filename,
    file_dd_sum,
    file_dependency_relation,
    file_mdd,
    file_head_initial,
    file_head_final,
    file_head_initial_per,
    file_head_final_per,
    sep = '\t',
    file = outputfile2,
  )
        
      #print(str(sentence_counter) + '\t' +line, file = outputfile1)
      #print(line, file = outputfile1)


