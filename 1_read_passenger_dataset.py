from google.colab import drive
# Mount Google Drive
drive.mount('/content/drive')
# Read and print the contents of a CSV file from Google Drive
import pandas as pd
a = pd.read_csv('/content/drive/MyDrive/passenger_dataset (1).csv')
print(a)
