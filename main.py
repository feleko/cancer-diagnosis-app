# Load libraries
import pandas
import matplotlib.pyplot as plt
import os
import csv


def cvs_reader(path):
    reader = csv.reader(open(path), delimiter=' ', quotechar='|')
    list_csv = list(reader)
    list_csv.pop(0)
    return list_csv


def test_libraries():
    # Python version
    import sys
    print('Python: {}'.format(sys.version))
    # scipy
    import scipy
    print('scipy: {}'.format(scipy.__version__))
    # numpy
    import numpy
    print('numpy: {}'.format(numpy.__version__))
    # matplotlib
    import matplotlib
    print('matplotlib: {}'.format(matplotlib.__version__))
    # pandas
    import pandas
    print('pandas: {}'.format(pandas.__version__))
    # scikit-learn
    import sklearn
    print('sklearn: {}'.format(sklearn.__version__))


def main():
    test_libraries()
    path = 'csv'
    for top, dnames, fnames in os.walk(path):
        for fname in fnames:
            table = cvs_reader(os.path.join(top, fname))
            if len(table) > 0:
                print(os.path.join(top, fname))
                dataset = pandas.read_csv(os.path.join(top, fname), header=0, sep=';')
                dataset = dataset.drop(['No', 'Filename', 'CircularShapeFactor', 'ElongationA', 'ElongationB',
                                        'Roundness', 'Convex Defficiency', 'Eccentricity',
                                        'Perimeter', 'MeanIntensity', 'MinIntensity', 'MaxIntensity'], axis=1)
                # shape
                print(dataset.shape)

                # head
                print(dataset.head(20))

                # descriptions
                print(dataset.describe())

                # box and whisker plots
                dataset.plot(kind='box', layout=(2, 2), sharex=False, sharey=False)
                # plt.show()
                plt.savefig('./img/box/(%s).png' % fname)
                plt.close()

                # histograms
                dataset.hist()
                # plt.show()
                plt.savefig('./img/histograms/(%s).png' % fname)
                plt.close()

                # scatter plot matrix
                pandas.scatter_matrix(dataset)
                # plt.show()
                plt.savefig('./img/scatter/(%s).png' % fname)
                plt.close()
            else:
                print("The file is empty: " + fname)


main()
