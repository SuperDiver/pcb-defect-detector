# 记录训练参数、mAP 变化、踩坑修复过程

## 实验名称

pcb_yolov8s_stable

## 训练参数

- Model: YOLOv8s (11.1M params)
- Dataset: PCB Defects v6 (Roboflow)
- Train/Val: 10,710 / 2,616 images
- Epochs: 50
- Batch: 16
- Imgsz: 640
- Optimizer: AdamW (auto)
- Lr: 0.01
- Patience: 15

## 关键决策

- 选择了 YOLOv8s 而非 nano：在精度和速度之间取得平衡
- 全量 10,710 张训练，未抽子集以获得更高 mAP
- ONNX 导出后加速不明显，因 v8s 推理时间接近数据拷贝时间
- TensorRT 未在 Windows 环境安装，留待 Linux 部署时测试

## mAP 收敛过程

- 10 epoch: mAP50 ≈ 0.85
- 20 epoch: mAP50 ≈ 0.94
- 30 epoch: mAP50 ≈ 0.98
- 50 epoch: mAP50 ≈ 0.99 (final)

## 踩坑记录

1. torch multiprocessing Windows 报错 → 加 `if __name__ == '__main__'`
2. `--extra-index-url` 在 Windows 上不生效 → 改用 `--index-url` 显式指定 PyTorch CUDA 源
3. 初始用随机 tensor benchmark 报归一化警告 → 改用真实图片路径

## 第一次测试

(pcb-yolo) D:\Workspace\pcb-defect-detector\data>python -c "from ultralytics import YOLO; model = YOLO('yolov8s.pt'); model.train(data=r'D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\data.yaml', epochs=1, batch=4, imgsz=640, device='cuda:0', name='dry_run')"
WARNING Download failure, retrying 1/3 https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8s.pt... <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (\_ssl.c:1017)>
-=O=- # # # # curl: (28) Failed to connect to github.com port 443 after 21054 ms: Could not connect to server
Warning: Problem : timeout. Will retry in 1 second. 3 retries left.
-=O=- # # ## curl: (28) Failed to connect to github.com port 443 after 21043 ms: Could not connect to server
Warning: Problem : timeout. Will retry in 2 seconds. 2 retries left.
-=O=- # # # # curl: (28) Failed to connect to github.com port 443 after 21046 ms: Could not connect to server
Warning: Problem : timeout. Will retry in 4 seconds. 1 retry left.
-=O=-# # # # curl: (28) Failed to connect to github.com port 443 after 21059 ms: Could not connect to server

WARNING Download failure, retrying 2/3 https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov8s.pt... Curl return value 28
-=O=- # # # # curl: (28) Failed to connect to github.com port 443 after 21059 ms: Could not connect to server
Warning: Problem : timeout. Will retry in 1 second. 3 retries left.
-=O=- # # ## curl: (28) Failed to connect to github.com port 443 after 21029 ms: Could not connect to server
Warning: Problem : timeout. Will retry in 2 seconds. 2 retries left.
###################################################################################################################################################### 100.0%
Ultralytics 8.4.75 Python-3.10.20 torch-2.6.0+cu124 CUDA:0 (NVIDIA GeForce RTX 4060 Laptop GPU, 8188MiB)
engine\trainer: agnostic_nms=False, amp=True, angle=1.0, augment=False, auto_augment=randaugment, batch=4, bgr=0.0, box=7.5, cache=False, cfg=None, classes=None, close_mosaic=10, cls=0.5, cls_pw=0.0, compile=False, conf=None, copy_paste=0.0, copy_paste_mode=flip, cos_lr=False, cutmix=0.0, data=D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\data.yaml, degrees=0.0, deterministic=True, device=0, dfl=1.5, dnn=False, dropout=0.0, dynamic=False, embed=None, end2end=None, epochs=1, erasing=0.4, exist_ok=False, fliplr=0.5, flipud=0.0, format=torchscript, fraction=1.0, freeze=None, half=False, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, imgsz=640, int8=False, iou=0.7, keras=False, kobj=1.0, line_width=None, lr0=0.01, lrf=0.01, mask_ratio=4, max_det=300, mixup=0.0, mode=train, model=yolov8s.pt, momentum=0.937, mosaic=1.0, multi_scale=0.0, name=dry_run, nbs=64, nms=False, opset=None, optimize=False, optimizer=auto, overlap_mask=True, patience=100, perspective=0.0, plots=True, pose=12.0, pretrained=True, profile=False, project=None, rect=False, resume=False, retina_masks=False, rle=1.0, save=True, save_conf=False, save_crop=False, save_dir=D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run, save_frames=False, save_json=False, save_period=-1, save_txt=False, scale=0.5, seed=0, shear=0.0, show=False, show_boxes=True, show_conf=True, show_labels=True, simplify=True, single_cls=False, source=None, split=val, stream_buffer=False, task=detect, time=None, tracker=botsort.yaml, translate=0.1, val=True, verbose=True, vid_stride=1, visualize=False, warmup_bias_lr=0.1, warmup_epochs=3.0, warmup_momentum=0.8, weight_decay=0.0005, workers=8, workspace=None
Overriding model.yaml nc=80 with nc=6

                   from  n    params  module                                       arguments

