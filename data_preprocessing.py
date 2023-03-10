import pandas as pd
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE 

class ClassBalance:
    def __init__(self, X: pd.DataFrame, y: pd.Series):
        self.X = X
        self.y = y
        self.data = pd.concat([X, y], axis=1)
        
    def resampling(self, balance_treshs: dict):

        list_of_balanced = []
        for (class_label, balance_thresh) in balance_treshs.items():

            resampled_data_class = resample(self.data[self.y==class_label], random_state=42, 
                                            replace=True, n_samples=balance_thresh)
            list_of_balanced.append(resampled_data_class)
        
        resampled_data = pd.concat(list_of_balanced)

        print(resampled_data.expert_PAM50_subtype.value_counts())

        return resampled_data

    def resampling_with_generation(self, sampling_strategy: dict):

        new_list_data = []
        for (label, value) in sampling_strategy.items():
            counts = (self.y==label).sum()
            if  counts > value:
                downsampled_data = resample(self.data[self.y==label], random_state=42, 
                                            replace=True, n_samples=value)
                new_list_data.append(downsampled_data)
            else:
                new_list_data.append(self.data[self.y==label])

        data_cut = pd.concat(new_list_data)
        X = data_cut.drop(columns='expert_PAM50_subtype', inplace=False)
        y = data_cut.expert_PAM50_subtype

        smote = SMOTE(sampling_strategy=sampling_strategy, random_state=42, k_neighbors=5)
        X_smote, y_smote = smote.fit_resample(X, y.ravel())
        y_smote = pd.DataFrame(y_smote, columns=['expert_PAM50_subtype'])
        print('Balance status after SMOTE:\n')
        print(y_smote.value_counts())

        return pd.concat([X_smote, y_smote], axis=1)



