import os
import re
#  - OBTAIN FEATURES

#  - READ SBD.train
with open('SBD.train', 'r') as f:
    train = f.readlines()

#  - LOOP THROUGH TRAIN AND REMOVE \n FROM EACH INDEX
for i in range(len(train)):
    # remove the number and space at the beginning of the line
    train[i] = re.sub(r'^\d+\s', '', train[i])
    # remove the 'TOK' at the end of the line
    train[i] = train[i].replace('TOK', '').replace('\n', '')
    
#  - REPEAT FOR SBD.test
with open('SBD.test', 'r') as f:
    test = f.readlines()
    
for i in range(len(test)):
    # remove the number and space at the beginning of the line
    test[i] = re.sub(r'^\d+\s', '', test[i])
    # remove the 'TOK' at the end of the line
    test[i] = test[i].replace('TOK', '').replace('\n', '')
    
    
#  - FEATURE EXTRACTION

# WE WILL BE USING THE FOLLOWING FEATURES
#  - Word to the left of "." (L)
#  - Word to the right of "." (R)
#  - Length of L < 3  
#  - Is L capitalized?
#  - Is R capitalized?
#  - count(period, R)  
#  - count(period, L)
#  - count(R, is lower case)
def extract_features(dataset, features):
    for i in range(len(dataset)):
        # for each token in dataset we check for a period. If there is one we extract the features
        if '.' in dataset[i]:
            # split the token at the period
            token = dataset[i].split('.')
            # if the token is not empty
            if token[0] != '':
                # extract EOS or NEOS label from token[1]
                if token[1].strip() == 'EOS':
                    EOS = 1
                else:
                    EOS = 0
                # extract the features
                L = token[0]
                if i+1 < len(dataset):
                    R = dataset[i+1]
                else:
                    R = ''
                L_len = len(L)
                # trim whitespace when checking for capitalization
                L_cap = L.strip()[0].isupper()
                R_cap = R.strip()[0].isupper()
                L_period = L.count('.')
                R_period = R.count('.')
                # check if R starts with a space
                R_space = 0
                if R[0] == ' ':
                    R_space = 1
                # append the features to the features list
                features.append([L, R, L_len, L_cap, R_cap, L_period, R_period, R_space, EOS])
    return features
train_features = extract_features(train, [])
test_features = extract_features(test, [])