0 -1 1 928 ultralytics.nn.modules.conv.Conv [3, 32, 3, 2]
1 -1 1 18560 ultralytics.nn.modules.conv.Conv [32, 64, 3, 2]
2 -1 1 29056 ultralytics.nn.modules.block.C2f [64, 64, 1, True]
3 -1 1 73984 ultralytics.nn.modules.conv.Conv [64, 128, 3, 2]
4 -1 2 197632 ultralytics.nn.modules.block.C2f [128, 128, 2, True]
5 -1 1 295424 ultralytics.nn.modules.conv.Conv [128, 256, 3, 2]
6 -1 2 788480 ultralytics.nn.modules.block.C2f [256, 256, 2, True]
7 -1 1 1180672 ultralytics.nn.modules.conv.Conv [256, 512, 3, 2]
8 -1 1 1838080 ultralytics.nn.modules.block.C2f [512, 512, 1, True]
9 -1 1 656896 ultralytics.nn.modules.block.SPPF [512, 512, 5]
10 -1 1 0 torch.nn.modules.upsampling.Upsample [None, 2, 'nearest']
11 [-1, 6] 1 0 ultralytics.nn.modules.conv.Concat [1]
12 -1 1 591360 ultralytics.nn.modules.block.C2f [768, 256, 1]
13 -1 1 0 torch.nn.modules.upsampling.Upsample [None, 2, 'nearest']
14 [-1, 4] 1 0 ultralytics.nn.modules.conv.Concat [1]
15 -1 1 148224 ultralytics.nn.modules.block.C2f [384, 128, 1]
16 -1 1 147712 ultralytics.nn.modules.conv.Conv [128, 128, 3, 2]
17 [-1, 12] 1 0 ultralytics.nn.modules.conv.Concat [1]
18 -1 1 493056 ultralytics.nn.modules.block.C2f [384, 256, 1]
19 -1 1 590336 ultralytics.nn.modules.conv.Conv [256, 256, 3, 2]
20 [-1, 9] 1 0 ultralytics.nn.modules.conv.Concat [1]
21 -1 1 1969152 ultralytics.nn.modules.block.C2f [768, 512, 1]
22 [15, 18, 21] 1 2118370 ultralytics.nn.modules.head.Detect [6, 16, None, [128, 256, 512]]
Model summary: 130 layers, 11,137,922 parameters, 11,137,906 gradients, 28.7 GFLOPs

