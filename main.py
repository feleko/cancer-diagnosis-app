# Load libraries
import pandas

import matplotlib.pyplot as plt
import os
import csv
import sys
import argparse


def print_libraries_version():
    import sys
    print('Python: {}'.format(sys.version))

    import scipy
    print('scipy: {}'.format(scipy.__version__))

    import numpy
    print('numpy: {}'.format(numpy.__version__))

    import matplotlib
    print('matplotlib: {}'.format(matplotlib.__version__))

    import pandas
    print('pandas: {}'.format(pandas.__version__))

    import sklearn
    print('sklearn: {}'.format(sklearn.__version__))


def csv_reader(path):
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
    pandas.scatter_matrix(dataset)
    # plt.show()
    plt.savefig('%s/scatter_matrix.png' % path)
    plt.close()

    # scatter
    dataset.plot.scatter(x='Centroid1', y='Centroid2', c='Area', s=50)
    plt.savefig('%s/scatter.png' % path)
    plt.close()


def statistical_data(dataset, fout=sys.stdout):
    to_write = [('shape', dataset.shape), ('head', dataset.head(20))]

    for name in 'count min max mean median quantile'.split():
        to_write.append((name, getattr(dataset, name)()))
        to_write.append(('descriptions', dataset.describe()))
    s = '\n'.join(["%s: %s " % (str(i[0]), repr(i[1])) for i in to_write])
    fout.write(s)


def check_directory_existence(directory):
    if os.path.exists(directory):
        print("`%s` directory exists" % directory)
        return True
    else:
        print("`%s` directory not found" % directory)
        return False


def run_analysis(path):
    for top, dnames, fnames in os.walk(path):
        for fname in fnames:
            table = csv_reader(os.path.join(top, fname))
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


def read_arguments():
    parser = argparse.ArgumentParser(description="Analysis of cancerous cells")
    parser.add_argument('csv_path', default='./csv', help='Path to the directory with *.csv files', nargs='?')
    parser.add_argument('scores_path', default='./scores', help='Path to scores directory', nargs='?')
    args = parser.parse_args()
    return args


def main():
    print_libraries_version()
    args = read_arguments()

    print "Environment: \n * CSV directory path: %s\n * Scores directory path: %s\n" \
          % (args.csv_path, args.scores_path)

    if check_directory_existence(args.csv_path):
        if not check_directory_existence(args.scores_path):
            os.makedirs(args.scores_path)
        run_analysis(args.csv_path)


main()

