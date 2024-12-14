import pandas as pd
from sklearn.model_selection import train_test_split
import sys

def split_data(input_file, train_file, val_file, test_size=0.2):
    df = pd.read_csv(input_file)

    df = df.sample(frac=1).reset_index(drop=True)
    train_df, val_df = train_test_split(df, test_size=test_size)

    train_df.to_csv(train_file, index=False)
    val_df.to_csv(val_file, index=False)

    print(f"Training set   : {len(train_df)} rows ({100 - test_size * 100}%)")
    print(f"Validation set : {len(val_df)} rows ({test_size * 100}%)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python split.py Train_knight.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    train_file = "Training_knight.csv"
    val_file = "Validation_knight.csv"

    split_data(input_file, train_file, val_file)
