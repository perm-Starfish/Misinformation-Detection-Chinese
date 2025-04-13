import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
import random

def shuffle():
    #shuffle rows
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)

    jieba_list_train = [] 
    jieba_list_test = [] 

    for i in range(0, len(x_train)):
        jieba_list_train.append(' '.join(jieba.cut(x_train[i], cut_all = False)))
    for j in range(0, len(x_test)):
        jieba_list_test.append(' '.join(jieba.cut(x_test[j], cut_all = False)))

    #words freqeuncy
    count_filter_vec = CountVectorizer()
    #stopword
    count_filter_train = count_filter_vec.fit_transform(jieba_list_train)
    count_filter_test = count_filter_vec.transform(jieba_list_test)

    #words freqeuncy
    tfidf_filter_vec = TfidfVectorizer()
    #stopword
    x_tfidf_filter_train = tfidf_filter_vec.fit_transform(jieba_list_train)
    x_tfidf_filter_test = tfidf_filter_vec.transform(jieba_list_test)

    return count_filter_train, count_filter_test, x_tfidf_filter_train, x_tfidf_filter_test, y_train, y_test

#read true data
t_frame = pd.read_csv("C:/FakeNews/true_data.csv")

#rename label
t_frame.rename(columns = {'內容':'content'}, inplace = True)

#drop
t_frame.drop(['標題', '附檔連結', '發布日期'], axis=1, inplace=True)

#sampling
#if random.randint(0, 1): copy the row to another frame
#delete the original frame (optional)

true_frame = pd.DataFrame(columns=['content', 'label'])
'''
for k in range(0, 4032):
    true_frame.loc[k] = t_frame.loc[k]
'''
t_cnt = 0
for k in range(0, 4032):
    if random.randint(0, 2)==0:
        true_frame.loc[t_cnt] = t_frame.loc[k]
        t_cnt += 1

#debug
search = "\n"
replace = ""

true_frame["label"] = 1

#create dataframe
false_frame = pd.DataFrame(columns=['content', 'label'])

#read false data
f_data = []
for i in range(0, 1288):
    n = "%04d" %i
    with open(r'C:/FakeNews/TFC/data_'+n+'.txt', 'r', encoding='UTF-8') as file:
        data = file.read()
        ndata = data[2:].replace(search, replace)
        idx = ndata.find("「錯誤」訊息")
        if idx!=-1:
            false_data = ndata[:idx]
        else:
            false_data = ndata
    false_frame.loc[i] = false_data, 0

#concat the two frames
all_frame = pd.concat([true_frame, false_frame], axis=0, ignore_index=True)

#dataframe convert to list
X = all_frame['content'].astype(str).tolist()
Y = all_frame['label'].tolist()

#function

MNBC_acc = MNBC_p = MNBC_r = MNBC_f1 = 0
MNBT_acc = MNBT_p = MNBT_r = MNBT_f1 = 0
svmC_acc = svmC_p = svmC_r = svmC_f1 = 0
svmT_acc = svmT_p = svmT_r = svmT_f1 = 0

#machine learning
for times in range(0, 10):
    count_filter_train, count_filter_test, x_tfidf_filter_train, x_tfidf_filter_test, y_train, y_test = shuffle()
    MNB_cnt = MultinomialNB()
    MNB_cnt.fit(count_filter_train, y_train)
    pre_ans = MNB_cnt.predict(count_filter_test)
    MNBC_acc += round(accuracy_score(y_test, pre_ans), 5)
    MNBC_p += round(precision_score(y_test, pre_ans), 5)
    MNBC_r += round(recall_score(y_test, pre_ans), 5)
    MNBC_f1 += round(f1_score(y_test, pre_ans), 5)

    MNB_tfidf = MultinomialNB()
    MNB_tfidf.fit(x_tfidf_filter_train, y_train)
    pre_ans = MNB_tfidf.predict(x_tfidf_filter_test)
    MNBT_acc += round(accuracy_score(y_test, pre_ans), 5)
    MNBT_p += round(precision_score(y_test, pre_ans), 5)
    MNBT_r += round(recall_score(y_test, pre_ans), 5)
    MNBT_f1 += round(f1_score(y_test, pre_ans), 5)

    svm_cnt = svm.SVC()
    svm_cnt.fit(count_filter_train, y_train)
    pre_ans = svm_cnt.predict(count_filter_test)
    svmC_acc += round(accuracy_score(y_test, pre_ans), 5)
    svmC_p += round(precision_score(y_test, pre_ans), 5)
    svmC_r += round(recall_score(y_test, pre_ans), 5)
    svmC_f1 += round(f1_score(y_test, pre_ans), 5)

    svm_tfidf = svm.SVC()
    svm_tfidf.fit(x_tfidf_filter_train, y_train)
    pre_ans = svm_tfidf.predict(x_tfidf_filter_test)
    svmT_acc += round(accuracy_score(y_test, pre_ans), 5)
    svmT_p += round(precision_score(y_test, pre_ans), 5)
    svmT_r += round(recall_score(y_test, pre_ans), 5)
    svmT_f1 += round(f1_score(y_test, pre_ans), 5)

print('MNB_Count')
print('accuracy: ', round(MNBC_acc/10, 4))
print('precision: ', round(MNBC_p/10, 4))
print('recall: ', round(MNBC_r/10, 4))
print('f1: ', round(MNBC_f1/10, 4))

print('MNB_Tfidf')
print('accuracy: ', round(MNBT_acc/10, 4))
print('precision: ', round(MNBT_p/10, 4))
print('recall: ', round(MNBT_r/10, 4))
print('f1: ', round(MNBT_f1/10, 4))

print('svm_Count')
print('accuracy: ', round(svmC_acc/10, 4))
print('precision: ', round(svmC_p/10, 4))
print('recall: ', round(svmC_r/10, 4))
print('f1: ', round(svmC_f1/10, 4))

print('svm_Tfidf')
print('accuracy: ', round(svmT_acc/10, 4))
print('precision: ', round(svmT_p/10, 4))
print('recall: ', round(svmT_r/10, 4))
print('f1: ', round(svmT_f1/10, 4))
#print(confusion_matrix(y_test, pre_ans))