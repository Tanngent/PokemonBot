import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from sklearn import preprocessing
import numpy as np

pd.options.display.max_rows = 10

class battleDataset(Dataset):
    def __init__(self, fileList):
        df_each = (pd.read_csv(f, keep_default_na=False, header=None, encoding='unicode_escape') for f in fileList)
        self.df = pd.concat(df_each, ignore_index=True)

        print(self.df.head())

        pokemonsCols = [0, 13, 26, 39, 52, 65, 78, 91, 104, 117, 130, 143]
        moveCols = [4, 5, 6, 7, 17, 18, 19, 20, 30, 31, 32, 33, 43, 44, 45, 46, 56, 57, 58, 59, 69, 70, 71, 72, 82, 83, 84, 85, 95, 96, 97, 98, 108, 109, 110, 111, 121, 122, 123, 124, 134, 135, 136, 137, 147, 148, 149, 150]
        statusCols = [3, 16, 29, 42, 55, 68, 81, 94, 107, 120, 133, 146]
        choiceCol = [164]
        

        le = preprocessing.LabelEncoder()

        #print(self.df[pokemonsCols].head())
        pokemonList = np.unique(self.df[pokemonsCols])
        le.fit(pokemonList)
        self.df[pokemonsCols] = self.df[pokemonsCols].apply(le.transform)
        #print(pokemonList)
        #print(self.df[pokemonsCols].head())
        print(le.classes_)

        #print(self.df[moveCols].head())
        moveList = np.unique(self.df[moveCols])
        le.fit(moveList)
        self.df[moveCols] = self.df[moveCols].apply(le.transform)
        #print(moveList)
        #print(self.df[moveCols].head())
        print(le.classes_)

        #print(self.df[statusCols].head())
        statusList = np.unique(self.df[statusCols])
        le.fit(statusList)
        self.df[statusCols] = self.df[statusCols].apply(le.transform)
        #print(statusList)
        #print(self.df[statusCols].head())
        print(le.classes_)

        #print(self.df[choiceCol].head())
        choiceList = np.unique(self.df[choiceCol])
        le.fit(choiceList)
        self.df[choiceCol] = self.df[choiceCol].apply(le.transform)
        #print(choiceList)
        #print(self.df[choiceCol].head())
        print(le.classes_)

        print(self.df.head())

    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        
        state = self.df.iloc[idx][0:165]
        outcome = self.df.iloc[idx][165]
        sample = {'state':state, 'outcome':outcome}

        return sample

newDataset = battleDataset(["train1.csv","train2.csv"])
print(newDataset.__len__())
for i in range(len(newDataset)):
    sample = newDataset[i]

    print(sample['state'])
    print(sample['outcome'])
    print("________")

    if i == 3:
        break