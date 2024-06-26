# -*- coding: utf-8 -*-
"""Credit Card Fraud Detection model

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/credit-card-fraud-detection-model-ed2ef4f7-e702-4a9f-a162-dffb4ac4af6c.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240429/auto/storage/goog4_request%26X-Goog-Date%3D20240429T142027Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D70e0a77f5ad8204b2e6b5f3e11181cc15a45c180fef4a030246f73f1bbdfb9af35c0e1032ee359e6595c603f9e84ed2c6fdf8bc631e6498d45f45db547d6faf5b597bea08d8ee0a16c718f2b605fe7260b30462a05bb9458e443e63eca9ab017554ab171db860f13549df8334b1593ce4ce4209936cb195e907fbcc55598c2d6890d163c8ef1f2758dd8745e254e7a0c82b03688423bd1cfcdaa75b0f4b3199d93fbaad0c2a6e4e94521bc3a443a6d4db17f7f9e6f72793fffc16fe706d05ca7f25b8343be50becf7aca1c068a7ae2abb2e5e60b223560f958d437b81b542da77e3c3269d1437e8079aead2d30e8f3ee167c6b02570c0dff9c2c1a9e66cc31a9
"""

# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES
# TO THE CORRECT LOCATION (/kaggle/input) IN YOUR NOTEBOOK,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR
# NOTEBOOK.

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'creditcardfraud:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F310%2F23498%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240429%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240429T142027Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D50aa558f85265a9915f265cd5df5d891b1c3964ed9d0efda82e18c10fbe1d088bbab4f6e466f2c4608e8926e82565b6ff32fe90f8d98ff111ccb837c8646a0ba09645348b63f6432b6ed1893bfc5d02d5c2ca9f7408b5943c0352d63af828db01f519072bacb98ef51c56bcbf97f052467a269f3dc04d79f8064ca5c91ee23fe6532f327c2b02bd54384aa7fcaa23ffd6c9f92333dc061d3503f6319f13d25dd34bb9717374daadae30a04cdbb32c72e52b040d154f136e4fc31b46d0312551aa3767f42b83bec09a59c23e4eb5a10dfdb57b3d4b3b20ea2b9119a47367481be4909aa7b414a55a77abab49579e4a258fd23fb13a9c1d652679bb034528b77b2'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

"""## Import Needed Dependencies"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Classifier Libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, recall_score, classification_report
from xgboost import XGBClassifier, plot_importance

"""## EDA"""

df = pd.read_csv('/kaggle/input/creditcardfraud/creditcard.csv')
df.head(10)

# Getting some information about data
df.info()

# Getting some descriptive statistics about data
df.describe()

"""## Checking Missing Data"""

total = df.isnull().sum().sort_values(ascending = False)
percent = (df.isnull().sum()/df.isnull().count()*100).sort_values(ascending = False)
pd.concat([total, percent], axis=1, keys=['Total', 'Percent']).transpose()

"""## Checking Duplicates"""

duplicated_values = df[df.duplicated()]
print(duplicated_values)

df.drop_duplicates(inplace=True)

# the dupliccates are all removed

df.info()

"""## Showing Fraud Results"""

df['Class'].value_counts()

print('No Frauds', round(df['Class'].value_counts()[0]/len(df) * 100,2), '% of the dataset')
print('Frauds', round(df['Class'].value_counts()[1]/len(df) * 100,2), '% of the dataset')

sns.countplot(x='Class',data = df)
plt.title('Class Distributions \n (0: No Fraud || 1: Fraud)', fontsize=14)

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12,6))
s = sns.boxplot(ax = ax1, x="Class", y="Amount", hue="Class",data=df, palette="PRGn",showfliers=True)
s = sns.boxplot(ax = ax2, x="Class", y="Amount", hue="Class",data=df, palette="PRGn",showfliers=False)
plt.show();

tmp = df[['Amount','Class']].copy()
class_0 = tmp.loc[tmp['Class'] == 0]['Amount']
class_1 = tmp.loc[tmp['Class'] == 1]['Amount']
class_0.describe()

class_1.describe()

"""#### The real transaction have a larger mean value, larger Q1, smaller Q3 and Q4 and larger outliers; fraudulent transactions have a smaller Q1 and mean, larger Q4 and smaller outliers."""

dataplot = sns.heatmap(df.corr(), cmap="Blues")
plt.show()

"""### Model Training"""

x = df.drop('Class', axis='columns')
y = df['Class']

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)

"""#### Logistic Regression"""

lr_model = LogisticRegression()
lr_model.fit(x_train, y_train)

y_predicted = lr_model.predict(x_test)
print(classification_report(y_test, y_predicted))

confusion = confusion_matrix(y_test, y_predicted)
confusion

sns.heatmap(confusion, annot=True, linecolor='white', linewidths=1)

"""### XGBoost Classifier"""

xgb = XGBClassifier()
xgb.fit(x_train,y_train)

y_pred = xgb.predict(x_test)
print(classification_report(y_test, y_pred))

confusion_m = confusion_matrix(y_test, y_pred)
confusion_m

sns.heatmap(confusion_m, annot=True, linecolor='white', linewidths=1)

plot_importance(xgb)
plt.show()