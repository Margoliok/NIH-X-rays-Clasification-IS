(.venv) PS C:\Users\Aitukka\Desktop\ZIP project> python main.py --resume --ckpt stage3_1e-05_09.pth --stage 4

device: cuda
RESUMING THE MODEL TRAINING

data\NIH Chest X-rays\Data_Entry_2017.csv found: True
self.df.shape: (112120, 2)

train_val_df.pickle: loaded

self.train_val_df.shape: (86524, 2)

Sampling the huuuge training dataset
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 86524/86524 [00:01<00:00, 69003.01it/s]

disease_classes.pickle: already exists

self.all_classes_dict: {'Effusion': 7997, 'Infiltration': 10005, 'No Finding': 10000, 'Atelectasis': 7699, 'Pneumothorax': 2535, 'Mass': 3844, 'Consolidation': 2642, 'Nodule': 4426, 'Fibrosis': 1167, 'Emphysema': 1365, 'Pneumonia': 772, 'Pleural_Thickening': 2138, 'Cardiomegaly': 1622, 'Edema': 1208, 'Hernia': 141}

self.df.shape: (112120, 2)

test_df.pickle: loaded
self.test_df.shape: (25596, 2)

-----Initial Dataset Information-----
num images in train_dataset   : 33791
num images in val_dataset     : 8448
num images in XRayTest_dataset: 25596
-------------------------------------

-----Initial Batchloaders Information -----
num batches in train_loader: 264
num batches in val_loader  : 66
num batches in test_loader : 200
-------------------------------------------

we are working with 
Images shape: torch.Size([3, 224, 224]) and 
Target shape: torch.Size([15])

ckpt loaded: stage3_1e-05_09.pth

> loss_fn: FocalLoss()
> epochs_till_now: 9
> batch_size: 128
> stage: 4
> lr: 1e-05

----- STAGE 4 -----

following are the trainable layers...
['fc']

we have 0.030735 Million trainable parameters here in the ResNet model

======= Training after epoch #9... =======

============ EPOCH 10/12 ============
TRAINING
libpng warning: iCCP: profile 'ICC Profile': 'GRAY': Gray color space not permitted on RGB PNG
Train Loss for batch 025/264 @epoch10/12: 0.0263 in 0 mins 2.86 secs
libpng warning: iCCP: profile 'ICC Profile': 'GRAY': Gray color space not permitted on RGB PNG
Train Loss for batch 050/264 @epoch10/12: 0.02926 in 0 mins 2.3 secs
Train Loss for batch 075/264 @epoch10/12: 0.02959 in 0 mins 2.41 secs
Train Loss for batch 100/264 @epoch10/12: 0.02619 in 0 mins 2.57 secs
Train Loss for batch 125/264 @epoch10/12: 0.02697 in 0 mins 2.42 secs
Train Loss for batch 150/264 @epoch10/12: 0.02463 in 0 mins 2.5 secs
Train Loss for batch 175/264 @epoch10/12: 0.02852 in 0 mins 2.21 secs
Train Loss for batch 200/264 @epoch10/12: 0.02839 in 0 mins 2.45 secs
Train Loss for batch 225/264 @epoch10/12: 0.0271 in 0 mins 2.45 secs
Train Loss for batch 250/264 @epoch10/12: 0.02669 in 0 mins 2.45 secs
VALIDATION
Val Loss   for batch 025/066 @epoch10/12: 0.02463 in 0 mins 2.44 secs
Val Loss   for batch 050/066 @epoch10/12: 0.02334 in 0 mins 2.49 secs

NoFindingIndex:  10
y_true.shape, y_probs.shape  (8448, 15) (8448, 15)

class_roc_auc_list:  [0.9873633606350045, 0.9977523719222751, 0.9801163560172285, 0.9928603828566716, 0.9929150674639602, 0.9979709114606475, 0.9904023839582343, 0.9966032057245974, 0.9145396361439215, 0.9955147290667317, 0.8685812588713915, 0.9850958588631535, 0.9932834343608754, 0.9835106494949963, 0.9973749084387866]

