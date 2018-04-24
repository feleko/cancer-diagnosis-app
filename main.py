# Load libraries
import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import os
import csv
import sys


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


def cvs_reader(path):
    reader = csv.reader(open(path), delimiter=' ', quotechar='|')
    list_csv = list(reader)
    list_csv.pop(0)
    return list_csv


def create_chart(dataset, path):
    # box and whisker plots
    dataset.plot(kind='box', layout=(2, 2), sharex=False, sharey=False)
    # plt.show()
    plt.savefig('%s/box.png' % path)
    plt.close()

    # histograms
    dataset.hist()
    # plt.show()
    plt.savefig('%s/histograms.png' % path)
    plt.close()

    # scatter plot matrix
    scatter_matrix(dataset)
    # plt.show()
    plt.savefig('%s/scatter_matrix.png' % path)
    plt.close()


def statistical_data(dataset, fout=sys.stdout):
    to_write = [('shape', dataset.shape), ('head', dataset.head(20))]

    for name in 'count min max mean median quantile'.split():
        to_write.append((name, getattr(dataset, name)()))
        to_write.append(('descriptions', dataset.describe()))
    s = '\n'.join(["%s: %s " % (str(i[0]), repr(i[1])) for i in to_write])
    # s.write(fout)
    fout.write(s)


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

                path = os.path.join("./scores/", fname)
                if not os.path.exists(path):
                    os.makedirs(path)

                    create_chart(dataset, path)

                    with open(os.path.join(path, 'info.txt'), 'w') as fout:
                        statistical_data(dataset, fout)

            else:
                print("The file is empty: " + fname)


main()
