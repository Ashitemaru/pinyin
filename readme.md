## 拼音输入法大作业

### 所需依赖

- `tqdm`模块，用于显示进度条

### 各文件解释

- `src/preprocess.py`用于清洗数据中的非法字符，运行方法为：

```shell
python3 preprocess.py <raw_file_path> <target_path> <hanzi_path> <size_of_tuples>
```

后面四个参数分别表示：原文件路径、目标路径、记录合法字符的文件路径、使用字几元模型。

**这里数据原文件因为过大不上传。**

- `src/train.py`用于统计数据，运行方法为：

```shell
python3 train.py <corpus_file_path> <target_path> <size_of_tuples>
```

后面三个参数分别表示：语料库路径、目标路径、使用字几元模型。

- `src/double.py`以及`src/final.py`分别为字二元以及混合字元模型，运行方法为：

```shell
python3 double.py <input> <output> <pinyin_to_hanzi> <json>
```

后面四个参数分别表示：输入文件路径、输出文件路径、拼音到汉字的转换文件路径、统计词频的`json`文件路径。

```shell
python3 double.py <input> <output> <pinyin_to_hanzi> <double_json> <triple_json>
```

后面五个参数分别表示：输入文件路径、输出文件路径、拼音到汉字的转换文件路径、统计二元词频的`json`文件路径、统计三元词频的`json`文件路径。

### 使用方法

首先准备语料并预处理，之后将预处理后的语料送入数据统计程序，生成的`json`文件即可用于最后的模型生成。