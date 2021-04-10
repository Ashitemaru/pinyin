import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm

corpus_path_prefix = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/corpus/news-'
corpus_index_list = ['02', '04', '05', '06', '07', '08', '09', '10', '11']
corpus_path_suffix = '.txt'

final_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/json/double.json'

def main():
    # The double dictionary
    static = {}

    # Sum all things up
    for i in corpus_index_list:
        corpus_handler = open(corpus_path_prefix + i + corpus_path_suffix, 'r')
        sentence_list = corpus_handler.readlines()

        # Get the statistics of every sentence
        for sentence in tqdm(sentence_list):
            for ind in range(len(sentence) - 1):
                # If the starting hanzi is not in the dict, create it
                if not sentence[ind] in static:
                    static[sentence[ind]] = {
                        'total': 0,
                    }
                
                # If the double is not in the dict, create it
                if not sentence[ind: ind + 2] in static[sentence[ind]]:
                    static[sentence[ind]][sentence[ind: ind + 2]] = 0
                
                # Add the number up
                static[sentence[ind]][sentence[ind: ind + 2]] += 1
                static[sentence[ind]]['total'] += 1
        
    final_json_handler = open(final_path, 'w')
    final_json_handler.write(str(static))

if __name__ == '__main__':
    main()