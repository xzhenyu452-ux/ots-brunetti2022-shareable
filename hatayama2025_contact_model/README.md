# Hatayama 2025 肖特基接触 OTS 准静态复现

这个独立子项目复现 Hatayama 等人在 GeTe6/Hf、W、Pt 器件中提出的接触解释：电极功函数改变界面带弯曲和耗尽层，从而移动冲击电离起点与阈值电压。

## 运行

```powershell
python -m pip install -e .
python scripts/reproduce_contact_model.py
python -m pytest -q
```

生成结果位于 `outputs/`：

- `electrode_comparison.png`：三种电极的 I-V、倍增因子和电压分配；
- `thickness_comparison.png`：100/50/25 nm 的耗尽层重叠趋势；
- `electrode_sweeps.csv`：完整扫描数据；
- `summary.json`：参数、阈值和厚度结果。

## 模型边界

论文明确给出的耗尽近似、Poole-Frenkel 和冲击电离公式被直接实现。论文没有给出闭合的 ON 态方程，也没有完整列出 PF/冲击电离的全部前因子，因此本复现增加了带电流限幅的工程 ON 分支，并把所有补充参数标为“基准标定参数”。它适合验证电极和厚度趋势，不应被当作论文原始数据的逐点拟合。

完整公式、参数来源和限制见 [MODEL.md](MODEL.md)。
