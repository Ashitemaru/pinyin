'''
    The module used to train the model.
    Usage: python3 train.py <size_of_char_tuples>
'''

import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm

corpus_path_prefix = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/double_corpus/news-'
corpus_index_list = ['02', '04', '05', '06', '07', '08', '09', '10', '11']
corpus_path_suffix = '.txt'

final_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/json/double.json'

def main():
    if len(sys.argv) != 2:
        print('Error!')
        return

    char_num = 0
    try:
        char_num = int(sys.argv[1])
    except ValueError:
        print('Illegal num!')
    char_num -= 1

    # The double dictionary
    static = {}

    # Sum all things up
    for i in corpus_index_list:
        corpus_handler = open(corpus_path_prefix + i + corpus_path_suffix, 'r')
        sentence_list = corpus_handler.readlines()

        # Get the statistics of every sentence
        for sentence in tqdm(sentence_list):
            for ind in range(len(sentence) - char_num):
                # If the starting hanzi is not in the dict, create it
                if not sentence[ind: ind + char_num] in static:
                    static[sentence[ind: ind + char_num]] = {
                        'total': 0,
                    }
                
                # If the double is not in the dict, create it
                if not sentence[ind: ind + char_num + 1] in static[sentence[ind: ind + char_num]]:
                    static[sentence[ind: ind + char_num]][sentence[ind: ind + char_num + 1]] = 0
                
                # Add the number up
                static[sentence[ind: ind + char_num]][sentence[ind: ind + char_num + 1]] += 1
                static[sentence[ind: ind + char_num]]['total'] += 1
        
    final_json_handler = open(final_path, 'w')
    final_json_handler.write(str(static))

if __name__ == '__main__':
    main()