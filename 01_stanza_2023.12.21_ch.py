# -*- coding: utf-8 -*-
#2023-2-16使用stanza分析多语言数据
#copyright @liwenping

#import re
import os
import stanza

nlp = stanza.Pipeline(lang = "zh-hans", download_method = None)

folder_input = '01_utf8'
folder_output = '02_stanza'

sentence_counter = 0


# 读入数据并制作单词列表
filenames = os.listdir(folder_input)
for filename in filenames:

  sentence_counter = 0
  filename1 = filename.replace('.txt', '_stanza.txt')

  header = True
  words = ''
  datafile = open(folder_input+'/'+filename, encoding='utf-8-sig')
  outputfile1 = open(folder_output+'/'+filename1, 'w', encoding = 'utf-8')
  
  print(
    "sentence_id",
    "dependent_id",
    "dependent",
    "dep_lemma",
    "UPOS",
    "XPOS",
    "head_id",
    "dependency_type",
    "dependency_distance",
    "dd_abs",
    sep = '\t',
    file = outputfile1
  )
  
  for line in datafile:

    line = line.rstrip()
  
    if header:     #取首行作为字典列表的关键词keys
      header = False
      continue
      
    
    doc3 = nlp(line)
    

    for sentence in doc3.sentences:
      for word in sentence.words:
        dd = int(word.head) - int(word.id)
        dd_abs = abs(dd)
        print(str(sentence.index+1+sentence_counter)+'\t'+str(word.id) +'\t' + str(word.text) + '\t' + str(word.lemma) + '\t' + str(word.upos) + '\t' + str(word.xpos) + '\t' + str(word.head) + '\t' + str(word.deprel)+'\t'+str(dd)+'\t'+str(dd_abs), file = outputfile1)
      print("EOS", file = outputfile1)
      sentence_counter += 1
      
      
      
    


