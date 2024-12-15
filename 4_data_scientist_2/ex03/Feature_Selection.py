import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor

def calculate_vif_1(data):
    vif_data = pd.DataFrame()
    vif_data["feature"] = data.columns
    vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
    vif_data["Tolerance"] = 1 / vif_data["VIF"]
    return vif_data

def calculate_vif_2(data):
    vif_data = pd.DataFrame()
    vif_data["feature"] = data.columns
    vif_data["VIF"] = [variance_inflation_factor(data.values, i) for i in range(data.shape[1])]
    vif_data["Tolerance"] = 1 / vif_data["VIF"]
    total_tolerance = vif_data["Tolerance"].sum()
    vif_data["Tolerance"] = (vif_data["Tolerance"] * 100) / total_tolerance
    return vif_data

def remove_high_tolerance_features(data, vif_data, threshold=5):
    features_to_remove = vif_data[vif_data["Tolerance"] > threshold]["feature"]
    data = data.drop(columns=features_to_remove)
    vif_data = vif_data[~vif_data["feature"].isin(features_to_remove)]
    return data, vif_data

if __name__ == "__main__":
    df = pd.read_csv('../Train_knight.csv')
    numeric_data = df.select_dtypes(include=[np.number])

    vif_data_1 = calculate_vif_1(numeric_data)
    print("Initial VIF:\n", vif_data_1.to_string(index=False))

    final_data_1, final_vif_1 = remove_high_tolerance_features(numeric_data, vif_data_1)
    print("\nFinal VIF:\n", final_vif_1.to_string(index=False))

    print("\n------------\n")

    vif_data_2 = calculate_vif_2(numeric_data)
    print("Initial VIF:\n", vif_data_2.to_string(index=False))

    final_data_2, final_vif_2 = remove_high_tolerance_features(numeric_data, vif_data_2)
    print("\nFinal VIF:\n", final_vif_2.to_string(index=False))