Transferred 349/355 items from pretrained weights
Freezing layer 'model.22.dfl.conv.weight'
AMP: running Automatic Mixed Precision (AMP) checks...
Downloading https://github.com/ultralytics/assets/releases/download/v8.4.0/yolo26n.pt to 'yolo26n.pt': 100% ━━━━━━━━━━━━ 5.3MB 4.3MB/s 1.2s
AMP: checks passed
train: Fast image access (ping: 0.60.7 ms, read: 132.520.1 MB/s, size: 63.4 KB)
train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 161 images, 1 backgrounds, 0 corrupt: 1% ──────────── 161/10710 4train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 352 images, 2 backgrounds, 0 corrupt: 3% ──────────── 352/10710 9train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 551 images, 5 backgrounds, 0 corrupt: 5% ╸─────────── 551/10710 1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 752 images, 5 backgrounds, 0 corrupt: 7% ╸─────────── 752/10710 1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 935 images, 7 backgrounds, 0 corrupt: 8% ━─────────── 935/10710 1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1066 images, 7 backgrounds, 0 corrupt: 9% ━─────────── 1066/10710train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1211 images, 7 backgrounds, 0 corrupt: 11% ━─────────── 1211/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1344 images, 7 backgrounds, 0 corrupt: 12% ━╸────────── 1344/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1480 images, 7 backgrounds, 0 corrupt: 13% ━╸────────── 1480/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1622 images, 7 backgrounds, 0 corrupt: 15% ━╸────────── 1622/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1767 images, 7 backgrounds, 0 corrupt: 16% ━╸────────── 1767/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 1892 images, 7 backgrounds, 0 corrupt: 17% ━━────────── 1892/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2016 images, 8 backgrounds, 0 corrupt: 18% ━━────────── 2016/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2144 images, 8 backgrounds, 0 corrupt: 20% ━━────────── 2144/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2275 images, 8 backgrounds, 0 corrupt: 21% ━━╸───────── 2275/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2410 images, 8 backgrounds, 0 corrupt: 22% ━━╸───────── 2410/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2533 images, 8 backgrounds, 0 corrupt: 23% ━━╸───────── 2533/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2655 images, 9 backgrounds, 0 corrupt: 24% ━━╸───────── 2655/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2776 images, 9 backgrounds, 0 corrupt: 25% ━━━───────── 2776/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 2894 images, 9 backgrounds, 0 corrupt: 27% ━━━───────── 2894/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3015 images, 9 backgrounds, 0 corrupt: 28% ━━━───────── 3015/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3133 images, 9 backgrounds, 0 corrupt: 29% ━━━╸──────── 3133/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3255 images, 9 backgrounds, 0 corrupt: 30% ━━━╸──────── 3255/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3375 images, 9 backgrounds, 0 corrupt: 31% ━━━╸──────── 3375/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3499 images, 9 backgrounds, 0 corrupt: 32% ━━━╸──────── 3499/1071train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3633 images, 10 backgrounds, 0 corrupt: 33% ━━━━──────── 3633/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3767 images, 10 backgrounds, 0 corrupt: 35% ━━━━──────── 3767/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 3904 images, 10 backgrounds, 0 corrupt: 36% ━━━━──────── 3904/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4041 images, 10 backgrounds, 0 corrupt: 37% ━━━━╸─────── 4041/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4174 images, 10 backgrounds, 0 corrupt: 38% ━━━━╸─────── 4174/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4308 images, 10 backgrounds, 0 corrupt: 40% ━━━━╸─────── 4308/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4428 images, 11 backgrounds, 0 corrupt: 41% ━━━━╸─────── 4428/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4553 images, 11 backgrounds, 0 corrupt: 42% ━━━━━─────── 4553/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4675 images, 12 backgrounds, 0 corrupt: 43% ━━━━━─────── 4675/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4797 images, 12 backgrounds, 0 corrupt: 44% ━━━━━─────── 4797/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 4917 images, 12 backgrounds, 0 corrupt: 45% ━━━━━╸────── 4917/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5041 images, 13 backgrounds, 0 corrupt: 47% ━━━━━╸────── 5041/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5175 images, 14 backgrounds, 0 corrupt: 48% ━━━━━╸────── 5175/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5307 images, 14 backgrounds, 0 corrupt: 49% ━━━━━╸────── 5307/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5436 images, 14 backgrounds, 0 corrupt: 50% ━━━━━━────── 5436/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5573 images, 16 backgrounds, 0 corrupt: 52% ━━━━━━────── 5573/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5711 images, 16 backgrounds, 0 corrupt: 53% ━━━━━━────── 5711/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5844 images, 16 backgrounds, 0 corrupt: 54% ━━━━━━╸───── 5844/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 5982 images, 16 backgrounds, 0 corrupt: 55% ━━━━━━╸───── 5982/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6117 images, 16 backgrounds, 0 corrupt: 57% ━━━━━━╸───── 6117/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6253 images, 17 backgrounds, 0 corrupt: 58% ━━━━━━━───── 6253/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6400 images, 17 backgrounds, 0 corrupt: 59% ━━━━━━━───── 6400/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6551 images, 17 backgrounds, 0 corrupt: 61% ━━━━━━━───── 6551/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6694 images, 17 backgrounds, 0 corrupt: 62% ━━━━━━━╸──── 6694/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6839 images, 18 backgrounds, 0 corrupt: 63% ━━━━━━━╸──── 6839/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 6994 images, 21 backgrounds, 0 corrupt: 65% ━━━━━━━╸──── 6994/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 7142 images, 21 backgrounds, 0 corrupt: 66% ━━━━━━━━──── 7142/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 7276 images, 22 backgrounds, 0 corrupt: 67% ━━━━━━━━──── 7276/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 7419 images, 22 backgrounds, 0 corrupt: 69% ━━━━━━━━──── 7419/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 7568 images, 22 backgrounds, 0 corrupt: 70% ━━━━━━━━──── 7568/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 7725 images, 23 backgrounds, 0 corrupt: 72% ━━━━━━━━╸─── 7725/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 7882 images, 24 backgrounds, 0 corrupt: 73% ━━━━━━━━╸─── 7882/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8034 images, 24 backgrounds, 0 corrupt: 75% ━━━━━━━━━─── 8034/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8181 images, 25 backgrounds, 0 corrupt: 76% ━━━━━━━━━─── 8181/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8333 images, 26 backgrounds, 0 corrupt: 77% ━━━━━━━━━─── 8333/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8488 images, 26 backgrounds, 0 corrupt: 79% ━━━━━━━━━╸── 8488/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8620 images, 28 backgrounds, 0 corrupt: 80% ━━━━━━━━━╸── 8620/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8738 images, 28 backgrounds, 0 corrupt: 81% ━━━━━━━━━╸── 8738/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8864 images, 28 backgrounds, 0 corrupt: 82% ━━━━━━━━━╸── 8864/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 8991 images, 28 backgrounds, 0 corrupt: 83% ━━━━━━━━━━── 8991/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9127 images, 28 backgrounds, 0 corrupt: 85% ━━━━━━━━━━── 9127/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9258 images, 29 backgrounds, 0 corrupt: 86% ━━━━━━━━━━── 9258/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9392 images, 29 backgrounds, 0 corrupt: 87% ━━━━━━━━━━╸─ 9392/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9525 images, 29 backgrounds, 0 corrupt: 88% ━━━━━━━━━━╸─ 9525/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9660 images, 30 backgrounds, 0 corrupt: 90% ━━━━━━━━━━╸─ 9660/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9798 images, 31 backgrounds, 0 corrupt: 91% ━━━━━━━━━━╸─ 9798/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 9930 images, 31 backgrounds, 0 corrupt: 92% ━━━━━━━━━━━─ 9930/107train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10054 images, 31 backgrounds, 0 corrupt: 93% ━━━━━━━━━━━─ 10054/1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10178 images, 31 backgrounds, 0 corrupt: 95% ━━━━━━━━━━━─ 10178/1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10309 images, 31 backgrounds, 0 corrupt: 96% ━━━━━━━━━━━╸ 10309/1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10425 images, 31 backgrounds, 0 corrupt: 97% ━━━━━━━━━━━╸ 10425/1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10547 images, 31 backgrounds, 0 corrupt: 98% ━━━━━━━━━━━╸ 10547/1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10674 images, 31 backgrounds, 0 corrupt: 99% ━━━━━━━━━━━╸ 10674/1train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels... 10710 images, 31 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 10710/10710 1.4Kit/s 7.9s
train: New cache created: D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels.cache
val: Fast image access (ping: 0.30.1 ms, read: 67.235.3 MB/s, size: 57.5 KB)
val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 120 images, 0 backgrounds, 0 corrupt: 4% ╸─────────── 120/2616 354.val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 236 images, 0 backgrounds, 0 corrupt: 9% ━─────────── 236/2616 592.val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 354 images, 0 backgrounds, 0 corrupt: 13% ━╸────────── 354/2616 766val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 473 images, 0 backgrounds, 0 corrupt: 18% ━━────────── 473/2616 889val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 589 images, 0 backgrounds, 0 corrupt: 22% ━━╸───────── 589/2616 969val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 713 images, 0 backgrounds, 0 corrupt: 27% ━━━───────── 713/2616 1.0val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 833 images, 0 backgrounds, 0 corrupt: 31% ━━━╸──────── 833/2616 1.1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 947 images, 0 backgrounds, 0 corrupt: 36% ━━━━──────── 947/2616 1.1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1077 images, 0 backgrounds, 0 corrupt: 41% ━━━━╸─────── 1077/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1207 images, 0 backgrounds, 0 corrupt: 46% ━━━━━╸────── 1207/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1330 images, 0 backgrounds, 0 corrupt: 50% ━━━━━━────── 1330/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1454 images, 0 backgrounds, 0 corrupt: 55% ━━━━━━╸───── 1454/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1581 images, 0 backgrounds, 0 corrupt: 60% ━━━━━━━───── 1581/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1704 images, 0 backgrounds, 0 corrupt: 65% ━━━━━━━╸──── 1704/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1831 images, 0 backgrounds, 0 corrupt: 69% ━━━━━━━━──── 1831/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 1960 images, 0 backgrounds, 0 corrupt: 74% ━━━━━━━━╸─── 1960/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 2093 images, 0 backgrounds, 0 corrupt: 80% ━━━━━━━━━╸── 2093/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 2220 images, 0 backgrounds, 0 corrupt: 84% ━━━━━━━━━━── 2220/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 2349 images, 0 backgrounds, 0 corrupt: 89% ━━━━━━━━━━╸─ 2349/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 2481 images, 0 backgrounds, 0 corrupt: 94% ━━━━━━━━━━━─ 2481/2616 1val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels... 2616 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 2616/2616 1.2Kit/s 2.1s
val: New cache created: D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels.cache
optimizer: 'optimizer=auto' found, ignoring 'lr0=0.01' and 'momentum=0.937' and determining best 'optimizer', 'lr0' and 'momentum' automatically...
optimizer: AdamW(lr=0.001, momentum=0.9) with parameter groups 57 weight(decay=0.0), 64 weight(decay=0.0005), 63 bias(decay=0.0)
Plotting labels to D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run\labels.jpg...
Image sizes 640 train, 640 val
Using 8 dataloader workers
Logging results to D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run
Starting training for 1 epochs...

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
        1/1      1.09G      2.113      2.781      1.365          4        640: 100% ━━━━━━━━━━━━ 2678/2678 7.6it/s 5:55
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 327/327 9.0it/s 36.2s
                   all       2616       5436      0.854      0.834      0.887      0.381

