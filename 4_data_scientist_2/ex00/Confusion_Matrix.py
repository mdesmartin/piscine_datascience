import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_confusion_matrix(y_true, y_pred, labels):
    cm = [[0, 0], [0, 0]]
    label_map = {label: idx for idx, label in enumerate(labels)}

    for true, pred in zip(y_true, y_pred):
        cm[label_map[true]][label_map[pred]] += 1

    return cm

def calculate_metrics(cm):
    tp0, fp0, fn0, tp1, fp1, fn1 = cm[0][0], cm[1][0], cm[0][1], cm[1][1], cm[0][1], cm[1][0]

    precision0 = tp0 / (tp0 + fp0) if (tp0 + fp0) > 0 else 0
    recall0 = tp0 / (tp0 + fn0) if (tp0 + fn0) > 0 else 0
    f1_0 = 2 * (precision0 * recall0) / (precision0 + recall0) if (precision0 + recall0) > 0 else 0

    precision1 = tp1 / (tp1 + fp1) if (tp1 + fp1) > 0 else 0
    recall1 = tp1 / (tp1 + fn1) if (tp1 + fn1) > 0 else 0
    f1_1 = 2 * (precision1 * recall1) / (precision1 + recall1) if (precision1 + recall1) > 0 else 0

    accuracy = (tp0 + tp1) / (tp0 + tp1 + fp0 + fp1)

    return precision0, recall0, f1_0, precision1, recall1, f1_1, accuracy

def display_confusion_matrix(cm, labels):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

def confusion_matrix_analysis(input_prediction, input_truth):
    prediction_df = pd.read_csv(input_prediction, delimiter="\t", header=None, names=["Prediction"])
    truth_df = pd.read_csv(input_truth, delimiter="\t", header=None, names=["Truth"])

    y_true = truth_df["Truth"].values
    y_pred = prediction_df["Prediction"].values

    labels = sorted(set(y_true).union(set(y_pred)))
    cm = calculate_confusion_matrix(y_true, y_pred, labels)

    precision0, recall0, f1_0, precision1, recall1, f1_1, accuracy = calculate_metrics(cm)

    print("Confusion Matrix:")
    print(cm)

    print("\nMetrics:")
    print(f"{'Class':<10} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Total':<10}")
    print(f"{labels[0]:<10} {precision0:<10.2f} {recall0:<10.2f} {f1_0:<10.2f} {sum(y_true == labels[0]):<10}")
    print(f"{labels[1]:<10} {precision1:<10.2f} {recall1:<10.2f} {f1_1:<10.2f} {sum(y_true == labels[1]):<10}")
    print(f"{'Accuracy':<10} {accuracy:<10.2f} {'':<10} {'':<10} {len(y_true):<10}")

    display_confusion_matrix(cm, labels=labels)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Confusion_Matrix.py prediction.txt truth.txt")
        sys.exit(1)

    input_prediction = sys.argv[1]
    input_truth = sys.argv[2]

    confusion_matrix_analysis(input_prediction, input_truth)
