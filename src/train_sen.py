'''
    The module used to train the model. This model is based on phrases.
    We let the size_of_phrase_tuple be fixed as 2.
    Usage: python3 train_sen.py
'''

import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import jieba

corpus_path_prefix = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/double_corpus/news-'
corpus_index_list = ['02', '04', '05', '06', '07', '08', '09', '10', '11']
corpus_path_suffix = '.txt'

final_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/json/double_sen.json'

def main():
    if len(sys.argv) != 1:
        print('Error!')
        return

    # The dictionary
    static = {}

    # Sum all things up
    for i in corpus_index_list:
        corpus_handler = open(corpus_path_prefix + i + corpus_path_suffix, 'r')
        sentence_list = corpus_handler.readlines()

        # Get the statistics of every sentence
        for sentence in tqdm(sentence_list):

            # Tokenize the sentence with jieba
            phrase_list = list(jieba.tokenize(sentence.strip()))
            phrase_list = list(map(lambda x: x[0], phrase_list))

            for ind in range(len(phrase_list) - 1):

                # If the starting phrase is not in the dict, create it
                if not phrase_list[ind] in static:
                    static[phrase_list[ind]] = {
                        'total': 0,
                    }
                
                # If the tuple is not in the dict, create it
                if not phrase_list[ind] + phrase_list[ind + 1] in static[phrase_list[ind]]:
                    static[phrase_list[ind]][phrase_list[ind] + phrase_list[ind + 1]] = 0
                
                # Add the number up
                static[phrase_list[ind]][phrase_list[ind] + phrase_list[ind + 1]] += 1
                static[phrase_list[ind]]['total'] += 1
        
    final_json_handler = open(final_path, 'w')
    final_json_handler.write(str(static))

if __name__ == '__main__':
    main()