1 epochs completed in 0.109 hours.
Optimizer stripped from D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run\weights\last.pt, 22.5MB
Optimizer stripped from D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run\weights\best.pt, 22.5MB

Validating D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run\weights\best.pt...
Ultralytics 8.4.75 Python-3.10.20 torch-2.6.0+cu124 CUDA:0 (NVIDIA GeForce RTX 4060 Laptop GPU, 8188MiB)
Model summary (fused): 73 layers, 11,127,906 parameters, 0 gradients, 28.4 GFLOPs
Class Images Instances Box(P R mAP50 mAP50-95): 100% ━━━━━━━━━━━━ 327/327 14.2it/s 23.0s
all 2616 5436 0.855 0.835 0.887 0.381
missing_hole 450 929 0.885 0.968 0.975 0.467
mouse_bite 456 908 0.92 0.878 0.918 0.4
open_circuit 395 821 0.748 0.898 0.868 0.335
short 375 786 0.847 0.762 0.832 0.355
spur 482 1011 0.964 0.64 0.862 0.376
spurious_copper 458 981 0.762 0.864 0.867 0.351
Speed: 0.3ms preprocess, 3.1ms inference, 0.0ms loss, 1.4ms postprocess per image
Results saved to D:\Workspace\pcb-defect-detector\data\runs\detect\dry_run

