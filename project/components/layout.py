from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd


def create_layout(df: pd.DataFrame) -> html.Div:
    """
    Create the full Dash layout for the NYC collisions dashboard.

    Expected columns in df (rename here if needed):
      - BOROUGH
      - CRASH_YEAR
      - VEHICLE_TYPE_CODE_1
      - CONTRIBUTING_FACTOR_VEHICLE_1
      - PERSON_TYPE
      - PERSON_INJURY
    """

    # ---- Safe unique-option helpers ----
    def sorted_unique(col):
        if col not in df.columns:
            return []
        return sorted(v for v in df[col].dropna().unique())

    borough_options = sorted_unique("BOROUGH")
    year_options = sorted(
        int(y) for y in df["CRASH_YEAR"].dropna().unique()
    ) if "CRASH_YEAR" in df.columns else []
    vehicle_type_options = sorted_unique("VEHICLE_TYPE_CODE_1")
    factor_options = sorted_unique("CONTRIBUTING_FACTOR_VEHICLE_1")
    person_type_options = sorted_unique("PERSON_TYPE")
    injury_options = sorted_unique("PERSON_INJURY")

    # ======================= LAYOUT ==========================
    return dbc.Container(
        className="app-container",
        fluid=True,
        children=[
            # ---------------- TITLE ----------------
            html.H1(
                "NYC Motor Vehicle Collisions – Interactive Explorer",
                className="app-title",
            ),
            html.Div(
                "Use the filters or natural-language search, then click "
                "“Generate Report” to update all visualizations.",
                className="app-subtitle",
            ),

            # ---------------- FILTERS + SEARCH ----------------
            dbc.Card(
                className="filters-card",
                body=True,
                children=[
                    html.Div(
                        "Search (e.g. “Brooklyn 2022 pedestrian crashes killed”)",
                        className="small-label",
                    ),
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Type a query to auto-fill filters",
                        style={"width": "100%", "marginBottom": "10px"},
                    ),

                    dbc.Row(
                        className="filters-row",
                        children=[
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div("Borough", className="small-label"),
                                    dcc.Dropdown(
                                        id="borough-dropdown",
                                        options=[
                                            {"label": b, "value": b}
                                            for b in borough_options
                                        ],
                                        placeholder="Select borough",
                                        clearable=True,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div("Year", className="small-label"),
                                    dcc.Dropdown(
                                        id="year-dropdown",
                                        options=[
                                            {"label": int(y), "value": int(y)}
                                            for y in year_options
                                        ],
                                        placeholder="Select year",
                                        clearable=True,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div("Vehicle Type", className="small-label"),
                                    dcc.Dropdown(
                                        id="vehicle-dropdown",
                                        options=[
                                            {"label": v, "value": v}
                                            for v in vehicle_type_options
                                        ],
                                        placeholder="Select vehicle type",
                                        clearable=True,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div(
                                        "Contributing Factor", className="small-label"
                                    ),
                                    dcc.Dropdown(
                                        id="factor-dropdown",
                                        options=[
                                            {"label": f, "value": f}
                                            for f in factor_options
                                        ],
                                        placeholder="Select factor",
                                        clearable=True,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div("Person Type", className="small-label"),
                                    dcc.Dropdown(
                                        id="person-type-dropdown",
                                        options=[
                                            {"label": p, "value": p}
                                            for p in person_type_options
                                        ],
                                        placeholder="Select person type",
                                        clearable=True,
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div("Injury Severity", className="small-label"),
                                    dcc.Dropdown(
                                        id="injury-dropdown",
                                        options=[
                                            {"label": i, "value": i}
                                            for i in injury_options
                                        ],
                                        placeholder="Select injury",
                                        clearable=True,
                                    ),
                                ],
                            ),
                        ],
                    ),

                    html.Button(
                        "Generate Report",
                        id="generate-button",
                        n_clicks=0,
                        style={
                            "marginTop": "10px",
                            "padding": "8px 18px",
                            "borderRadius": "999px",
                            "border": "none",
                            "backgroundColor": "#2563eb",
                            "color": "white",
                            "fontWeight": "600",
                            "cursor": "pointer",
                        },
                    ),

                    html.Div(
                        id="filter-summary",
                        style={
                            "marginTop": "6px",
                            "fontSize": "13px",
                            "color": "#555",
                        },
                    ),
                ],
            ),

            # ---------------- SUMMARY KPIs ----------------
            dbc.Card(
                className="summary-card",
                body=True,
                children=[
                    dbc.Row(
                        className="summary-row",
                        children=[
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div(
                                        id="summary-total-crashes",
                                        className="summary-metric",
                                    ),
                                    html.Div("Total crashes", className="summary-label"),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div(
                                        id="summary-total-persons",
                                        className="summary-metric",
                                    ),
                                    html.Div(
                                        "Total persons involved",
                                        className="summary-label",
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div(
                                        id="summary-total-injuries",
                                        className="summary-metric",
                                    ),
                                    html.Div(
                                        "Total injuries", className="summary-label"
                                    ),
                                ],
                            ),
                            dbc.Col(
                                className="filter-item",
                                children=[
                                    html.Div(
                                        id="summary-total-fatalities",
                                        className="summary-metric",
                                    ),
                                    html.Div(
                                        "Total fatalities",
                                        className="summary-label",
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),

            # ---------------- FIRST ROW OF GRAPHS ----------------
            dbc.Row(
                className="graphs-row",
                children=[
                    dbc.Col(
                        className="graph-card graph-half",
                        children=[
                            html.H3(
                                "Crashes over time",
                                style={"fontSize": "17px", "marginBottom": "8px"},
                            ),
                            dcc.Graph(id="time-series-graph", style={"height": "350px"}),
                        ],
                    ),
                    dbc.Col(
                        className="graph-card graph-half",
                        children=[
                            html.H3(
                                "Crashes by borough",
                                style={"fontSize": "17px", "marginBottom": "8px"},
                            ),
                            dcc.Graph(id="borough-bar-graph", style={"height": "350px"}),
                        ],
                    ),
                ],
            ),

            # ---------------- SECOND ROW OF GRAPHS ----------------
            dbc.Row(
                className="graphs-row",
                children=[
                    dbc.Col(
                        className="graph-card graph-half",
                        children=[
                            html.H3(
                                "Injury outcome distribution",
                                style={"fontSize": "17px", "marginBottom": "8px"},
                            ),
                            dcc.Graph(id="injury-pie-graph", style={"height": "350px"}),
                        ],
                    ),
                    dbc.Col(
                        className="graph-card graph-half",
                        children=[
                            html.H3(
                                "Crash locations (sample)",
                                style={"fontSize": "17px", "marginBottom": "8px"},
                            ),
                            dcc.Graph(id="location-scatter-graph", style={"height": "350px"}),
                        ],
                    ),
                ],
            ),

            # ---------------- THIRD ROW (HEATMAP) ----------------
            dbc.Row(
                className="graphs-row",
                children=[
                    dbc.Col(
                        className="graph-card graph-half",
                        children=[
                            html.H3(
                                "Crash density by hour & borough",
                                style={"fontSize": "17px", "marginBottom": "8px"},
                            ),
                            dcc.Graph(id="heatmap-graph", style={"height": "350px"}),
                        ],
                    ),
                ],
            ),
        ],
    )
