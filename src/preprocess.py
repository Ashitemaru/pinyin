import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import json
import re

dict_path = ''
raw_file_path = ''
final_path = ''

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
    if len(sys.argv) != 5:
        print('Error!')
        return

    char_num = 0
    try:
        char_num = int(sys.argv[4])
    except ValueError:
        print('Illegal num!')
    char_num -= 1

    global raw_file_path, final_path, dict_path
    raw_file_path, final_path, dict_path = sys.argv[1], sys.argv[2], sys.argv[3]

    # Get all the legal hanzi
    hanzi_set = get_hanzi_table()

    corpus_handler = open(raw_file_path, 'r')
    final_handler = open(final_path, 'w')
        
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
            final_handler.write('^' * char_num + part + '$' * char_num + '\n')

if __name__ == '__main__':
    data_filter()