## 第一次训练

(pcb-yolo) D:\Workspace\pcb-defect-detector>python notebooks\train.py
Ultralytics 8.4.75 Python-3.10.20 torch-2.6.0+cu124 CUDA:0 (NVIDIA GeForce RTX 4060 Laptop GPU, 8188MiB)
engine\trainer: agnostic_nms=False, amp=True, angle=1.0, augment=False, auto_augment=randaugment, batch=8, bgr=0.0, box=7.5, cache=False, cfg=None, classes=None, close_mosaic=10, cls=0.5, cls_pw=0.0, compile=False, conf=None, copy_paste=0.0, copy_paste_mode=flip, cos_lr=False, cutmix=0.0, data=D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\data.yaml, degrees=0.0, deterministic=True, device=0, dfl=1.5, dnn=False, dropout=0.0, dynamic=False, embed=None, end2end=None, epochs=50, erasing=0.4, exist_ok=False, fliplr=0.5, flipud=0.0, format=torchscript, fraction=1.0, freeze=None, half=False, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, imgsz=640, int8=False, iou=0.7, keras=False, kobj=1.0, line_width=None, lr0=0.01, lrf=0.01, mask_ratio=4, max_det=300, mixup=0.0, mode=train, model=yolov8s.pt, momentum=0.937, mosaic=1.0, multi_scale=0.0, name=pcb_yolov8s_stable, nbs=64, nms=False, opset=None, optimize=False, optimizer=auto, overlap_mask=True, patience=15, perspective=0.0, plots=True, pose=12.0, pretrained=True, profile=False, project=None, rect=False, resume=False, retina_masks=False, rle=1.0, save=True, save_conf=False, save_crop=False, save_dir=D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable, save_frames=False, save_json=False, save_period=10, save_txt=False, scale=0.5, seed=0, shear=0.0, show=False, show_boxes=True, show_conf=True, show_labels=True, simplify=True, single_cls=False, source=None, split=val, stream_buffer=False, task=detect, time=None, tracker=botsort.yaml, translate=0.1, val=True, verbose=True, vid_stride=1, visualize=False, warmup_bias_lr=0.1, warmup_epochs=3.0, warmup_momentum=0.8, weight_decay=0.0005, workers=0, workspace=None
Downloading https://ultralytics.com/assets/Arial.ttf to 'C:\Users\Fu\AppData\Roaming\Ultralytics\Arial.ttf': 100% ━━━━━━━━━━━━ 755.1KB 2.0MB/s 0.4s
Overriding model.yaml nc=80 with nc=6

                   from  n    params  module                                       arguments

0 -1 1 928 ultralytics.nn.modules.conv.Conv [3, 32, 3, 2]
1 -1 1 18560 ultralytics.nn.modules.conv.Conv [32, 64, 3, 2]
2 -1 1 29056 ultralytics.nn.modules.block.C2f [64, 64, 1, True]
3 -1 1 73984 ultralytics.nn.modules.conv.Conv [64, 128, 3, 2]
4 -1 2 197632 ultralytics.nn.modules.block.C2f [128, 128, 2, True]
5 -1 1 295424 ultralytics.nn.modules.conv.Conv [128, 256, 3, 2]
6 -1 2 788480 ultralytics.nn.modules.block.C2f [256, 256, 2, True]
7 -1 1 1180672 ultralytics.nn.modules.conv.Conv [256, 512, 3, 2]
8 -1 1 1838080 ultralytics.nn.modules.block.C2f [512, 512, 1, True]
9 -1 1 656896 ultralytics.nn.modules.block.SPPF [512, 512, 5]
10 -1 1 0 torch.nn.modules.upsampling.Upsample [None, 2, 'nearest']
11 [-1, 6] 1 0 ultralytics.nn.modules.conv.Concat [1]
12 -1 1 591360 ultralytics.nn.modules.block.C2f [768, 256, 1]
13 -1 1 0 torch.nn.modules.upsampling.Upsample [None, 2, 'nearest']
14 [-1, 4] 1 0 ultralytics.nn.modules.conv.Concat [1]
15 -1 1 148224 ultralytics.nn.modules.block.C2f [384, 128, 1]
16 -1 1 147712 ultralytics.nn.modules.conv.Conv [128, 128, 3, 2]
17 [-1, 12] 1 0 ultralytics.nn.modules.conv.Concat [1]
18 -1 1 493056 ultralytics.nn.modules.block.C2f [384, 256, 1]
19 -1 1 590336 ultralytics.nn.modules.conv.Conv [256, 256, 3, 2]
20 [-1, 9] 1 0 ultralytics.nn.modules.conv.Concat [1]
21 -1 1 1969152 ultralytics.nn.modules.block.C2f [768, 512, 1]
22 [15, 18, 21] 1 2118370 ultralytics.nn.modules.head.Detect [6, 16, None, [128, 256, 512]]
Model summary: 130 layers, 11,137,922 parameters, 11,137,906 gradients, 28.7 GFLOPs

