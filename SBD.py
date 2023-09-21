import os
#  - OBTAIN FEATURES

#  - READ SBD.train
with open('SBD.train', 'r') as f:
    train = f.readlines()

#  - LOOP THROUGH TRAIN AND REMOVE \n FROM EACH INDEX
for i in range(len(train)):
    train[i] = train[i].replace('\n', '')
    
#  - REPEAT FOR SBD.test
with open('SBD.test', 'r') as f:
    test = f.readlines()
    
for i in range(len(test)):
    test[i] = test[i].replace('\n', '')
    
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
features = []
for i in range(len(train)):
    temp_features = []
