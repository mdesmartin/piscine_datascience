import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import f1_score
import matplotlib.pyplot as plt
import sys

def main():
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    train_data = pd.read_csv('../Training_knight.csv')
    validation_data = pd.read_csv('../Validation_knight.csv')

    X_train = train_data.drop(columns=['knight'])
    y_train = train_data['knight']
    X_val = validation_data.drop(columns=['knight'])
    y_val = validation_data['knight']

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred_val = model.predict(X_val)

    f1 = f1_score(y_val, y_pred_val, pos_label='Jedi')
    print(f"F1-score on validation set: {f1}")

    if f1 < 0.9:
        print("The model did not meet the required F1-score of 90%.")
    else:
        print("The model meets the required F1-score of 90%.")

    with open('Tree.txt', 'w') as f:
        for prediction in y_pred_val:
            f.write(f"{prediction}\n")

    plt.figure(figsize=(20, 10))
    plot_tree(model, filled=True, feature_names=X_train.columns, class_names=model.classes_, rounded=True)
    plt.show()

if __name__ == "__main__":
    main()