Transferred 349/355 items from pretrained weights
Freezing layer 'model.22.dfl.conv.weight'
AMP: running Automatic Mixed Precision (AMP) checks...
AMP: checks passed
train: Fast image access (ping: 0.20.1 ms, read: 137.021.7 MB/s, size: 63.4 KB)
train: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\train\labels.cache... 10710 images, 31 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 10710/10710 0.0s
val: Fast image access (ping: 0.20.1 ms, read: 88.017.3 MB/s, size: 57.5 KB)
val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels.cache... 2616 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 2616/2616 0.0s
optimizer: 'optimizer=auto' found, ignoring 'lr0=0.01' and 'momentum=0.937' and determining best 'optimizer', 'lr0' and 'momentum' automatically...
optimizer: AdamW(lr=0.001, momentum=0.9) with parameter groups 57 weight(decay=0.0), 64 weight(decay=0.0005), 63 bias(decay=0.0)
Plotting labels to D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable\labels.jpg...
Image sizes 640 train, 640 val
Using 0 dataloader workers
Logging results to D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable
Starting training for 50 epochs...

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       1/50      1.94G      2.125      2.911      1.369         12        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 6:05
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.3it/s 37.9s
                   all       2616       5436      0.875      0.819      0.888      0.377

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       2/50      2.36G      1.826      1.232      1.212         24        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:28
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.3it/s 38.2s
                   all       2616       5436      0.805        0.9      0.811      0.378

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       3/50       2.4G      1.784      1.111      1.178         21        640: 100% ━━━━━━━━━━━━ 1339/1339 4.2it/s 5:19
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.5it/s 36.7s
                   all       2616       5436      0.933      0.896      0.938      0.454

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       4/50      2.44G      1.752      1.056      1.165         20        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:24
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.0it/s 41.3s
                   all       2616       5436       0.94      0.916      0.952      0.452

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       5/50      2.44G       1.71     0.9806      1.146         18        640: 100% ━━━━━━━━━━━━ 1339/1339 4.3it/s 5:14
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.3it/s 37.8s
                   all       2616       5436      0.948      0.948      0.966      0.472

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       6/50      2.44G      1.687     0.9358      1.137         12        640: 100% ━━━━━━━━━━━━ 1339/1339 4.2it/s 5:21
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.4it/s 37.6s
                   all       2616       5436      0.959      0.946      0.967      0.478

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       7/50      2.44G       1.67     0.8945      1.131         10        640: 100% ━━━━━━━━━━━━ 1339/1339 4.2it/s 5:21
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 39.1s
                   all       2616       5436      0.965      0.954      0.972      0.491

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       8/50      2.48G      1.648     0.8613      1.116         26        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:28
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.3it/s 38.6s
                   all       2616       5436      0.963      0.949      0.968      0.479

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
       9/50      2.48G      1.637      0.838      1.119         12        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:32
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.3it/s 37.8s
                   all       2616       5436      0.971      0.966      0.978      0.495

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      10/50      2.48G      1.625     0.8147       1.11         16        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:30
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 39.5s
                   all       2616       5436       0.97      0.967      0.977      0.506

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      11/50      2.48G      1.605     0.7966      1.104         12        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:31
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.1it/s 39.9s
                   all       2616       5436      0.974      0.968      0.979      0.501

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      12/50      2.48G      1.591     0.7786      1.098         20        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:32
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.4it/s 36.9s
                   all       2616       5436      0.969      0.964      0.979      0.502

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      13/50      2.48G      1.585     0.7757      1.094         14        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:25
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.6it/s 36.0s
                   all       2616       5436       0.97      0.974      0.981      0.513

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      14/50      2.48G      1.569     0.7591      1.092         12        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:25
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.8it/s 43.5s
                   all       2616       5436      0.972       0.97      0.981      0.515

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      15/50      2.48G      1.562     0.7422      1.087         17        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:24
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.4it/s 37.6s
                   all       2616       5436      0.976      0.975      0.982      0.518

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      16/50      2.48G      1.548     0.7342      1.085         18        640: 100% ━━━━━━━━━━━━ 1339/1339 3.6it/s 6:13
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.6it/s 45.9s
                   all       2616       5436      0.974      0.976      0.984      0.515

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      17/50      2.48G      1.538     0.7208      1.083         16        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 5:60
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.4it/s 37.7s
                   all       2616       5436      0.971      0.973      0.981      0.518

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      18/50      2.48G      1.527     0.7084      1.077         15        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:35
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.8it/s 43.4s
                   all       2616       5436      0.975      0.974      0.983       0.53

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      19/50      2.48G      1.517     0.6994      1.073         19        640: 100% ━━━━━━━━━━━━ 1339/1339 3.8it/s 5:56
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.9it/s 42.2s
                   all       2616       5436      0.972      0.976      0.982      0.524

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      20/50      2.48G      1.504     0.6885      1.064         15        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:34
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.0it/s 40.6s
                   all       2616       5436      0.969      0.979      0.983      0.527

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      21/50      2.52G      1.486     0.6779      1.063         27        640: 100% ━━━━━━━━━━━━ 1339/1339 3.9it/s 5:41
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.9it/s 41.8s
                   all       2616       5436      0.974      0.981      0.985      0.527

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      22/50      2.52G      1.479       0.67      1.057         16        640: 100% ━━━━━━━━━━━━ 1339/1339 4.3it/s 5:09
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.5it/s 36.1s
                   all       2616       5436      0.974      0.976      0.985      0.534

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      23/50      2.52G      1.463     0.6613      1.053         15        640: 100% ━━━━━━━━━━━━ 1339/1339 3.0it/s 7:24
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.1it/s 53.5s
                   all       2616       5436      0.976       0.98      0.985      0.534

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      24/50      2.52G      1.465     0.6571      1.055         21        640: 100% ━━━━━━━━━━━━ 1339/1339 2.8it/s 7:58
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.2it/s 51.8s
                   all       2616       5436      0.973      0.985      0.985       0.54

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      25/50      2.52G      1.449     0.6487      1.052         11        640: 100% ━━━━━━━━━━━━ 1339/1339 3.0it/s 7:34
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.1it/s 53.4s
                   all       2616       5436      0.973      0.981      0.985      0.537

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      26/50      2.52G      1.438     0.6397      1.047         25        640: 100% ━━━━━━━━━━━━ 1339/1339 2.7it/s 8:08
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 2.7it/s 1:00
                   all       2616       5436      0.971      0.984      0.984       0.54

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      27/50      2.52G       1.42     0.6312      1.042         15        640: 100% ━━━━━━━━━━━━ 1339/1339 2.8it/s 7:56
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.5it/s 47.4s
                   all       2616       5436      0.977      0.981      0.986      0.545

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      28/50      2.52G      1.408     0.6295       1.04         13        640: 100% ━━━━━━━━━━━━ 1339/1339 3.1it/s 7:08
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.2it/s 52.0s
                   all       2616       5436      0.974      0.985      0.987      0.538

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      29/50      2.52G      1.397     0.6256      1.037         16        640: 100% ━━━━━━━━━━━━ 1339/1339 3.1it/s 7:07
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.4it/s 48.1s
                   all       2616       5436      0.972      0.986      0.985      0.545

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      30/50      2.52G      1.387     0.6123      1.029         17        640: 100% ━━━━━━━━━━━━ 1339/1339 3.2it/s 6:57
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.3it/s 49.5s
                   all       2616       5436      0.975      0.982      0.987      0.546

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      31/50      2.52G      1.372     0.6046      1.027          9        640: 100% ━━━━━━━━━━━━ 1339/1339 3.1it/s 7:07
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.4it/s 49.0s
                   all       2616       5436      0.975      0.986      0.987       0.55

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      32/50      2.52G      1.354     0.6002      1.018         12        640: 100% ━━━━━━━━━━━━ 1339/1339 3.2it/s 7:02
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.8it/s 43.2s
                   all       2616       5436      0.975      0.985      0.987      0.551

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      33/50      2.52G      1.346     0.5909      1.018         19        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 5:59
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.4it/s 37.4s
                   all       2616       5436      0.976      0.986      0.987      0.557

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      34/50      2.52G      1.323      0.584      1.011         13        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:33
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.5it/s 36.2s
                   all       2616       5436      0.972      0.987      0.988      0.556

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      35/50      2.52G      1.327       0.58      1.011         16        640: 100% ━━━━━━━━━━━━ 1339/1339 4.3it/s 5:14
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.9it/s 42.5s
                   all       2616       5436      0.978      0.984      0.986      0.557

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      36/50      2.52G      1.304     0.5746      1.007         15        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 6:05
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.9it/s 42.3s
                   all       2616       5436      0.976      0.988      0.987      0.556

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      37/50      2.52G      1.296     0.5705          1         13        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 6:01
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.7it/s 44.7s
                   all       2616       5436      0.976      0.987      0.988      0.558

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      38/50      2.52G      1.286     0.5635     0.9995         13        640: 100% ━━━━━━━━━━━━ 1339/1339 3.9it/s 5:44
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.9it/s 42.1s
                   all       2616       5436      0.975      0.988      0.989       0.56

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      39/50      2.52G      1.274     0.5595     0.9971         20        640: 100% ━━━━━━━━━━━━ 1339/1339 4.0it/s 5:34
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 38.9s
                   all       2616       5436      0.977      0.986      0.988      0.565

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      40/50      2.52G       1.26     0.5555     0.9913         20        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 5:58
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.9it/s 42.0s
                   all       2616       5436      0.977      0.985      0.988      0.563

