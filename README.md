# LazySOC

SoC 寄存器生成工具 - 从 YAML 定义生成 SystemVerilog 和 C 代码。

## 安装

```bash
uv sync
```

## 使用

```bash
# 生成代码
lazysoc generate sample.yaml -o output/

# 验证定义文件
lazysoc validate sample.yaml
```
