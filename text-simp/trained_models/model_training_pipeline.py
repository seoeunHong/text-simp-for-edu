from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error,mean_squared_log_error, explained_variance_score
from sklearn.preprocessing import StandardScaler
from pysr import PySRRegressor
import pickle
import spacy
import numpy as np

from linguistic_features.web_scraping import run_initial_web_scraping
from linguistic_features import data_pre_processing
import evaluation_functions

def split_train_test_by_category(df, category_name, nlp):
    # This function prepares the data for training by collecting all the features and Lexile scores for each sample. Splits the data into 80% for training and 20% for testing.

    # df = df.sample(n=500, random_state=42)
    mask = np.random.rand(len(df)) < 0.8
    train_df = df[mask]
    test_df = df[~mask]

    if category_name == 'Lexile':
        print('Lexile')
        function = evaluation_functions.all_linguistic_features
    elif category_name == 'lexical':
        print('lexical')
        function = evaluation_functions.lexical_linguistic_features
    elif category_name == 'syntax':
        print('syntax')
        function = evaluation_functions.syntax_linguistic_features
    else:
        print('decodability')
        function = evaluation_functions.decodability_linguistic_features

    X_train = []
    X_test = []
    Y_train = []
    Y_test = []
    for index, row in train_df.iterrows():
        print("working on text number: ", index)
        y = row['Lexile']
        text = row['Content']
        x = []
        text_score_dict = function(text, nlp)
        for key, value in text_score_dict.items():
            x.append(value)
        X_train.append(x)
        Y_train.append(y)
    for index, row in test_df.iterrows():
        print("working on text number: ", index)
        y = row['Lexile']
        text = row['Content']
        x = []
        text_score_dict = function(text, nlp)
        for key, value in text_score_dict.items():
            x.append(value)
        X_test.append(x)
        Y_test.append(y)
    return X_train, Y_train, X_test, Y_test

def linear_regrassion(train_X, train_Y, test_X,test_Y,category_name,model_save_path):
    # This function trains a linear regression model and prints the MSE, MSLE, EVS and correlation of the model. It also saves the model to a file

    model = LinearRegression()
    model.fit(train_X, train_Y)
    y_pred = model.predict(test_X)
    print("y_pred", y_pred)
    print("test_Y", test_Y)
    mse = mean_squared_error(test_Y, y_pred)
    print("MSE of",category_name, "is: ", mse)
    msle = mean_squared_log_error(test_Y, y_pred)
    print("MSLE of",category_name, "is: ", msle)
    evs = explained_variance_score(test_Y, y_pred)
    print("EVS of",category_name, "is: ", evs)
    print("corrolation of",category_name, "is: ", np.corrcoef(test_Y, y_pred))
    with open(model_save_path, 'wb') as model_file:
        pickle.dump(model, model_file)
    return model

def run_regression(category):
    # This function trains linear regression model on the lexile dataset
    nlp = spacy.load("en_core_web_sm")
    dataset_path = 'datasets/lexile_dataset.xlsx'
    df = data_pre_processing.read_xlsx_to_df(dataset_path)
    X_train, Y_train, X_test, Y_test = split_train_test_by_category(df, category, nlp)
    print("X_train:", X_train)
    print("Y_train:", Y_train)
    print("X_train[0]:" ,X_train[0])
    linear_regrassion(X_train, Y_train, X_test, Y_test, category, f'trained_models/final_{category}')



def normalized_linear_regrassion(train_X, train_Y, test_X,test_Y,category_name,model_save_path):
    # This function trains a normalized linear regression model and prints the MSE, MSLE, EVS and correlation of the model. It also saves the model to a file

    scaler = StandardScaler()
    train_X_scaled = scaler.fit_transform(train_X)
    test_X_scaled = scaler.transform(test_X)

    model = LinearRegression()
    model.fit(train_X_scaled, train_Y)
    y_pred = model.predict(test_X_scaled)
    print("y_pred", y_pred)
    print("test_Y", test_Y)
    mse = mean_squared_error(test_Y, y_pred)
    print("MSE of",category_name, "is: ", mse)
    msle = mean_squared_log_error(test_Y, y_pred)
    print("MSLE of",category_name, "is: ", msle)
    evs = explained_variance_score(test_Y, y_pred)
    print("EVS of",category_name, "is: ", evs)
    print("corrolation of",category_name, "is: ", np.corrcoef(test_Y, y_pred))
    with open(model_save_path, 'wb') as model_file:
        pickle.dump(model, model_file)
    return model

def sparse_linear_regrassion(train_X, train_Y, test_X,test_Y,category_name,model_save_path):
    # This function trains a sparse linear regression model and prints the MSE, MSLE, EVS and correlation of the model. It also saves the model to a file

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(train_X)
    X_test_scaled = scaler.transform(test_X)
    alpha = 0.5  # Adjust the alpha value as needed
    lasso_model = Lasso(alpha=alpha)
    lasso_model.fit(X_train_scaled, train_Y)
    y_pred = lasso_model.predict(X_test_scaled)
    mse = mean_squared_error(test_Y, y_pred)
    print("MSE of", category_name, "is: ", mse)
    msle = mean_squared_log_error(test_Y, y_pred)
    print("MSLE of", category_name, "is: ", msle)
    evs = explained_variance_score(test_Y, y_pred)
    print("EVS of", category_name, "is: ", evs)
    print("corrolation of", category_name, "is: ", np.corrcoef(test_Y, y_pred))
    with open(model_save_path, 'wb') as model_file:
        pickle.dump(lasso_model, model_file)


def pysrtrain_X(train_X,train_Y, test_X,test_Y,category_name):
    # This function trains a symbolic regression model and prints the MSE, MSLE, EVS and correlation of the model. It also saves the model to a file
    model = PySRRegressor(
        niterations=20,  # < Increase me for better results
        binary_operators=["+", "*"],
        unary_operators=[
            "exp",
            "inv(x) = 1/x",
        ],
        extra_sympy_mappings={"inv": lambda x: 1 / x},
        # The loss function is very sensitive! change carefully
        # loss="loss(prediction, target) = (prediction - target) ^ 2 + 1 - abs(prediction - 4.1)"
        loss="loss(prediction, target) = (prediction - target)^2",
    )
    model.fit(train_X, train_Y)
    y_pred = model.predict(test_X)
    print("y_pred", y_pred)
    print("test_Y", test_Y)
    mse = mean_squared_error(test_Y, y_pred)
    print("MSE of",category_name, "is: ", mse)
    msle = mean_squared_log_error(test_Y, y_pred)
    print("MSLE of",category_name, "is: ", msle)
    evs = explained_variance_score(test_Y, y_pred)
    print("EVS of",category_name, "is: ", evs)
    print("corrolation of",category_name, "is: ", np.corrcoef(test_Y, y_pred))
    return model

def model_training_pipeline():
    # Initialize Base Datasets
    run_initial_web_scraping()
    run_regression('Lexile')
    run_regression('lexical')
    run_regression('syntax')
    run_regression('decodability')

if __name__ == '__main__':
    model_training_pipeline()