Closing dataloader mosaic

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      41/50      2.52G      1.237     0.5091      1.022         10        640: 100% ━━━━━━━━━━━━ 1339/1339 3.9it/s 5:41
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.2it/s 51.6s
                   all       2616       5436      0.979      0.984      0.988      0.563

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      42/50      2.52G      1.217     0.4975      1.013          9        640: 100% ━━━━━━━━━━━━ 1339/1339 4.2it/s 5:19
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.1it/s 40.1s
                   all       2616       5436      0.975      0.989      0.989      0.566

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      43/50      2.52G      1.197     0.4932      1.009         10        640: 100% ━━━━━━━━━━━━ 1339/1339 4.2it/s 5:17
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.0it/s 41.0s
                   all       2616       5436      0.976      0.988      0.988      0.566

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      44/50      2.52G      1.179     0.4878      1.001         13        640: 100% ━━━━━━━━━━━━ 1339/1339 4.5it/s 4:59
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 39.4s
                   all       2616       5436      0.976      0.988      0.989      0.568

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      45/50      2.52G      1.169     0.4835     0.9963         10        640: 100% ━━━━━━━━━━━━ 1339/1339 4.5it/s 4:58
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 39.0s
                   all       2616       5436      0.976      0.988      0.989      0.568

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      46/50      2.52G      1.156     0.4764     0.9938         10        640: 100% ━━━━━━━━━━━━ 1339/1339 4.1it/s 5:30
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.1it/s 40.0s
                   all       2616       5436      0.977      0.988      0.988      0.569

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      47/50      2.52G      1.146     0.4774     0.9904          9        640: 100% ━━━━━━━━━━━━ 1339/1339 4.4it/s 5:03
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 39.4s
                   all       2616       5436      0.977      0.987      0.989      0.572

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      48/50      2.52G      1.137     0.4741     0.9848          6        640: 100% ━━━━━━━━━━━━ 1339/1339 4.3it/s 5:08
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.2it/s 39.0s
                   all       2616       5436      0.978      0.987       0.99       0.57

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      49/50      2.52G      1.126     0.4674     0.9843         11        640: 100% ━━━━━━━━━━━━ 1339/1339 5.0it/s 4:26
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 4.8it/s 34.0s
                   all       2616       5436      0.977      0.987       0.99      0.572

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      50/50      2.52G      1.116     0.4657     0.9764         13        640: 100% ━━━━━━━━━━━━ 1339/1339 3.7it/s 5:59
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 164/164 2.9it/s 56.1s
                   all       2616       5436      0.978      0.986       0.99      0.572

