import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import json
import re

dict_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/dictionary/hanzi_table.txt'

corpus_path_prefix = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/sina_news/news-'
corpus_index_list = ['02', '04', '05', '06', '07', '08', '09', '10', '11']
corpus_path_suffix = '.txt'

final_path_prefix = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/corpus/news-'

punctuation_regex = r'[，。、！？《》“”（）\(\)@#¥%&*～；【】「」｜：\.,a-zA-Z0-9\{\}\[\]\\<>~`\$\^-_—+=|;:\'\"!?]'

def get_hanzi_table():
    dict_handler = open(dict_path, 'r')
    raw_str = dict_handler.readlines()[0]

    hanzi_set = set([])
    for hanzi in raw_str:
        hanzi_set.add(hanzi)
    return hanzi_set

def filter_legal_hanzi(raw_str, table):
    # Split the sentence by punctuations, numbers & letters
    splited_str = re.split(punctuation_regex, raw_str)

    # Remove null strings & remove all the spaces
    splited_str = list(filter(lambda x: len(x.replace(' ', '')) > 0, splited_str))
    splited_str = list(map(lambda x: x.replace(' ', ''), splited_str))

    # Filter illegal hanzi
    def is_legal_sentence(origin_str):
        for char in origin_str:
            if not char in table:
                return False
        return True
    
    splited_str = list(filter(is_legal_sentence, splited_str))

    return splited_str

def data_filter():
    # Get all the legal hanzi
    hanzi_set = get_hanzi_table()

    for i in corpus_index_list:
        corpus_handler = open(corpus_path_prefix + i + corpus_path_suffix, 'r')
        final_handler = open(final_path_prefix + i + corpus_path_suffix, 'w')
        
        for raw_json_str in tqdm(corpus_handler.readlines()):
            # Get the content of the news
            sentence_json = json.loads(raw_json_str)
            news_content = sentence_json['html']
            news_title = sentence_json['title']

            # Filter the legal hanzi
            sentence_list = []
            sentence_list += filter_legal_hanzi(news_content, hanzi_set)
            sentence_list += filter_legal_hanzi(news_title, hanzi_set)

            # Write it into files
            for part in sentence_list:
                final_handler.write('#' + part + '\n')

if __name__ == '__main__':
    data_filter()