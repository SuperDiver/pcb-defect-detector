from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolov8s.pt")

    results = model.train(
        # ===== 数据 =====
        data=r"D:\Workspace\pcb-defect-detector\data\PCB Defects.v6i.yolov8\data.yaml",

        # ===== 训练规模 =====
        epochs=50,
        imgsz=640,

        # ===== GPU设置 =====
        device=0,          # ⭐比 "cuda:0" 更稳定
        amp=True,          # ⭐必须（显存优化 + 加速）

        # ===== batch（4060关键优化）=====
        batch=8,           # ⭐建议 8（16容易爆/不稳定）

        # ===== 学习率 =====
        lr0=0.01,
        lrf=0.01,

        # ===== 优化器 =====
        optimizer="auto",

        # ===== 稳定性关键参数 =====
        workers=0,         # ⭐⭐⭐⭐⭐ Windows必加
        cache=False,       # ⭐避免 shared memory 崩溃
        deterministic=True,# ⭐减少随机CUDA错误（略降速但稳定）

        # ===== 训练控制 =====
        patience=15,
        pretrained=True,

        # ===== 保存与日志 =====
        save=True,
        save_period=10,
        plots=True,
        verbose=True,

        # ===== 命名 =====
        name="pcb_yolov8s_stable",
    )