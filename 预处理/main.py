# encoding=utf-8
import jieba
import jieba.analyse
import sys

raw_str = ''
with open('.\预处理\source.txt') as f:
    raw_str = f.read()

#库实现
print('调用包结果：')
tf_idf = jieba.analyse.extract_tags(raw_str, topK=10, withWeight=True)
for x,w in tf_idf:
    print('%s %s' %(x, w)) 

#手动实现
print('手动实现结果：')
words = jieba.lcut(raw_str)
stopwords = [line.strip() for line in open('.\预处理\stopwords.txt', 'r', encoding='utf-8').readlines()]  # 这里加载停用词的路径
outstr = []
for word in words:
    if word not in stopwords:
        if word != '\n':
            outstr.append(word)

#IDF文件读入
idf_dict = {}
with open('.\预处理\idf.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        tmp = line.strip().split(' ')
        idf_dict[tmp[0]] = float(tmp[1])
default_idf = sorted(idf_dict.values())[len(idf_dict)//2] #不存在则取中位数

#统计词频，可使用collections包，这里自己实现
total = len(outstr)
word_freq = {}
for word in outstr:
    if(word in word_freq):
        word_freq[word] += 1
    else:
        word_freq[word] = 1
for k,v in word_freq.items():
    idf = idf_dict.get(k, default_idf)
    word_freq[k] = v*idf/total
result = sorted(word_freq.items(), key=lambda x:x[1], reverse=True)
result = result[:10]
for k,v in result:
    print('%s %f' %(k, v))    