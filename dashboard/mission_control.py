import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(interval=2000, key="refresh")
except Exception:
    pass

DATA_FILE = Path("datasets/synthetic/live_uao_events.csv")

st.set_page_config(page_title="SentinelAI Mission Control", layout="wide")

st.title("🛡️ SentinelAI Mission Control")
st.caption("Autonomous Multi-Sensor Counter-UAO Defense System")

if not DATA_FILE.exists():
    st.error("No UAO data detected. Start the simulator first.")
    st.code("python3 simulator/uav_simulator.py")
    st.stop()

df = pd.read_csv(DATA_FILE)

latest = df.sort_values("timestamp").groupby("drone_id").tail(1)

colors = {
    "high": "red",
    "medium": "orange",
    "low": "yellow",
    "friendly": "cyan",
    "shot_down": "black",
}

fig = go.Figure()

# Battlefield boundary
fig.add_shape(
    type="rect",
    x0=0,
    y0=0,
    x1=1000,
    y1=1000,
    line=dict(color="white", width=2),
)

# Defense rings
rings = [
    (70, "red", "solid"),
    (180, "orange", "dash"),
    (320, "cyan", "dot"),
]

for radius, color, dash in rings:
    fig.add_shape(
        type="circle",
        x0=500 - radius,
        y0=500 - radius,
        x1=500 + radius,
        y1=500 + radius,
        line=dict(color=color, dash=dash, width=2),
    )

# FOB
fig.add_trace(
    go.Scatter(
        x=[500],
        y=[500],
        mode="markers+text",
        marker=dict(size=36, color="lime", symbol="square"),
        text=["FOB"],
        textposition="top center",
        name="FOB",
    )
)

# Sensor towers
sensors = [
    ("RADAR", 150, 850),
    ("RF", 850, 850),
    ("EO/IR", 150, 150),
    ("ACOUSTIC", 850, 150),
]

for name, x, y in sensors:
    fig.add_trace(
        go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(size=24, color="white", symbol="diamond"),
            text=[name],
            textposition="top center",
            name=name,
        )
    )

    fig.add_shape(
        type="circle",
        x0=x - 180,
        y0=y - 180,
        x1=x + 180,
        y1=y + 180,
        line=dict(color="gray", dash="dot", width=1),
    )

# Flight trails
for uao_id, group in df.groupby("drone_id"):
    recent = group.sort_values("timestamp").tail(8)

    fig.add_trace(
        go.Scatter(
            x=recent["x_position_m"],
            y=recent["y_position_m"],
            mode="lines",
            line=dict(color="gray", width=1),
            showlegend=False,
            hoverinfo="skip",
        )
    )

# UAOs
for _, row in latest.iterrows():
    is_down = row["status"] == "shot_down"

    color = "black" if is_down else colors.get(row["threat_level"], "white")
    symbol = "x" if is_down else "triangle-up"
    label = f"{row['drone_id']} DOWN" if is_down else row["drone_id"]

    if not is_down:
        fig.add_trace(
            go.Scatter(
                x=[row["x_position_m"], row["predicted_x_m"]],
                y=[row["y_position_m"], row["predicted_y_m"]],
                mode="lines",
                line=dict(color=color, width=2, dash="dash"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[row["x_position_m"]],
            y=[row["y_position_m"]],
            mode="markers+text",
            marker=dict(
                size=24 if is_down else 19,
                color=color,
                symbol=symbol,
                line=dict(color="white", width=1),
            ),
            text=[label],
            textposition="top center",
            hovertemplate=(
                f"<b>{row['drone_id']}</b><br>"
                f"Type: {row['drone_type']}<br>"
                f"Mission: {row['mission']}<br>"
                f"Status: {row['status']}<br>"
                f"Threat: {row['threat_level']}<br>"
                f"Score: {row['threat_score']}<br>"
                f"Distance to FOB: {row['distance_to_fob_m']} m<br>"
                f"Countermeasure: {row['countermeasure']}"
                "<extra></extra>"
            ),
            name=str(row["drone_id"]),
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=720,
    paper_bgcolor="#050914",
    plot_bgcolor="#050914",
    xaxis=dict(
        range=[0, 1000],
        title="X Position (m)",
        showgrid=True,
        gridcolor="#1f2937",
        zeroline=False,
    ),
    yaxis=dict(
        range=[0, 1000],
        title="Y Position (m)",
        scaleanchor="x",
        showgrid=True,
        gridcolor="#1f2937",
        zeroline=False,
    ),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

left, right = st.columns([3, 1])

with left:
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Mission Status")

    st.metric("Active UAOs", len(latest[latest["status"] == "active"]))
    st.metric("Neutralized", len(latest[latest["status"] == "shot_down"]))
    st.metric("High Threats", len(latest[latest["threat_level"] == "high"]))
    st.metric("Friendly", len(latest[latest["friendly"] == True]))

    st.markdown("---")

    high_threats = latest[latest["threat_level"] == "high"]

    if len(high_threats) > 0:
        closest = high_threats.sort_values("distance_to_fob_m").iloc[0]
        st.error("⚠ HIGH PRIORITY CONTACT")
        st.write(f"**Track:** {closest['drone_id']}")
        st.write(f"**Distance:** {closest['distance_to_fob_m']} m")
        st.write(f"**Action:** {closest['countermeasure']}")
    else:
        st.success("No critical threats inside defense zone.")

    st.markdown("---")

    st.subheader("AI Decision Panel")

    if len(latest) > 0:
        priority = latest.sort_values(
            ["threat_score", "distance_to_fob_m"],
            ascending=[False, True],
        ).iloc[0]

        st.write(f"**Priority Track:** {priority['drone_id']}")
        st.write(f"**Classification:** {priority['drone_type']}")
        st.write(f"**Mission:** {priority['mission']}")
        st.write(f"**Threat Score:** {priority['threat_score']}")
        st.write(f"**Recommendation:** {priority['countermeasure']}")

        st.progress(min(float(priority["threat_score"]), 1.0))

    st.markdown("---")

    st.subheader("Latest Tracks")

    st.dataframe(
        latest[
            [
                "drone_id",
                "drone_type",
                "mission",
                "status",
                "threat_level",
                "threat_score",
                "distance_to_fob_m",
                "countermeasure",
            ]
        ],
        use_container_width=True,
    )