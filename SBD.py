import os
import re
import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

char_num = 1
char_num_map = {}

def read_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [re.sub(r'^\d+\s', '', line).replace('TOK', '').strip() for line in lines]

def convert_to_ml_format(token):
    global char_num
    global char_num_map
    for i in range(len(token)):
        if token[i] not in char_num_map:
            char_num_map[token[i]] = char_num
            char_num += 1
        token[i] = char_num_map[token[i]]
    return int(''.join(map(str, token))) if token else 0

def extract_features(dataset):
    features = []
    for i, token in enumerate(dataset):
        if '. ' not in token:
            continue
        L, label = token.split('. ')
        EOS = 1 if label.strip() == 'EOS' else 0
        R = dataset[i + 1] if i + 1 < len(dataset) else ''
        L_len = len(L)
        if L_len > 0:
            L_cap = int(L.strip()[0].isupper())
        R_cap = int(R.strip()[0].isupper()) if R else 0
        L_period = L.count('.')
        R_period = R.count('.')
        R_space = int(R.startswith(' '))
        L = convert_to_ml_format(list(L))
        R = convert_to_ml_format(list(R))
        features.append([L, R, L_len, L_cap, R_cap, L_period, R_period, R_space, EOS])
    return features

def train_and_evaluate(train_features, test_features):
    clf = DecisionTreeClassifier()
    X_train = [f[:-1] for f in train_features]
    y_train = [f[-1] for f in train_features]
    clf.fit(X_train, y_train)
    X_test = [f[:-1] for f in test_features]
    y_test = [f[-1] for f in test_features]
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    print(f'Accuracy: {accuracy}')

if __name__ == "__main__":
    train = read_file('SBD.train')
    test = read_file('SBD.test')
    train_features = extract_features(train)
    test_features = extract_features(test)
    train_and_evaluate(train_features, test_features)
