#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ author: Bereket Kebede
"""
########################################################
# Import Necessary Libraries

from xlwt import *
import numpy as np
import os
import math
import torch
from torch.utils.data import DataLoader
from skimage import io, transform
import sys

path = '/home/star/0_code_lhj/DL-SIM-github/Training_codes/UNet/'
sys.path.append(path)

from unet_model import UNet


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        data_in, data_out = sample['image_in'], sample['groundtruth']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C X H X W
        # image = image.transpose((2, 0, 1))
        # landmarks = landmarks.transpose((2, 0, 1))

        # return {'image': image, 'landmarks': torch.from_numpy(landmarks)}
        return {'image_in': torch.from_numpy(data_in),
                'groundtruth': torch.from_numpy(data_out)}


class ReconsDataset(torch.utils.data.Dataset):
    def __init__(self, train_in_path, train_gt_path, transform, img_type, in_size):
        self.train_in_path = train_in_path
        self.train_gt_path = train_gt_path
        self.transform = transform
        self.img_type = img_type
        self.in_size = in_size
        self.dirs_gt = os.listdir(self.train_gt_path)

    def __len__(self):
        dirs = os.listdir(self.train_gt_path)  # open the files
        return len(dirs)  # because one of the file is for groundtruth

    def __getitem__(self, idx):
        image_name = os.path.join(self.train_gt_path, self.dirs_gt[idx])
        data_gt = io.imread(image_name)
        max_out = 15383.0
        data_gt = data_gt / max_out

        filepath = os.path.join(self.train_in_path, self.dirs_gt[idx][:-4])
        # filepath = os.listdir(filepath)
        # train_in_size = len(filepath)
        train_in_size = 3

        data_in = np.zeros((self.in_size, self.in_size, train_in_size))
        filepath = os.path.join(self.train_in_path, self.dirs_gt[idx][:-4])
        for i in range(train_in_size):
            ii = i * 5
            if ii <= 9:
                image_name = os.path.join(filepath, "HE_0" + str(ii) + "." + self.img_type)
            else:
                image_name = os.path.join(filepath, "HE_" + str(ii) + "." + self.img_type)
            image = io.imread(image_name)
            data_in[:, :, i] = image
        max_in = 5315.0
        data_in = data_in / max_in
        sample = {'image_in': data_in, 'groundtruth': data_gt}

        if self.transform:
            sample = self.transform(sample)
        return sample


def get_learning_rate(epoch):
    limits = [3, 8, 12]
    lrs = [1, 0.1, 0.05, 0.005]
    assert len(lrs) == len(limits) + 1
    for lim, lr in zip(limits, lrs):
        if epoch < lim:
            return lr * learning_rate
        return lrs[-1] * learning_rate


def val_during_training(dataloader):
    model.eval()

    loss_all = np.zeros((len(dataloader)))
    for batch_idx, items in enumerate(dataloader):
        image = items['image_in']
        gt = items['groundtruth']

        image = np.swapaxes(image, 1, 3)
        image = np.swapaxes(image, 2, 3)
        image = image.float()
        image = image.cuda(cuda)

        gt = gt.squeeze()
        gt = gt.float()
        gt = gt.cuda(cuda)

        pred = model(image).squeeze()
        loss0 = (pred - gt).abs().mean()

        loss_all[batch_idx] = loss0.item()

    mae_m, mae_s = loss_all.mean(), loss_all.std()
    return mae_m, mae_s


if __name__ == "__main__":
    cuda = torch.device('cuda:0')
    learning_rate = 0.001
    # momentum = 0.99
    # weight_decay = 0.0001
    batch_size = 1

    SRRFDATASET = ReconsDataset(
        train_in_path="D:\Bereket\microtubule\Training_Testing_microtubules\HE_X2",
        train_gt_path="D:\Bereket\microtubule\Training_Testing_microtubules\HER",
        transform=ToTensor(),
        img_type='tif',
        in_size=256)
    train_dataloader = torch.utils.data.DataLoader(SRRFDATASET, batch_size=batch_size, shuffle=True,
                                                   pin_memory=True)  # better than for loop

    SRRFDATASET2 = ReconsDataset(
        train_in_path="D:/Bereket/microtubule/Training_Testing_microtubules/testing_HE_X2",
        train_gt_path="D:/Bereket/microtubule/Training_Testing_microtubules/testing_HER",
        transform=ToTensor(),
        img_type='tif',
        in_size=256)
    validation_dataloader = torch.utils.data.DataLoader(SRRFDATASET2, batch_size=batch_size, shuffle=True,
                                                        pin_memory=True)  # better than for loop

    model = UNet(n_channels=3, n_classes=1)

    print("{} paramerters in total".format(sum(x.numel() for x in model.parameters())))
    model.cuda(cuda)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate, betas=(0.9, 0.999))

    loss_all = np.zeros((2000, 4))
    for epoch in range(2000):

        mae_m, mae_s = val_during_training(train_dataloader)
        loss_all[epoch, 0] = mae_m
        loss_all[epoch, 1] = mae_s
        mae_m, mae_s = val_during_training(validation_dataloader)
        loss_all[epoch, 2] = mae_m
        loss_all[epoch, 3] = mae_s

        file = Workbook(encoding='utf-8')
        table = file.add_sheet('loss_all')
        for i, p in enumerate(loss_all):
            for j, q in enumerate(p):
                table.write(i, j, q)
        file.save('D:/Bereket/DeepLearning/Training_codes/UNet/loss_UNet_SIM3_microtubule.xls')

        lr = get_learning_rate(epoch)
        for p in optimizer.param_groups:
            p['lr'] = lr
            print("learning rate = {}".format(p['lr']))

        for batch_idx, items in enumerate(train_dataloader):
            image = items['image_in']
            gt = items['groundtruth']

            model.train()

            image = np.swapaxes(image, 1, 3)
            image = np.swapaxes(image, 2, 3)
            image = image.float()
            image = image.cuda(cuda)

            gt = gt.squeeze()
            gt = gt.float()
            gt = gt.cuda(cuda)

            pred = model(image).squeeze()

            loss = (pred - gt).abs().mean() + 5 * ((pred - gt) ** 2).mean()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            print("[Epoch %d] [Batch %d/%d] [loss: %f]" % (epoch, batch_idx, len(train_dataloader), loss.item()))
        torch.save(model.state_dict(),
                   "D:/Bereket/DeepLearning/Training_codes/UNet/UNet_SIM3_microtubule.pkl")
