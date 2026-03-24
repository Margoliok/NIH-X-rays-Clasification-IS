(.venv) PS C:\Users\Aitukka\Desktop\ZIP project> python main.py --test --ckpt stage4_1e-05_12.pth  

device: cuda

Overwriting stage to 1, as the model training is being done from scratch
TESTING THE MODEL

data\NIH Chest X-rays\Data_Entry_2017.csv found: True
self.df.shape: (112120, 2)

train_val_df.pickle: loaded

self.train_val_df.shape: (86524, 2)

Sampling the huuuge training dataset
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 86524/86524 [00:01<00:00, 63257.41it/s]

disease_classes.pickle: already exists

self.all_classes_dict: {'Cardiomegaly': 1631, 'Effusion': 8000, 'Infiltration': 10006, 'Consolidation': 2660, 'Pneumothorax': 2520, 'Nodule': 4397, 'No Finding': 10000, 'Atelectasis': 7704, 'Mass': 3844, 'Emphysema': 1355, 'Pleural_Thickening': 2152, 'Edema': 1224, 'Pneumonia': 784, 'Fibrosis': 1177, 'Hernia': 141}

self.df.shape: (112120, 2)

test_df.pickle: loaded
self.test_df.shape: (25596, 2)

-----Initial Dataset Information-----
num images in train_dataset   : 33793
num images in val_dataset     : 8449
num images in XRayTest_dataset: 25596
-------------------------------------

-----Initial Batchloaders Information -----
num batches in train_loader: 265
num batches in val_loader  : 67
num batches in test_loader : 200
-------------------------------------------

we are working with 
Images shape: torch.Size([3, 224, 224]) and 
Target shape: torch.Size([15])

checkpoint loaded: stage4_1e-05_12.pth

======= Testing... =======

200/200 (100.00 %)
NoFindingIndex:  10
y_true.shape, y_probs.shape  (25596, 15) (25596, 15)

class_roc_auc_list:  [0.6978753275104188, 0.8407285104523706, 0.6674850619802853, 0.8063070220315569, 0.7759030105485122, 0.8595517310481878, 0.7562702175004465, 0.8300830499667252, 0.6341095981492668, 0.7257332168378372, 0.6992751518106768, 0.6702156248433009, 0.7084497161855912, 0.631503109674908, 0.7982056046596433]

useful_classes_roc_auc_list [0.6978753275104188, 0.8407285104523706, 0.6674850619802853, 0.8063070220315569, 0.7759030105485122, 0.8595517310481878, 0.7562702175004465, 0.8300830499667252, 0.6341095981492668, 0.7257332168378372, 0.6702156248433009, 0.7084497161855912, 0.631503109674908, 0.7982056046596433]
test_roc_auc: 0.743030057242075 in 8 mins 26 secs