useful_classes_roc_auc_list [0.9873633606350045, 0.9977523719222751, 0.9801163560172285, 0.9928603828566716, 0.9929150674639602, 0.9979709114606475, 0.9904023839582343, 0.9966032057245974, 0.9145396361439215, 0.9955147290667317, 0.9850958588631535, 0.9932834343608754, 0.9835106494949963, 0.9973749084387866]

checkpoint models\stage4_1e-05_10.pth saved
loss plots saved !!!

TRAIN LOSS : 0.026818856163793935
VAL   LOSS : 0.025557581561081337
VAL ROC_AUC: 0.9860930897433633

Epoch 10/12 took 0 h 13 m

Sampling the huuuge training dataset
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 86524/86524 [00:01<00:00, 59393.98it/s]

self.all_classes_dict: {'Mass': 3824, 'Effusion': 7992, 'No Finding': 10000, 'Pleural_Thickening': 2107, 'Atelectasis': 7694, 'Infiltration': 10009, 'Pneumonia': 788, 'Edema': 1245, 'Consolidation': 2634, 'Nodule': 4453, 'Cardiomegaly': 1646, 'Pneumothorax': 2541, 'Emphysema': 1368, 'Fibrosis': 1183, 'Hernia': 141}

-----Resampled Dataset Information-----
num images in train_dataset   : 33792
num images in val_dataset     : 8448
---------------------------------------

-----Resampled Batchloaders Information -----
num batches in train_loader: 264
num batches in val_loader  : 66
---------------------------------------------

============ EPOCH 11/12 ============
TRAINING
Train Loss for batch 025/264 @epoch11/12: 0.0279 in 0 mins 2.46 secs
Train Loss for batch 050/264 @epoch11/12: 0.02672 in 0 mins 2.43 secs
Train Loss for batch 075/264 @epoch11/12: 0.02578 in 0 mins 2.47 secs
Train Loss for batch 100/264 @epoch11/12: 0.02506 in 0 mins 2.51 secs
Train Loss for batch 125/264 @epoch11/12: 0.02404 in 0 mins 2.5 secs
Train Loss for batch 150/264 @epoch11/12: 0.02685 in 0 mins 2.48 secs
Train Loss for batch 175/264 @epoch11/12: 0.02472 in 0 mins 2.5 secs
libpng warning: iCCP: profile 'ICC Profile': 'GRAY': Gray color space not permitted on RGB PNG
Train Loss for batch 200/264 @epoch11/12: 0.02543 in 0 mins 2.53 secs
Train Loss for batch 225/264 @epoch11/12: 0.02598 in 0 mins 2.49 secs
libpng warning: iCCP: profile 'ICC Profile': 'GRAY': Gray color space not permitted on RGB PNG
Train Loss for batch 250/264 @epoch11/12: 0.02399 in 0 mins 2.54 secs
VALIDATION
Val Loss   for batch 025/066 @epoch11/12: 0.02363 in 0 mins 2.59 secs
Val Loss   for batch 050/066 @epoch11/12: 0.02469 in 0 mins 2.6 secs

NoFindingIndex:  10
y_true.shape, y_probs.shape  (8448, 15) (8448, 15)

class_roc_auc_list:  [0.987180553746971, 0.9980918702095543, 0.9824802705858326, 0.9938544950258675, 0.9933835649005928, 0.9983005162080483, 0.9928707293572159, 0.9980865133441719, 0.9161433680810082, 0.995588912798801, 0.872362900000152, 0.9841637027374506, 0.9928367729636229, 0.9779068879693393, 0.9973880221439356]

useful_classes_roc_auc_list [0.987180553746971, 0.9980918702095543, 0.9824802705858326, 0.9938544950258675, 0.9933835649005928, 0.9983005162080483, 0.9928707293572159, 0.9980865133441719, 0.9161433680810082, 0.995588912798801, 0.9841637027374506, 0.9928367729636229, 0.9779068879693393, 0.9973880221439356]

