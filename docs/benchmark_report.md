# Benchmark Report

## 测试环境

- GPU: NVIDIA RTX 4060 Laptop (8GB)
- CUDA: 12.4
- PyTorch: 2.6.0+cu124
- ONNX Runtime: 1.23.2 (CUDAExecutionProvider)

## 测试方法

- 预热 30 次，正式测试 300 次取均值
- 使用验证集真实图片（避免随机 tensor 的归一化偏差）
- 端到端延迟：含文件 I/O + 预处理 + 推理 + 后处理

## 结果

|       引擎       |  延迟  | FPS |  加速比  | 体积 |
| :--------------: | :----: | :-: | :------: | :--: |
|   PyTorch FP32   | 15.3ms | 65  |   1.0×   | 22MB |
| ONNX Runtime GPU | 14.0ms | 71  |   1.1×   | 22MB |
|  TensorRT FP16   | 待测试 |  —  | 预期 3×+ | ~6MB |

## 分析

ONNX Runtime 仅提升 1.1×，原因：

- YOLOv8s 推理时间（~7ms）接近数据在 CPU/GPU 间拷贝的时间
- 加速效果随模型变大更明显（v8l/m 预期 2×+）
- 生产环境推荐 Linux + TensorRT FP16，预期 3×+
