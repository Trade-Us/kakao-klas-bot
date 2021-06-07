import sys
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def save_txt(output,i):
    sys.stdout = open('./data/output'+str(i)+'.txt', 'w')
    print(output)
    
    sys.stdout.close()

def extractor(output):
    okt = Okt()
    noun = okt.nouns(output)
    count = Counter(noun)
    
    noun_list = count.most_common(100)
    print(sorted(count.items(), key=lambda kv : kv[1], reverse=True)[:3])
    
    wc = WordCloud(font_path='./테트리스M.ttf', background_color="white", width=1000, height=1000, max_words=100, max_font_size=300)
    wc.generate(output)
    # plt.figure(figsize=(10, 8))
    # plt.imshow(wc)
    # plt.tight_layout(pad=0)
    # plt.axis('off')
    # plt.show()
    wc.to_file('wordcloud_outputs.png')

