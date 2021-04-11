import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm

corpus_path = ''
final_path = ''

def main():
    if len(sys.argv) != 4:
        print('Error!')
        return

    char_num = 0
    try:
        char_num = int(sys.argv[3])
    except ValueError:
        print('Illegal num!')
        return
    char_num -= 1

    global corpus_path, final_path
    corpus_path, final_path = sys.argv[1], sys.argv[2]

    # The dictionary
    static = {}

    corpus_handler = open(corpus_path, 'r')
    sentence_list = corpus_handler.readlines()

    # Get the statistics of every sentence
    for sentence in tqdm(sentence_list):
        for ind in range(len(sentence) - char_num):
            # If the starting hanzi is not in the dict, create it
            if not sentence[ind: ind + char_num] in static:
                static[sentence[ind: ind + char_num]] = {
                    'total': 0,
                }
                
            # If the tuple is not in the dict, create it
            if not sentence[ind: ind + char_num + 1] in static[sentence[ind: ind + char_num]]:
                static[sentence[ind: ind + char_num]][sentence[ind: ind + char_num + 1]] = 0
                
            # Add the number up
            static[sentence[ind: ind + char_num]][sentence[ind: ind + char_num + 1]] += 1
            static[sentence[ind: ind + char_num]]['total'] += 1
        
    final_json_handler = open(final_path, 'w')
    final_json_handler.write(str(static))

if __name__ == '__main__':
    main()