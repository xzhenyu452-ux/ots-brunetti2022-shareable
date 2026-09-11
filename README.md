# Brunetti 2022 动态 OTS 模型（可分享复现包）

这是一个独立、可复制的 Python 仿真包，用于复现基于 Brunetti 等人 2022 双能级电子模型的准静态/瞬态 OTS 基础现象。

## 快速开始

```powershell
python -m pip install -e .
python scripts/reproduce_brunetti2022.py
python -m pytest -q
```

运行脚本会在 `outputs/brunetti2022_dynamic/` 生成阶跃响应、50 Ω 串联电阻三角扫描 I–V 图和 `summary.json`。

## 从哪里开始

- [MODEL.md](MODEL.md)：公式、参数、来源、假设和拟合注意事项。
- [src/ots_brunetti2022/brunetti2022.py](src/ots_brunetti2022/brunetti2022.py)：模型实现。
- [scripts/reproduce_brunetti2022.py](scripts/reproduce_brunetti2022.py)：一键复现脚本。
- [scripts/compare_activation_energy.py](scripts/compare_activation_energy.py)：固定其他参数、比较不同激活能的 I–V 曲线。
- [tests/test_brunetti2022.py](tests/test_brunetti2022.py)：自动化检查。
- [outputs/brunetti2022_dynamic/triangle_iv_Rs50ohm.png](outputs/brunetti2022_dynamic/triangle_iv_Rs50ohm.png)：示例电压扫描曲线。
- [outputs/brunetti2022_dynamic/activation_energy_comparison.png](outputs/brunetti2022_dynamic/activation_energy_comparison.png)：激活能对比图。

## 模型边界

代码是论文双能级模型的零维工程化缩减版：保留场辅助势垒降低、移动载流子分数、载流子能量弛豫和串联电阻；没有实现论文中的完整空间分辨 Poisson、能量通量和电极边界求解。`eta_E` 是为零维能量闭合加入的标定参数，论文表格没有直接给出，文档中已单独标注。

## 参考结果

当前基准参数、`Rs=50 Ω`、3 V 三角扫描得到约 `Vth=2.50 V`、`Vhold=1.58 V`；2.4 V 阶跃的半电流建立延迟约 `4.58 ns`。这些数值是该缩减模型的复现基准，不应直接视为某一具体器件的唯一材料常数。

## 工程说明

本目录是独立分享副本；不依赖上级项目路径。依赖见 `pyproject.toml` 和 `requirements.txt`，项目约束和变更记录见 `AGENTS.md`、`docs/`。
