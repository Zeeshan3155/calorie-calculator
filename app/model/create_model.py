import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
import joblib


def load_data():
    print("loading dataset")
    df = pd.read_csv("../../data/health_fitness_dataset.csv")

    categorical_features = ['gender', 'activity_type', 'intensity']

    # Define sample size per group (adjust as needed)
    n_samples_per_group = 1000

    # Stratified sampling across multiple categorical features
    df_sample = df.groupby(categorical_features).apply(
        lambda x: x.sample(n=min(n_samples_per_group, len(x)), random_state=42)).reset_index(drop=True)
    df_sample.drop(columns=["date", "participant_id"], inplace=True)
    X = df_sample.drop(columns=["calories_burned"])
    y = df_sample["calories_burned"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    print("loading data done")
    return X_train, y_train


def train_model():
    X_train, y_train = load_data()
    print("training model")
    categorical_features2 = ['activity_type']
    numerical_features2 = ['age', 'height_cm', 'weight_kg', 'duration_minutes']
    intensity_features2 = ['intensity']

    categorical_transformer2 = Pipeline([
        ('encoder', OneHotEncoder(sparse_output=False, drop='first', handle_unknown='ignore'))
    ])

    numerical_transformer2 = Pipeline([
        ('scaler', StandardScaler())
    ])

    intensity_transformer2 = Pipeline([
        ('encoder', OrdinalEncoder())
    ])

    preprocessor2 = ColumnTransformer([
        ('cat', categorical_transformer2, categorical_features2),
        ('num', numerical_transformer2, numerical_features2),
        ('intensity', intensity_transformer2, intensity_features2)
    ])

    rf2 = RandomForestRegressor(n_estimators=100, max_depth=20, min_samples_split=2, min_samples_leaf=1)

    pipeline_rf2 = Pipeline([
        ('preprocessor', preprocessor2),
        ('rf_model', rf2)
    ])

    pipeline_rf2.fit(X_train, y_train)
    print("model trained")

    cv_r2_scores2 = cross_val_score(pipeline_rf2, X_train, y_train, cv=5, scoring='r2')
    print("CV R2 Scores: ", cv_r2_scores2)
    print("Mean R2 Scores: ", np.mean(cv_r2_scores2))
    print("Standard Deviation R2 Scores: ", np.std(cv_r2_scores2))

    joblib.dump(pipeline_rf2, "model.pkl")
    print("model saved")


train_model()