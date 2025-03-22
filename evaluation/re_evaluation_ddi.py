#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from utils.util import *
from sklearn.metrics import f1_score, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import itertools


# ##
def plot_confusion_matrix_jama(confusion_mat, classes, normalize=False, title='',
                               save_dir='results_plot_confusion_matrix', save_name='confusion_matrix',
                               confusion_matap=plt.cm.get_cmap('Blues'), colorbar=True,
                               fontsize=14):  # plt.cm.Blues   plt.cm.get_cmap('RdYlBu')
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    ### usage1
    mat=excel2numpy('a.xlsx')
    y_test=mat[:,0]
    y_pred=mat[:,1]
    confusion_mat = confusion_matrix(y_test, y_pred)
    class_names=[0,1,2,3,4,5,6,7,8,9]
    plot_confusion_matrix(confusion_mat, classes=class_names, normalize=True)
    """

    fig = plt.figure()
    if normalize:
        confusion_mat = confusion_mat

    plt.imshow(confusion_mat, interpolation='nearest', cmap=confusion_matap)
    if len(title) > 0:
        plt.title(title, fontsize=fontsize + 4)
    if colorbar:
        cbar = plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45, fontsize=fontsize + 4)
    plt.yticks(tick_marks, classes, fontsize=fontsize + 4)

    fmt = '.3f' if normalize else 'd'
    thresh = confusion_mat.max() / 2.
    for i, j in itertools.product(range(confusion_mat.shape[0]), range(confusion_mat.shape[1])):
        plt.text(j, i, "%d" % (confusion_mat[i, j]), horizontalalignment="center",
                 color="white" if confusion_mat[i, j] > thresh else "black", fontsize=fontsize - 1)
    plt.ylabel('True label', fontsize=fontsize + 4)
    plt.xlabel('Predicted label', fontsize=fontsize + 4)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    plt.tight_layout()
    fig.set_size_inches(10.2, 8.5)
    # plt.savefig(os.path.join(save_dir,save_name+'.eps'))
    # plt.savefig(os.path.join(save_dir, save_name + '.png'), dpi=200)
    # plt.savefig(r'D:\ProgramData\PycharmProject\DDBioRE\results\cm.png')
    plt.show()
    # plt.savefig(os.path.join(save_dir,save_name+'.jpg'), dpi=200)
    # plt.savefig(os.path.join(save_dir,save_name+'.pdf'))
    plt.close()
    print("Plot confusion matrix finished")


# ##
def load_label_and_result_compute_f1_score(src_file, result_file):
    # ##
    label_list = []
    json_data = load_json_data_base(src_file)
    for obj in json_data:
        option_src = ddi_relation_convert_to_option(obj['relation'])
        label = ddi_option_convert_to_id(option_src)
        label_list.append(label)
    # ##
    result_label_list = []
    result_json_data = load_json_data_base(result_file)
    for obj in result_json_data:
        option = obj['result'].replace('\"', '')
        print(obj['sentence'])
        result_label = ddi_option_convert_to_id(option)
        result_label_list.append(result_label)

    # ##
    f1_score_macro = f1_score(label_list, result_label_list, average='macro')
    f1_score_micro = f1_score(label_list, result_label_list, average='micro')
    f1_score_weighted = f1_score(label_list, result_label_list, average='weighted')
    # ##
    print("\033[91mMacro F1 Score is {}!\033[0m".format(f1_score_macro))
    print("\033[92mMicro F1 Score is {}!\033[0m".format(f1_score_micro))
    print("\033[93mWeighted F1 Score is {}!\033[0m".format(f1_score_weighted))

    # ##
    labels_name = ['mechanism', 'effect', 'advise', 'int', 'false']
    cm = confusion_matrix(label_list, result_label_list)
    plot_confusion_matrix_jama(cm, classes=labels_name, title='Confusion Matrix DDI', save_dir=r'results')


if __name__ == '__main__':
    # ##
    src_file = r'../data/DDICorpus/test.json'

    result_file = r'../data/DDICorpus/test_baseline.json'

    load_label_and_result_compute_f1_score(src_file, result_file)
