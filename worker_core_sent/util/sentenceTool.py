import jieba
import jieba.posseg as pseg
import re
import json

word_tags = {}
with open("./util/dict.txt") as f:
# with open("./dict.txt") as f:
  for line in f.readlines():
    line = line.replace("\n", "")
    if len(line)>0:
      word,_,tag = line.split(" ")
      jieba.add_word(word)
      word_tags[word] = tag


with open("./util/addition_dict.txt") as f:
# with open("./addition_dict.txt") as f:
  for line in f.readlines():
    line = line.replace("\n","")
    if len(line) > 0:
      word,tag,_ = line.split(" ")
      jieba.add_word(word)
      word_tags[word] = tag


with open("./util/dict.txt") as f:
# with open("./tfidf.json") as f:
  tfidf = json.load(f)


def keep_zh(sent):
  cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z]")  # 保留中英
  sent = cop.sub(' ', sent)  # 将string1中匹配到的字符替换成空字符
  return sent


def sent_cut(sent):
  sent = keep_zh(sent)
  return [i for i in jieba.cut(sent) if i != " "]


def keep_tag_N_A_V(word):
  if word in word_tags:
    tag = word_tags[word]
    if tag.startswith("N") or tag.startswith("V") or tag == "A":
      return [(word,tag)]
  else:
    word = pseg.cut(word)
    word = [(w.word ,w.flag) for w in word]
    rearr = []
    for w,tag in word:
      if tag.startswith("N") or tag.startswith("V") or tag == "A":
        rearr.append((w, tag))

def find_tfidf(word):
  if word in tfidf:
    return tfidf[word]
  else:
    return 0.0

def is_important_word(word):
  words = keep_tag_N_A_V(word)
  return_arr= []
  for w,t in words:
    score = find_tfidf(w)
    if score > 25:
      return_arr.append((w,t,score))

  return is_important_word

# print(keep_tag_N_A_V("國道"))
# print(keep_tag_N_A_V("兩個月"))
