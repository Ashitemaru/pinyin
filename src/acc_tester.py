import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm

output_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/test/output.txt'
tgt_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/test/answer.txt'

def get_right_chars(o, t):
    acc = 0
    for i, char in enumerate(o):
        acc += 1 if char == t[i] else 0
    return acc

def main():
    output_handler = open(output_file_path, 'r')
    tgt_handler = open(tgt_file_path, 'r')

    output_lines = output_handler.readlines()
    tgt_lines = tgt_handler.readlines()

    assert len(output_lines) == len(tgt_lines)

    sen_acc = 0
    char_acc = 0
    tot_char = 0
    for i, output_sen in enumerate(output_lines):
        output_sen = output_sen.replace('\n', '')
        tgt_sen = tgt_lines[i].replace('\n', '')

        sen_acc += 1 if output_sen == tgt_sen else 0

        assert len(output_sen) == len(tgt_sen)

        tot_char += len(output_sen)
        char_acc += get_right_chars(output_sen, tgt_sen)
    
    print('The char accuracy is %lf%%, The sentence accuracy is %lf%%.' % (
        char_acc / tot_char * 100,
        sen_acc / len(output_lines) * 100
    ))

if __name__ == '__main__':
    main()