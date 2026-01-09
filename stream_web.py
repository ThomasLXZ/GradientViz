import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 页面配置 ---
st.set_page_config(page_title="梯度可视化", page_icon="📈", layout="wide")

st.title("🎯 梯度与最速上升方向可视化")

# --- 侧边栏 ---
with st.sidebar:
    st.header("⚙️ 参数设置")
    
    func_type = st.selectbox(
        "函数类型",
        ["抛物面 (x² + y²)", "马鞍面 (x² - y²)", "波浪面", "高斯曲面"]
    )
    
    px = st.slider("X 坐标", -4.0, 4.0, 1.5, step=0.1)
    py = st.slider("Y 坐标", -4.0, 4.0, 1.5, step=0.1)
    arrow_scale = st.slider("梯度箭头缩放", 0.1, 1.0, 0.4, step=0.05)

# --- 函数定义 ---
if func_type == "抛物面 (x² + y²)":
    def f(x, y): return x**2 + y**2
    def grad(x, y): return (2*x, 2*y)
elif func_type == "马鞍面 (x² - y²)":
    def f(x, y): return x**2 - y**2
    def grad(x, y): return (2*x, -2*y)
elif func_type == "波浪面":
    def f(x, y): return np.sin(x) + np.cos(y)
    def grad(x, y): return (np.cos(x), -np.sin(y))
else:
    def f(x, y): return np.exp(-(x**2 + y**2) / 4)
    def grad(x, y): return (-x/2 * np.exp(-(x**2 + y**2)/4), -y/2 * np.exp(-(x**2 + y**2)/4))

# --- 网格数据 ---
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# --- 计算梯度 ---
grad_x, grad_y = grad(px, py)
pz = f(px, py)

# --- 信息显示 ---
col1, col2, col3 = st.columns(3)
col1.metric("当前点", f"({px:.1f}, {py:.1f})")
col2.metric("函数值", f"{pz:.3f}")
col3.metric("梯度", f"({grad_x:.2f}, {grad_y:.2f})")

st.divider()

# --- 图表 ---
chart_col1, chart_col2 = st.columns(2)

# 3D 曲面图
with chart_col1:
    st.subheader("3D 曲面图")
    
    fig3d = go.Figure()
    fig3d.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', opacity=0.9, showscale=False))
    fig3d.add_trace(go.Scatter3d(x=[px], y=[py], z=[pz], mode='markers', marker=dict(size=10, color='red')))
    
    fig3d.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        margin=dict(l=0, r=0, t=10, b=0),
        height=450
    )
    st.plotly_chart(fig3d, use_container_width=True)

# 等高线图
with chart_col2:
    st.subheader("等高线图 + 梯度箭头")
    
    fig_contour = go.Figure()
    fig_contour.add_trace(go.Contour(x=x, y=y, z=Z, colorscale='Viridis', showscale=False))
    fig_contour.add_trace(go.Scatter(x=[px], y=[py], mode='markers', marker=dict(size=15, color='red')))
    
    # 梯度箭头
    fig_contour.add_annotation(
        x=px + grad_x * arrow_scale, y=py + grad_y * arrow_scale,
        ax=px, ay=py,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=2, arrowwidth=3, arrowcolor="red"
    )
    
    fig_contour.update_layout(
        xaxis_title='X', yaxis_title='Y',
        margin=dict(l=0, r=0, t=10, b=0),
        height=450
    )
    st.plotly_chart(fig_contour, use_container_width=True)

st.divider()

# X/Y 切片图
st.subheader("X/Y 方向切片")
slice_col1, slice_col2 = st.columns(2)

with slice_col1:
    z_x = f(x, py)
    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(x=x, y=z_x, mode='lines', line=dict(color='#667eea', width=3)))
    fig_x.add_trace(go.Scatter(x=[px], y=[pz], mode='markers', marker=dict(size=12, color='red')))
    
    # 切线
    t_x = np.array([px - 1.5, px + 1.5])
    t_z = pz + grad_x * (t_x - px)
    fig_x.add_trace(go.Scatter(x=t_x, y=t_z, mode='lines', line=dict(color='red', width=2, dash='dash')))
    
    fig_x.update_layout(title=f"X切片 (y={py:.1f}), 斜率={grad_x:.2f}", height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_x, use_container_width=True)

with slice_col2:
    z_y = f(px, y)
    fig_y = go.Figure()
    fig_y.add_trace(go.Scatter(x=y, y=z_y, mode='lines', line=dict(color='#764ba2', width=3)))
    fig_y.add_trace(go.Scatter(x=[py], y=[pz], mode='markers', marker=dict(size=12, color='red')))
    
    # 切线
    t_y = np.array([py - 1.5, py + 1.5])
    t_z_y = pz + grad_y * (t_y - py)
    fig_y.add_trace(go.Scatter(x=t_y, y=t_z_y, mode='lines', line=dict(color='red', width=2, dash='dash')))
    
    fig_y.update_layout(title=f"Y切片 (x={px:.1f}), 斜率={grad_y:.2f}", height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_y, use_container_width=True)
