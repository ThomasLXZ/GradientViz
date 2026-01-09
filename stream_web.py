import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="GradientViz", page_icon="📈", layout="wide")

st.title("🎯 Gradient & Steepest Ascent Visualization")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Settings")
    
    func_type = st.selectbox(
        "Function Type",
        ["Paraboloid (x² + y²)", "Saddle (x² - y²)", "Wave Surface", "Gaussian"]
    )
    
    px = st.slider("X Coordinate", -4.0, 4.0, 1.5, step=0.1)
    py = st.slider("Y Coordinate", -4.0, 4.0, 1.5, step=0.1)
    arrow_scale = st.slider("Gradient Arrow Scale", 0.1, 1.0, 0.4, step=0.05)

# --- Function Definitions ---
if func_type == "Paraboloid (x² + y²)":
    def f(x, y): return x**2 + y**2
    def grad(x, y): return (2*x, 2*y)
elif func_type == "Saddle (x² - y²)":
    def f(x, y): return x**2 - y**2
    def grad(x, y): return (2*x, -2*y)
elif func_type == "Wave Surface":
    def f(x, y): return np.sin(x) + np.cos(y)
    def grad(x, y): return (np.cos(x), -np.sin(y))
else:  # Gaussian
    def f(x, y): return np.exp(-(x**2 + y**2) / 4)
    def grad(x, y): return (-x/2 * np.exp(-(x**2 + y**2)/4), -y/2 * np.exp(-(x**2 + y**2)/4))

# --- Grid Data ---
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# --- Compute Gradient ---
grad_x, grad_y = grad(px, py)
pz = f(px, py)

# --- Info Display ---
col1, col2, col3 = st.columns(3)
col1.metric("Current Point", f"({px:.1f}, {py:.1f})")
col2.metric("Function Value", f"{pz:.3f}")
col3.metric("Gradient", f"({grad_x:.2f}, {grad_y:.2f})")

st.divider()

# --- Charts ---
chart_col1, chart_col2 = st.columns(2)

# 3D Surface Plot
with chart_col1:
    st.subheader("3D Surface Plot")
    
    fig3d = go.Figure()
    fig3d.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', opacity=0.9, showscale=False))
    fig3d.add_trace(go.Scatter3d(x=[px], y=[py], z=[pz], mode='markers', marker=dict(size=10, color='red')))
    
    fig3d.update_layout(
        scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'),
        margin=dict(l=0, r=0, t=10, b=0),
        height=450
    )
    st.plotly_chart(fig3d, use_container_width=True)

# Contour Plot
with chart_col2:
    st.subheader("Contour Plot + Gradient Arrow")
    
    fig_contour = go.Figure()
    fig_contour.add_trace(go.Contour(x=x, y=y, z=Z, colorscale='Viridis', showscale=False))
    fig_contour.add_trace(go.Scatter(x=[px], y=[py], mode='markers', marker=dict(size=15, color='red')))
    
    # Gradient arrow
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

# X/Y Slice Plots
st.subheader("X/Y Direction Slices")
slice_col1, slice_col2 = st.columns(2)

# X-direction slice (fixed y)
with slice_col1:
    z_x = f(x, py)
    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(x=x, y=z_x, mode='lines', line=dict(color='#667eea', width=3)))
    fig_x.add_trace(go.Scatter(x=[px], y=[pz], mode='markers', marker=dict(size=12, color='red')))
    
    # Tangent line
    t_x = np.array([px - 1.5, px + 1.5])
    t_z = pz + grad_x * (t_x - px)
    fig_x.add_trace(go.Scatter(x=t_x, y=t_z, mode='lines', line=dict(color='red', width=2, dash='dash')))
    
    fig_x.update_layout(title=f"X-Slice (y={py:.1f}), Slope={grad_x:.2f}", height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_x, use_container_width=True)

# Y-direction slice (fixed x)
with slice_col2:
    z_y = f(px, y)
    fig_y = go.Figure()
    fig_y.add_trace(go.Scatter(x=y, y=z_y, mode='lines', line=dict(color='#764ba2', width=3)))
    fig_y.add_trace(go.Scatter(x=[py], y=[pz], mode='markers', marker=dict(size=12, color='red')))
    
    # Tangent line
    t_y = np.array([py - 1.5, py + 1.5])
    t_z_y = pz + grad_y * (t_y - py)
    fig_y.add_trace(go.Scatter(x=t_y, y=t_z_y, mode='lines', line=dict(color='red', width=2, dash='dash')))
    
    fig_y.update_layout(title=f"Y-Slice (x={px:.1f}), Slope={grad_y:.2f}", height=300, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_y, use_container_width=True)
