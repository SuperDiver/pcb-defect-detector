import gradio as gr
from ultralytics import YOLO
import cv2
import numpy as np
import os

# 加载模型
model = YOLO(r"runs\detect\pcb_yolov8s_stable\weights\best.pt")
CLASS_NAMES = ['missing_hole', 'mouse_bite', 'open_circuit', 'short', 'spur', 'spurious_copper']

def detect_pcb(image):
    if image is None:
        return None, "请上传图片"
    results = model(image, verbose=False)[0]
    boxes = results.boxes
    annotated = results.plot()

    detections = []
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()
            detections.append([
                CLASS_NAMES[cls_id],
                f"{conf:.3f}",
                f"({xyxy[0]:.0f}, {xyxy[1]:.0f}, {xyxy[2]:.0f}, {xyxy[3]:.0f})"
            ])
    if not detections:
        return annotated, "未检测到缺陷"
    return annotated, detections

# 准备所有可用的示例图片
example_dir = r"data\sample_results"
example_files = []
if os.path.exists(example_dir):
    for f in sorted(os.listdir(example_dir)):
        if f.endswith(('.jpg', '.png', '.jpeg')):
            example_files.append(os.path.join(example_dir, f))

# 如果 sample_results 里没有图，fallback 到验证集
if not example_files:
    val_dir = r"data\PCB Defects.v6i.yolov8\valid\images"
    if os.path.exists(val_dir):
        for f in sorted(os.listdir(val_dir))[:6]:
            if f.endswith(('.jpg', '.png')):
                example_files.append(os.path.join(val_dir, f))

examples_list = [[f] for f in example_files[:6]]  # 最多 6 个示例

with gr.Blocks(title="PCB Defect Detector", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧩 PCB Defect Detector")
    gr.Markdown("上传 PCB 图片，YOLOv8 自动检测 6 类板面缺陷。")

    with gr.Row():
        with gr.Column(scale=1):
            input_img = gr.Image(label="上传 PCB 图片", type="numpy")
            detect_btn = gr.Button("🚀 开始检测", variant="primary", size="lg")

        with gr.Column(scale=1):
            output_img = gr.Image(label="检测结果", type="numpy")

    with gr.Row():
        output_table = gr.Dataframe(
            headers=["缺陷类别", "置信度", "位置 (x1,y1,x2,y2)"],
            label="检测详情",
            col_count=(3, "fixed")
        )

    # 示例图片：点击后自动加载到 input_img 并自动推理
    gr.Markdown("---\n### 📂 点击示例图片快速体验")
    gr.Examples(
        examples=examples_list,
        inputs=input_img,
        outputs=[output_img, output_table],
        fn=detect_pcb,
        label="点击加载并自动检测",
        cache_examples=False,
    )

    detect_btn.click(fn=detect_pcb, inputs=input_img, outputs=[output_img, output_table])

demo.launch(share=True)