50 epochs completed in 5.516 hours.
Optimizer stripped from D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable\weights\last.pt, 22.5MB
Optimizer stripped from D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable\weights\best.pt, 22.5MB

Validating D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable\weights\best.pt...
Ultralytics 8.4.75 Python-3.10.20 torch-2.6.0+cu124 CUDA:0 (NVIDIA GeForce RTX 4060 Laptop GPU, 8188MiB)
Model summary (fused): 73 layers, 11,127,906 parameters, 0 gradients, 28.4 GFLOPs
Class Images Instances Box(P R mAP50 mAP50-95): 100% ━━━━━━━━━━━━ 164/164 3.2it/s 51.0s
all 2616 5436 0.978 0.986 0.99 0.572
missing_hole 450 929 0.98 0.996 0.993 0.621
mouse_bite 456 908 0.974 0.996 0.989 0.57
open_circuit 395 821 0.984 0.981 0.991 0.53
short 375 786 0.973 0.971 0.987 0.582
spur 482 1011 0.984 0.981 0.992 0.567
spurious_copper 458 981 0.975 0.992 0.99 0.561
Speed: 0.3ms preprocess, 3.8ms inference, 0.0ms loss, 1.8ms postprocess per image
Results saved to D:\Workspace\pcb-defect-detector\runs\detect\pcb_yolov8s_stable

## 模型验证

(pcb-yolo) D:\Workspace\pcb-defect-detector>python -c "from ultralytics import YOLO; model = YOLO(r'runs\detect\pcb_yolov8s_stable\weights\best.pt'); results = model.val(data=r'data\PCB Defects.v6i.yolov8\data.yaml')"
Ultralytics 8.4.75 Python-3.10.20 torch-2.6.0+cu124 CUDA:0 (NVIDIA GeForce RTX 4060 Laptop GPU, 8188MiB)
Model summary (fused): 73 layers, 11,127,906 parameters, 0 gradients, 28.4 GFLOPs
val: Fast image access (ping: 0.20.1 ms, read: 132.830.8 MB/s, size: 60.7 KB)
val: Scanning D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\valid\labels.cache... 2616 images, 0 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 2616/2616 0.0s
Class Images Instances Box(P R mAP50 mAP50-95): 100% ━━━━━━━━━━━━ 164/164 5.5it/s 29.9s
all 2616 5436 0.977 0.987 0.99 0.573
missing_hole 450 929 0.979 0.996 0.993 0.624
mouse_bite 456 908 0.972 0.996 0.989 0.57
open_circuit 395 821 0.984 0.981 0.991 0.532
short 375 786 0.973 0.973 0.987 0.583
spur 482 1011 0.981 0.981 0.991 0.568
spurious_copper 458 981 0.974 0.993 0.99 0.562
Speed: 1.1ms preprocess, 6.7ms inference, 0.0ms loss, 0.9ms postprocess per image
Results saved to D:\Workspace\pcb-defect-detector\runs\detect\val
