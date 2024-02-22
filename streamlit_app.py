import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

import streamlit as st
import plotly.graph_objects as go

# Employee details for hover information
employee_details = {
    '김홍매 / 金红梅 / Kim Hongmae': "Employee detail 1",
    '하지윤 / 河祉赟 / Ha Jiyoon': "Employee detail 2",
    '오은초 / Oh Euncho': "Employee detail 3",
    '신위범 / 申威帆 / Andy Sun': "Employee detail 4",
    '박일수 / 朴日洙 / Park Lisu': "Employee detail 5",
    '전철송 / 田哲松 / Tian Zhesong': "Employee detail 6",
    '임경립 / 林京立 / Lim Kyoungli': "Employee detail 7",
}

# Define the structure of the organization
positions = {
    '会长': {
        '贷款': ['김홍매 / 金红梅 / Kim Hongmae', '하지윤 / 河祉赟 / Ha Jiyoon', '오은초 / Oh Euncho'],
        '工程': ['신위범 / 申威帆 / Andy Sun', '박일수 / 朴日洙 / Park Lisu', '전철송 / 田哲松 / Tian Zhesong', '임경립 / 林京立 / Lim Kyoungli']
    }
}

# Initialize list of nodes, edges, and annotations
nodes = []
edges = []
annotations = []

# Function to create nodes, edges, and annotations
def add_nodes_and_edges(department, members, x, y, x_offset, y_offset):
    # Add department node
    department_node = (x, y, department, 'department')
    nodes.append(department_node)
    annotations.append(dict(x=x, y=y, text=department, showarrow=False, bgcolor="lightblue", borderpad=4, font=dict(color="black")))
    # Create right-angled edge from "会长" to each department node
    president_x, president_y = 0, 0.5
    mid_x = president_x
    mid_y = y  # Horizontal line at the same y as the department for a right angle
    edges.append((president_x, president_y, mid_x, mid_y))  # Vertical part
    edges.append((mid_x, mid_y, x, y))  # Horizontal part to department
    # Add member nodes, edges, and annotations
    for i, member in enumerate(members):
        member_x, member_y = x + x_offset, y - (i + 1) * y_offset
        nodes.append((member_x, member_y, member, 'member'))
        annotations.append(dict(x=member_x, y=member_y, text=member, showarrow=False, bgcolor="lightgreen", borderpad=4, font=dict(color="black")))
        # Create edges with right angles
        edges.append((x, y, x, member_y))
        edges.append((x, member_y, member_x, member_y))

# Add the "会长" node at a specific location
nodes.append((0, 0.5, '会长', 'president'))
annotations.append(dict(x=0, y=0.5, text='会长', showarrow=False, bgcolor="tomato", borderpad=4, font=dict(color="white")))

# Generate nodes and edges for the hierarchy
x_start = -0.4  # Adjust starting x position to spread departments out
y_start = 0  # Starting y position for department nodes
x_offset = 0.4  # Spacing between nodes horizontally
y_offset = 0.1  # Spacing between nodes vertically

for department, members in positions['会长'].items():
    add_nodes_and_edges(department, members, x_start, y_start, x_offset, y_offset)
    x_start += x_offset * 3  # Increase offset to spread departments

# Create traces for nodes with differentiation between roles
node_trace = go.Scatter(
    x=[node[0] for node in nodes],
    y=[node[1] for node in nodes],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        size=[15 if node[3] == 'president' else 10 for node in nodes],
        color=['red' if node[3] == 'president' else 'blue' if node[3] == 'department' else 'green' for node in nodes]
    ),
    hovertext=[employee_details.get(node[2], '') for node in nodes]
)

# Create traces for edges
edge_traces = []
for edge in edges:
    edge_traces.append(go.Scatter(x=[edge[0], edge[2]], y=[edge[1], edge[3]], mode='lines', line=dict(width=2, color='grey'), hoverinfo='none'))

# Create figure, add traces, and update layout
fig = go.Figure()
fig.add_trace(node_trace)
for trace in edge_traces:
    fig.add_trace(trace)
fig.update_layout(
    title="Organization Chart",
    showlegend=False,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor='white',
    annotations=annotations  # Add annotations to the layout
)

# Display the figure in a Streamlit app
st.plotly_chart(fig)

