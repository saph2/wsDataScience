import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

header="../data/"

def create_matrix(classifier,X,realY,predY,numberOfClasses):

    def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
        print("Ploting the confusion matrix...\n")
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks=np.arange(numberOfClasses)
        plt.xticks(tick_marks)
        plt.yticks(tick_marks)
        plt.tight_layout()
        plt.xlabel('Predicted label')
        plt.ylabel('True label')


    # Compute confusion matrix
    cm = confusion_matrix(realY, predY)
    np.set_printoptions(precision=2)
    print('Confusion matrix, without normalization\n')
    print(cm)
    plt.figure()
    plot_confusion_matrix(cm)

    plt.savefig(header+"Results/Classifier/confusion_matrix_{0}".format(classifier))

    # Normalize the confusion matrix by row (i.e by the number of samples in each class)
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print('Normalized confusion matrix')
    print(cm_normalized)
    plt.figure()
    plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')

    plt.savefig(header+"Results/Classifier/confusion_matrix_norm_{0}".format(classifier))

   # plt.show()