checkpoint models\stage4_1e-05_11.pth saved
loss plots saved !!!

TRAIN LOSS : 0.026524737434969706
VAL   LOSS : 0.02542816297235814
VAL ROC_AUC: 0.9863054414337437

Epoch 11/12 took 0 h 13 m

Sampling the huuuge training dataset
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 86524/86524 [00:01<00:00, 59112.73it/s]

self.all_classes_dict: {'Infiltration': 10003, 'Pneumothorax': 2524, 'No Finding': 10000, 'Nodule': 4422, 'Pleural_Thickening': 2121, 'Cardiomegaly': 1617, 'Pneumonia': 782, 'Consolidation': 2649, 'Effusion': 7980, 'Mass': 3832, 'Atelectasis': 7687, 'Fibrosis': 1179, 'Edema': 1202, 'Emphysema': 1366, 'Hernia': 141}

-----Resampled Dataset Information-----
num images in train_dataset   : 33791
num images in val_dataset     : 8448
---------------------------------------

-----Resampled Batchloaders Information -----
num batches in train_loader: 264
num batches in val_loader  : 66
---------------------------------------------

============ EPOCH 12/12 ============
TRAINING
Train Loss for batch 025/264 @epoch12/12: 0.02782 in 0 mins 2.53 secs
Train Loss for batch 050/264 @epoch12/12: 0.0234 in 0 mins 2.49 secs
Train Loss for batch 075/264 @epoch12/12: 0.02933 in 0 mins 2.46 secs
Train Loss for batch 100/264 @epoch12/12: 0.02521 in 0 mins 2.55 secs
Train Loss for batch 125/264 @epoch12/12: 0.02399 in 0 mins 2.63 secs
libpng warning: iCCP: profile 'ICC Profile': 'GRAY': Gray color space not permitted on RGB PNG
Train Loss for batch 150/264 @epoch12/12: 0.02532 in 0 mins 2.56 secs
Train Loss for batch 175/264 @epoch12/12: 0.02724 in 0 mins 2.52 secs
Train Loss for batch 200/264 @epoch12/12: 0.02334 in 0 mins 2.53 secs
Train Loss for batch 225/264 @epoch12/12: 0.02763 in 0 mins 2.45 secs
Train Loss for batch 250/264 @epoch12/12: 0.02421 in 0 mins 2.5 secs
VALIDATION
libpng warning: iCCP: profile 'ICC Profile': 'GRAY': Gray color space not permitted on RGB PNG
Val Loss   for batch 025/066 @epoch12/12: 0.02725 in 0 mins 2.52 secs
Val Loss   for batch 050/066 @epoch12/12: 0.02407 in 0 mins 2.49 secs

NoFindingIndex:  10
y_true.shape, y_probs.shape  (8448, 15) (8448, 15)

class_roc_auc_list:  [0.9874745899032144, 0.997834511640883, 0.9777985038422727, 0.9913781497166148, 0.9931537660948253, 0.9983688750107976, 0.9912609546088758, 0.9977397097311445, 0.9182479916096399, 0.9948853309369846, 0.865658992325659, 0.9845372812972224, 0.9928548400046165, 0.9830897587863036, 0.9977802493291287]

useful_classes_roc_auc_list [0.9874745899032144, 0.997834511640883, 0.9777985038422727, 0.9913781497166148, 0.9931537660948253, 0.9983688750107976, 0.9912609546088758, 0.9977397097311445, 0.9182479916096399, 0.9948853309369846, 0.9845372812972224, 0.9928548400046165, 0.9830897587863036, 0.9977802493291287]

checkpoint models\stage4_1e-05_12.pth saved
loss plots saved !!!

TRAIN LOSS : 0.026337025553812243
VAL   LOSS : 0.025242458944293587
VAL ROC_AUC: 0.9861717508937516

Epoch 12/12 took 0 h 13 m
0 h 41m laga poore script me !