from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS
from sklearn.manifold import TSNE
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def classification(X, y, kernel, norm_flag, train_size, feature_names, classifier, selection_method='None', K='5'):

    test_size = 1-train_size
    # Train-Test Split:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, train_size=train_size, shuffle=True,
                                                        random_state=5)
    if classifier == "SVM":
        clf = svm.SVC(kernel=kernel)
    elif classifier == "KNN":
        clf = KNeighborsClassifier(n_neighbors=K)

    if norm_flag:
        # fit scaler on training data
        norm = MinMaxScaler().fit(X_train)
        # transform training data
        X_train = norm.transform(X_train)
        # transform testing dataabs
        X_test = norm.transform(X_test)

    if selection_method == "RFE":
        ## Recursive Feature Elimination
        max_accur = 0
        selected_features = []
        N_features = len(feature_names)
        for i in range(0, N_features):
            rfe = RFE(clf, n_features_to_select=i + 1)
            rfe_fit = rfe.fit(X_train, y_train)

            y_pred = rfe.predict(X_test)
            accuracy = metrics.accuracy_score(y_test, y_pred)
            print("Number of features: ", i + 1)
            print("current accuracy: ", accuracy)
            feature_idx_temp = pd.Series(data=rfe_fit.ranking_, index=feature_names)
            selected_features_temp = feature_idx_temp[feature_idx_temp == 1].index
            print("temp Selected features are: ", selected_features_temp.values)

            if accuracy > max_accur:
                max_accur = accuracy
                feature_idx = pd.Series(data=rfe_fit.ranking_, index=feature_names)
                selected_features = feature_idx[feature_idx == 1].index

        print("Selected features are: ", selected_features.values)
        print("Final Accuracy: ", max_accur)

    elif selection_method == "EFS":
        # Exhaustive Feature Selection
        efs1 = EFS(clf, min_features=20, max_features=X.shape[1] - 5, scoring='accuracy', print_progress=True)
        efs1 = efs1.fit(X_train, y_train)

        print('Best accuracy score: %.2f' % efs1.best_score_)
        print('Best subset (indices):', efs1.best_idx_)
        print('Best subset (corresponding names):', efs1.best_feature_names_)

    elif selection_method == 'None':
        # Train the model:
        clf.fit(X_train, y_train)
        # Predict the response for test dataset:
        y_pred = clf.predict(X_test)
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print("accuracy: ", accuracy)
        return accuracy


def our_tsne(X, experiment, exp_type, participantID, labels, norm_flag):

    if norm_flag:
        # fit scaler on training data
        norm = MinMaxScaler().fit(X)
        # transform training data
        X = norm.transform(X)

    tsne = TSNE(n_components=2, random_state=5)
    tsne_results = tsne.fit_transform(X)
    x = tsne_results[:, 0]
    y = tsne_results[:, 1]

    df_subset = pd.DataFrame()
    df_subset['tsne-2d-one'] = x
    df_subset['tsne-2d-two'] = y
    df_subset['experiment'] = experiment
    df_subset['labels'] = labels

    plt.figure(figsize=(16, 10))
    ax = sns.scatterplot(
        x="tsne-2d-one", y="tsne-2d-two",
        hue='experiment',
        style='labels',
        palette=sns.color_palette("hls", 10),
        data=df_subset,
        s=200,
        legend="full",
        alpha=1
    )
    plt.legend(fontsize=20)
    plt.show()

