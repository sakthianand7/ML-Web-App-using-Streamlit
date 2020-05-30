import streamlit as slt
from sklearn.svm import SVC,SVR
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import plot_confusion_matrix, plot_roc_curve, plot_precision_recall_curve
from sklearn.metrics import precision_score, recall_score,mean_squared_error
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

def main():
	slt.title('Visualize Classification and Regression ')
	slt.subheader('Classifiers - Naive Bayes , Kernel SVM , Support Vector Machine')
	slt.subheader('Regression - Linear Regression , Polynomial Regression , Random Forest')

	slt.sidebar.title("SELECT YOUR ALGORITHM")
	select=slt.sidebar.selectbox("Try Classification or Regression",("Classification", "Regression"))
	if select=='Classification':
		@slt.cache(persist=True)
		def fetch_data():
			data=pd.read_csv('Social_Network_Ads.csv')
			x=data.iloc[:,[2,3]].values
			y=data.iloc[:,-1].values

			return x,y

		@slt.cache(persist=True)
		def split_data(x,y):
			x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
			sc=StandardScaler()
			x_train=sc.fit_transform(x_train)
			x_test=sc.transform(x_test)
			return x_train,x_test,y_train,y_test

		def plot_values(listofmetrics):
			if 'Confusion Matrix' in listofmetrics:
				slt.subheader('Confusion Matrix')
				plot_confusion_matrix(model,x_test,y_test,display_labels=class_names,cmap='viridis',)
				slt.pyplot()

			if 'ROC Curve' in listofmetrics:
				slt.subheader("ROC Curve")
				plot_roc_curve(model, x_test, y_test)
				slt.pyplot()
	        

		x,y=fetch_data()
		class_names=['notpurchased','purchased']

		x_train,x_test,y_train,y_test=split_data(x,y)

		classifier = slt.sidebar.selectbox("Classifier", ("Kernel SVM","Naive Bayes","Support Vector Machine"))
		if classifier == 'Support Vector Machine':
			slt.sidebar.subheader("Model Hyperparameters")
			metrics = slt.sidebar.multiselect("What metrics to plot?", ('Confusion Matrix','ROC Curve'))

			if slt.sidebar.button("Classify", key='classify'):
				slt.subheader("Support Vector Machine  Results")
				model = SVC(kernel='linear', random_state=0)
				model.fit(x_train, y_train)
				accuracy = model.score(x_test, y_test)
				y_pred = model.predict(x_test)
				slt.write("Accuracy: ", accuracy.round(2))
				slt.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
				plot_values(metrics)
				
		if classifier == 'Kernel SVM':
			slt.sidebar.subheader("Model Hyperparameters")
			metrics = slt.sidebar.multiselect("What metrics to plot?", ('Confusion Matrix','ROC Curve'))
			kernel = slt.sidebar.radio("Kernel", ("rbf", "linear"), key='kernel')

			if slt.sidebar.button("Classify", key='classify'):
				slt.subheader("Kernel SVM Results")
				model = SVC(kernel=kernel, random_state=0)
				model.fit(x_train, y_train)
				accuracy = model.score(x_test, y_test)
				y_pred = model.predict(x_test)
				slt.write("Accuracy: ", accuracy.round(2))
				slt.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
				plot_values(metrics)
		if classifier == 'Naive Bayes':
			slt.sidebar.subheader("Model Hyperparameters")
			metrics = slt.sidebar.multiselect("What metrics to plot?", ('Confusion Matrix','ROC Curve'))
			if slt.sidebar.button("Classify", key='classify'):
				slt.subheader("Naive Bayes Results")
				model = GaussianNB()
				model.fit(x_train, y_train)
				accuracy = model.score(x_test, y_test)
				y_pred = model.predict(x_test)
				slt.write("Accuracy: ", accuracy.round(2))
				slt.write("Precision: ", precision_score(y_test, y_pred, labels=class_names).round(2))
				plot_values(metrics)

		if slt.sidebar.checkbox("Show Dataset", False):
			slt.subheader("Classification Dataset ")
			slt.write("Customer Purchase Staus based on Social Media Ads")
			d=pd.read_csv('Social_Network_Ads.csv')
			slt.write(d)
	else:
		@slt.cache(persist=True)
		def fetch_data():
			data=pd.read_csv('salary_data.csv')
			x=data.iloc[:,:-1].values
			y=data.iloc[:,-1].values

			return x,y

		@slt.cache(persist=True)
		def split_data(x,y):
			x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
			return x_train,x_test,y_train,y_test

		def plot_values(listofmetrics):
			if 'Graph - Train Predictions' in listofmetrics:
				slt.subheader('Graph - Train Predictions')
				plt.scatter(x_train,y_train,color='red')
				plt.plot(x_train,y_train_pred,color='blue')
				plt.title('Experience Vs Salary')
				plt.xlabel('Experience')
				plt.ylabel('Salary')
				slt.pyplot()
			if 'Graph - Test Predictions' in listofmetrics:
				slt.subheader('Graph - Test Predictions')
				plt.scatter(x_test,y_test,color='red')
				plt.plot(x_test,y_pred,color='blue')
				plt.title('Experience Vs Salary')
				plt.xlabel('Experience')
				plt.ylabel('Salary')
				slt.pyplot()

		x,y=fetch_data()
		x_train,x_test,y_train,y_test=split_data(x,y)
		regressor = slt.sidebar.selectbox("Regressor", ("Simple Linear Regression","Polynomial Regression","Random Forest Regression"))
		if regressor == 'Simple Linear Regression':
			slt.sidebar.subheader("Model Hyperparameters")
			metrics = slt.sidebar.multiselect("What metrics to plot?", ('Graph - Train Predictions','Graph - Test Predictions'))

			if slt.sidebar.button("Predict", key='predict'):
				slt.subheader("Simple Linear Regression  Results")
				model=LinearRegression()
				model.fit(x_train, y_train)
				accuracy = model.score(x_test, y_test)
				y_train_pred=model.predict(x_train)
				y_pred = model.predict(x_test)
				slt.write("Accuracy: ", accuracy.round(2))
				plot_values(metrics)

		if regressor == 'Polynomial Regression':
			slt.sidebar.subheader("Model Hyperparameters")
			metrics = slt.sidebar.multiselect("What metrics to plot?", ('Graph - Predictions',))
			if slt.sidebar.button("Predict", key='predict'):
				slt.subheader("Polynomial Regression Results")
				poly_reg = PolynomialFeatures(degree = 4)
				x_poly = poly_reg.fit_transform(x)
				poly_reg.fit(x_poly, y)
				model = LinearRegression()
				model.fit(x_poly, y)
				accuracy = model.score(poly_reg.fit_transform(x), y)
				slt.write("Accuracy: ", accuracy.round(2))
				plt.scatter(x,y,color='red')
				plt.plot(x,model.predict(poly_reg.fit_transform(x)))
				plt.title('Experience Vs Salary')
				plt.xlabel('Experience')
				plt.ylabel('Salary')
				slt.pyplot()
				
		if regressor == 'Random Forest Regression':
			slt.sidebar.subheader("Model Hyperparameters")
			metrics = slt.sidebar.multiselect("What metrics to plot?", ('Graph - Predictions',))
			if slt.sidebar.button("Predict", key='predict'):
				slt.subheader("Random Forest Regression Results")
				model = RandomForestRegressor(n_estimators = 10, random_state = 0)
				model.fit(x_train,y_train)
				accuracy = model.score(x_test, y_test)
				slt.write("Accuracy: ", accuracy.round(2))
				X_grid = np.arange(min(x_train), max(x_train), 0.01)
				X_grid = X_grid.reshape((len(X_grid), 1))
				plt.scatter(x_train, y_train, color = 'red')
				plt.plot(X_grid, model.predict(X_grid), color = 'blue')
				plt.title('Experience Vs Salary')
				plt.xlabel('Experience')
				plt.ylabel('Salary')
				slt.pyplot()

		if slt.sidebar.checkbox("Show Dataset", False):
			slt.subheader("Regression Dataset ")
			slt.write("Experience vs Salary Dataset")
			d=pd.read_csv('salary_data.csv')
			slt.write(d)

	        



if __name__ == '__main__':
    main()