import time
import torch
from ultralytics import YOLO

def benchmark(label, model, n=300):
    """测推理速度，用真实图片路径避免归一化问题"""
    test_img = r"data\PCB Defects.v6i.yolov8\valid\images"  # 验证集目录
    import os
    files = [os.path.join(test_img, f) for f in os.listdir(test_img) if f.endswith(('.jpg','.png'))]
    if not files:
        print(f"{label}: 没有测试图片，跳过")
        return None, None

    img = files[0]

    # 预热
    for _ in range(30):
        model(img, verbose=False)

    # 正式计时（跑 N 次取平均）
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(n):
        model(img, verbose=False)
    torch.cuda.synchronize()
    t1 = time.time()

    avg_ms = (t1 - t0) / n * 1000
    fps = n / (t1 - t0)
    print(f"{label:25s}: {avg_ms:6.1f}ms  {fps:6.0f}FPS")
    return avg_ms, fps

if __name__ == "__main__":
    print("=== Benchmark 开始 ===\n")

    # 1. PyTorch 基线
    model_pt = YOLO(r"runs\detect\pcb_yolov8s_stable\weights\best.pt")
    pt_ms, pt_fps = benchmark("PyTorch FP32", model_pt)

    # 2. ONNX Runtime GPU
    import os
    onnx_path = r"weights\best.onnx"
    if os.path.exists(onnx_path):
        model_onnx = YOLO(onnx_path, task="detect")
        onnx_ms, onnx_fps = benchmark("ONNX Runtime GPU", model_onnx)
    else:
        print("ONNX 未导出，先跑 yolo export")

    # 3. TensorRT（可选）
    trt_path = r"weights\best_fp16.engine"
    if os.path.exists(trt_path):
        model_trt = YOLO(trt_path, task="detect")
        trt_ms, trt_fps = benchmark("TensorRT FP16", model_trt)
    else:
        print("TensorRT 未安装/未导出，跳过。")

    # 4. 汇总表
    print("\n=== Benchmark 汇总 ===")
    print(f"{'引擎':25s} {'延迟':>8s} {'FPS':>8s}")
    print("-" * 43)
    if pt_ms: print(f"{'PyTorch FP32':25s} {pt_ms:8.1f}ms {pt_fps:8.0f}")
    if 'onnx_ms' in dir() and onnx_ms: print(f"{'ONNX Runtime GPU':25s} {onnx_ms:8.1f}ms {onnx_fps:8.0f}")
    if 'trt_ms' in dir() and trt_ms: print(f"{'TensorRT FP16':25s} {trt_ms:8.1f}ms {trt_fps:8.0f}")