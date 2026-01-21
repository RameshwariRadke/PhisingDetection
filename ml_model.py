#import libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold
from imblearn.over_sampling import SMOTE

#read csv files and create dataframe
phish=pd.read_csv("data/structured_data_phishing.csv")
legit=pd.read_csv("data/structured_data_legitimate.csv")


#combine legitimate and phishing dataframe
final_df=pd.concat([phish,legit],axis=0)

#shuffle
final_df=final_df.sample(frac=1)
print(final_df.shape)

#remove urls,duplicates & then we create X and Y for the models,Supervised learning
final_df=final_df.drop(columns="URL",axis=1)
final_df=final_df.drop_duplicates()

print(final_df.shape)

X=final_df.drop(columns="label",axis=1)
Y=final_df["label"]

FEATURE_COLUMNS = X.columns.tolist()


print(X.shape)
print(Y.shape)
print(final_df["label"].value_counts())


#create an ML model using sklearn
svc_model=svm.LinearSVC(class_weight="balanced")

#RandomForest
rf_model=RandomForestClassifier(n_estimators=60,class_weight="balanced")

#DecisionTree
dt_model=DecisionTreeClassifier(class_weight="balanced")

#AdaBoost
ab_model=AdaBoostClassifier()

#GaussianNB
nb_model=GaussianNB()


def calculate_measures(tn,fp,fn,tp):
    model_accuracy=(tp+tn)/(tp+fn+fp+tn)
    model_precision=tp/(tp+fp) if(tp+fp)!= 0  else 0
    model_recall=tp/(tp+fn) if(tp+fn)!= 0  else 0

    return model_accuracy,model_precision,model_recall

#Initialize the SMOTE
smote=SMOTE(random_state=42)


#K- fold cross validation for K=5
k=5
stf=StratifiedKFold(n_splits=k,shuffle=True,random_state=42)

rf_accuracy_list,rf_precision_list,rf_recall_list=[],[],[]
dt_accuracy_list,dt_precision_list,dt_recall_list=[],[],[]
svc_accuracy_list,svc_precision_list,svc_recall_list=[],[],[]
ab_accuracy_list,ab_precision_list,ab_recall_list=[],[],[]
nb_accuracy_list,nb_precision_list,nb_recall_list=[],[],[]

for train_idx,test_idx in stf.split(X,Y):
    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = Y.iloc[train_idx]
    y_test = Y.iloc[test_idx]

    ## Apply SMOTE
    X_train_res,y_train_res=smote.fit_resample(X_train,y_train)

    ## RandomForestClassifier
    rf_model.fit(X_train_res,y_train_res)
    rf_pred=rf_model.predict(X_test)
    tn,fp,fn,tp=confusion_matrix(y_true=y_test,y_pred=rf_pred).ravel()
    accuracy_rf,precision_rf,recall_rf=calculate_measures(tn,fp,fn,tp)
    rf_accuracy_list.append(accuracy_rf)
    rf_recall_list.append(recall_rf)
    rf_precision_list.append(precision_rf)

    ## SVC
    svc_model.fit(X_train_res,y_train_res)
    svc_pred=svc_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=svc_pred).ravel()
    svc_accuracy, svc_precision, svc_recall = calculate_measures(tn, fp, fn, tp)
    svc_accuracy_list.append(svc_accuracy)
    svc_precision_list.append(svc_precision)
    svc_recall_list.append(svc_recall)

    ## DecisionTreeClassifier
    dt_model.fit(X_train_res,y_train_res)
    dt_pred = dt_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=dt_pred).ravel()
    dt_accuracy, dt_precision, dt_recall = calculate_measures(tn, fp, fn, tp)
    dt_accuracy_list.append(dt_accuracy)
    dt_precision_list.append(dt_precision)
    dt_recall_list.append(dt_recall)

    ## GaussianNB
    nb_model.fit(X_train_res,y_train_res)
    nb_pred = nb_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=nb_pred).ravel()
    nb_accuracy, nb_precision, nb_recall = calculate_measures(tn, fp, fn, tp)
    nb_accuracy_list.append(nb_accuracy)
    nb_precision_list.append(nb_precision)
    nb_recall_list.append(nb_recall)

    ## AdaBoost
    ab_model.fit(X_train_res,y_train_res)
    ab_pred = ab_model.predict(X_test)
    tn, fp, fn, tp = confusion_matrix(y_true=y_test, y_pred=ab_pred).ravel()
    ab_accuracy, ab_precision, ab_recall = calculate_measures(tn, fp, fn, tp)
    ab_accuracy_list.append(ab_accuracy)
    ab_precision_list.append(ab_precision)
    ab_recall_list.append(ab_recall)



#RandomForest
rf_accuracy=sum(rf_accuracy_list)/len(rf_accuracy_list)
rf_precision=sum(rf_precision_list)/len(rf_precision_list)
rf_recall=sum(rf_recall_list)/len(rf_recall_list)

print("RF accuracy:",rf_accuracy)
print("RF precision:",rf_precision)
print("RF recall:",rf_recall)

#DecisionTree
dt_accuracy=sum(dt_accuracy_list)/len(dt_accuracy_list)
dt_precision=sum(dt_precision_list)/len(dt_precision_list)
dt_recall=sum(dt_recall_list)/len(dt_recall_list)

print("DT accuracy:",dt_accuracy)
print("DT precision:",dt_precision)
print("DT recall:",dt_recall)

#SVC
svc_accuracy=sum(svc_accuracy_list)/len(svc_accuracy_list)
svc_precision=sum (svc_precision_list)/len(svc_precision_list)
svc_recall=sum(svc_recall_list)/len(svc_recall_list)

print("SVC accuracy:",svc_accuracy)
print("SVC precision:",svc_precision)
print("SVC recall:",svc_recall)


#GaussianNB
nb_accuracy=sum(nb_accuracy_list)/len(nb_accuracy_list)
nb_precision=sum (nb_precision_list)/len(nb_precision_list)
nb_recall=sum (nb_recall_list)/len(nb_recall_list)
print("NB accuracy:",nb_accuracy)
print("NB precision:",nb_precision)
print("NB recall:",nb_recall)


#AdaBoost
ab_accuracy=sum(ab_accuracy_list)/len(ab_accuracy_list)
ab_precision=sum (ab_precision_list)/len(ab_precision_list)
ab_recall=sum (ab_recall_list)/len(ab_recall_list)
print("AB accuracy:",ab_accuracy)
print("AB precision:",ab_precision)
print("AB recall:",ab_recall)


data={"accuracy":[nb_accuracy,rf_accuracy,dt_accuracy,svc_accuracy,ab_accuracy],
      "precision":[nb_precision,rf_precision,dt_precision,svc_precision,ab_precision],
      "recall":[nb_recall,rf_recall,dt_recall,svc_recall,ab_recall]}

index=["NB","RF","DT","SVC","AB"]

visual_df=pd.DataFrame(data,index=index)

##Visualize the data
# f=visual_df.plot.bar(rot=0)
# plt.show()
X_resampled, Y_resampled = smote.fit_resample(X, Y)
final_model = AdaBoostClassifier()
final_model.fit(X_resampled, Y_resampled)

import pickle

with open("models/adaboost_model.pkl", "wb") as f:
    pickle.dump(final_model, f)

