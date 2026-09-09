# Brunetti 2022 双能级电子 OTS 模型说明

## 1. 目标与范围

本包用于复现 OTS（Ovonic Threshold Switch）的基础阈值开关、保持和动态延迟现象。实现采用 Brunetti 等人 2022 年模型的**零维（0-D）动态缩减**：把器件看成均匀有源层，用两个电子能级描述载流子占据，并用一个有效电子温度描述载流子能量弛豫。

它不是论文中包含空间分辨 Poisson 方程、能量通量和边界条件的完整 PDE 求解器。因此，本文档把“论文直接给出的关系”和“为了得到可运行零维模型而加入的闭合”分开标注。

## 2. 文献来源

主要来源是 Brunetti et al., *A compact model for the dynamics of ovonic threshold switches*, Frontiers in Physics 10, 854393 (2022), DOI [10.3389/fphy.2022.854393](https://doi.org/10.3389/fphy.2022.854393)，其开放全文和 Table 1 给出了双能级动态模型及基准参数。

模型思想沿袭 Ielmini, *Threshold switching and voltage snapback in chalcogenide glasses*, Phys. Rev. B 78, 035308 (2008)，DOI [10.1103/PhysRevB.78.035308](https://doi.org/10.1103/PhysRevB.78.035308)，并与 Piccinini et al., *A complete and consistent model of threshold switching in chalcogenide glasses*, J. Appl. Phys. 112, 083722 (2012)，DOI [10.1063/1.4761997](https://doi.org/10.1063/1.4761997) 的场增强、载流子输运和自洽建模路线相联系。

## 3. 变量与基本关系

设有源层厚度为 `L`，面积为 `A`，局部平均电场为 `F`，电子有效温度为 `Te`，高能级移动载流子分数为 `x=nB/n0`。

双能级能量差为

\[
\Delta E=E_B-E_T.
\]

场辅助势垒降低采用

\[
\Delta E_{\rm eff}(F)=\Delta E-\gamma |F|/q,
\]

其中 `gamma` 的单位为 C·m，故 `gamma F/q` 是 eV/J 一致的能量量纲（代码内部使用 SI J）。平衡移动载流子分数写成

\[
x_{\rm eq}(F,T_e)=\frac{1}{1+\Gamma\exp\left[\frac{\Delta E_{\rm eff}(F)}{k_B T_e}\right]},
\]

其中 \(\Gamma=g_T/g_B\) 是简并度比。

漂移电流为

\[
I=q\mu n_0 x F A,
\qquad G(x)=\frac{q\mu n_0 A}{L}x.
\]

## 4. 外部电路与串联电阻

外加电压通过串联电阻 `Rs` 驱动器件：

\[
V_{\rm src}=V_{\rm OTS}+I R_s.
\]

由于 \(I=G(x)V_{\rm OTS}\)，在每个时间步可直接得到

\[
V_{\rm OTS}=\frac{V_{\rm src}}{1+G(x)R_s},
\qquad F=V_{\rm OTS}/L.
\]

这一步是有限串联电阻下电压扫描能够出现稳定 ON 态和滞回的关键。`Rs=0` 时是理想电压源，内禀曲线可能在阈值后出现没有有限稳定解的区域。

## 5. 动态方程

### 5.1 移动载流子分数

\[
\frac{dx}{dt}=\frac{x_{\rm eq}(F,T_e)-x}{\tau_n}.
\]

`tau_n` 决定高能级移动载流子占据向场/温度决定的平衡值靠拢的时间尺度。

### 5.2 载流子能量弛豫

零维能量状态采用

\[
\frac{dT_e}{dt}=\frac{T_{e,\rm eq}(F,x)-T_e}{\tau_T},
\]

并令

\[
T_{e,\rm eq}=T_0+\eta_E\frac{2}{3}\frac{q\mu F^2\tau_T}{k_B}x.
\]

这里 \(\tau_T\) 是电子能量弛豫时间，\(\eta_E\) 是本零维实现的无量纲能量闭合/标定因子。论文的完整模型通过能量输运方程求解该部分，Table 1 没有一个可直接对应 `eta_E` 的独立参数；因此 `eta_E=0.60` 必须视为**本缩减模型的附加拟合参数**，不能冒充论文原始参数。

## 6. 正反馈与阈值/保持

模型中的电子学正反馈链为：

\[
F\uparrow \Rightarrow \Delta E_{\rm eff}\downarrow
\Rightarrow x_{\rm eq}\uparrow \Rightarrow I\uparrow
\Rightarrow T_e\uparrow \Rightarrow x_{\rm eq}\text{进一步增大}.
\]

上扫时，反馈超过载流子弛豫和电路负载的稳定性边界，定义为阈值点 `Vth`。下扫时，ON 态只有在反馈仍能维持、且 \(x\) 尚未衰减到 OFF 分支前才存在；失稳点定义为保持点 `Vhold`。因此 `Vth` 和 `Vhold` 不是两个完全独立输入，而是由 `DeltaE`、`Gamma`、`gamma`、`mu`、`n0`、`tau_n`、`tau_T`、`eta_E`、`L`、`A`、`Rs`、扫描速率及初始状态共同决定。

## 7. 基准参数

| 参数 | 数值 | 状态 | 备注 |
|---|---:|---|---|
| `ET` | 0 eV | 论文 Table 1 | 低能级参考能量 |
| `EB` | 0.35 eV | 论文 Table 1 | 高能级能量 |
| `Gamma` | 2.5e-3 | 论文 Table 1 | 简并度比 |
| `gamma` | 3.36e-28 C·m | 论文 Table 1 | 场辅助系数 |
| `epsilon_r` | 15 | 论文 Table 1 | 0-D 代码未显式求 Poisson |
| `mu` | 5.9e-4 m²·V⁻¹·s⁻¹ | 论文 Table 1 | 迁移率 |
| `n0` | 6.8e25 m⁻³ | 论文 Table 1 | 总可参与载流子浓度 |
| `tau_T` | 1.5e-13 s | 论文 Table 1 | 能量弛豫时间 |
| `tau_n` | 0.6e-9 s | 论文 Table 1 | 载流子占据弛豫时间 |
| `L` | 53 nm | 论文 Table 1 | 有源层厚度 |
| `A` | 5000 nm² | 论文模型假设 | 有效面积 |
| `T0` | 298 K | 论文 Table 1 | 晶格/环境温度 |
| `eta_E` | 0.60 | 本缩减模型附加闭合 | 需按器件/数据重新标定 |
| `Rs` | 50 Ω（示例） | 仿真工况 | 外部串联电阻 |

## 8. 数值实现与输出定义

代码位于 `src/ots_brunetti2022/brunetti2022.py`，使用 `scipy.integrate.solve_ivp` 积分两个状态变量。三角电压扫描由 `scripts/reproduce_brunetti2022.py` 完成。

- `Vth`：上扫电压中首次满足电流相对 OFF 基线显著跃迁的点。
- `Vhold`：下扫中电流从 ON 分支跌回 OFF 分支的点。
- 动态延迟：阶跃响应达到最终电流 50% 的时间。

以当前基准参数、`Rs=50 Ω`、3 V 三角扫描为例，约得到 `Vth=2.50 V`、`Vhold=1.58 V`；2.4 V 阶跃的半电流建立延迟约 `4.58 ns`。这些是复现基准，不是对所有 OTS 器件的普适常数。

## 9. 依赖与运行

运行时依赖：Python 3.11+、NumPy、SciPy、Matplotlib；测试依赖 pytest。版本下限写在 `pyproject.toml` 和 `requirements.txt`。

```powershell
python -m pip install -e .
python scripts/reproduce_brunetti2022.py
python -m pytest -q
```

结果写入 `outputs/brunetti2022_dynamic/`：

- `triangle_iv_Rs50ohm.png`：三角电压扫描 I–V 和阈值/保持标记；
- `step_response_2p4V.png`：阶跃响应；
- `summary.json`：提取出的数值摘要。

## 10. 复现边界

若要用于具体材料拟合，应进一步引入空间坐标、Poisson 自洽场、接触注入、能量通量、温度依赖迁移率和器件几何校准。尤其不要把 `eta_E` 当作论文直接测得的材料常数；它只是让零维模型保留电子学正反馈和纳秒级动态尺度的工程闭合。
