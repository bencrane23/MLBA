import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="NFL Win Predictor", layout="wide")
st.title("NFL Win Predictor")
st.caption("Upload a CSV file, look at a column, then pick two inputs and a target to see what a straight line predicts.")

# one sentence about what the model is used for and what happens when it is wrong
st.write("This model estimates how many wins a team should expect from the points it scores and allows, and when it is wrong a team can look stronger or weaker than it really is, so treat the number as a rough guide, not a promise.")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) < 3:
        st.error("This file needs at least three numeric columns.")
        st.stop()

    st.subheader("Preview")
    st.dataframe(df.head(), hide_index=True, width="stretch")

    # Chart: the user picks a chart type and a column.
    st.subheader("Chart")
    col1, col2, col3 = st.columns(3)
    chart_type = col1.selectbox("Chart type", ["Line", "Scatter", "Histogram"])
    variable = col2.selectbox("Column to plot", numeric_cols)
    x_axis = col3.selectbox("X axis (line and scatter)", df.columns, disabled=chart_type == "Histogram")

    if chart_type == "Line":
        fig = px.line(df, x=x_axis, y=variable, title=f"{variable} by {x_axis}")
    elif chart_type == "Scatter":
        fig = px.scatter(df, x=x_axis, y=variable, title=f"{variable} versus {x_axis}")
    else:
        fig = px.histogram(df, x=variable, title=f"Distribution of {variable}")
    st.plotly_chart(fig, width="stretch")

    # Model: two inputs and one target.
    # Each select box leaves out the columns already chosen.
    st.subheader("Predict")
    col1, col2, col3 = st.columns(3)
    x1_start = numeric_cols.index("scored") if "scored" in numeric_cols else 0
    x1_col = col1.selectbox("Input 1: what you know", numeric_cols, index=x1_start)
    x2_options = [c for c in numeric_cols if c != x1_col]
    x2_start = x2_options.index("allowed") if "allowed" in x2_options else 0
    x2_col = col2.selectbox("Input 2: what else you know", x2_options, index=x2_start)
    y_options = [c for c in numeric_cols if c not in (x1_col, x2_col)]
    y_start = y_options.index("wins") if "wins" in y_options else 0
    y_col = col3.selectbox("Target: what you want to predict", y_options, index=y_start)

    data = df[[x1_col, x2_col, y_col]].dropna()
    if len(data) < 5:
        st.error("Need at least 5 rows with values in all three columns.")
        st.stop()

    x = data[[x1_col, x2_col]]
    y = data[y_col]
    model = LinearRegression()
    model.fit(x, y)

    m1, m2, m3 = st.columns(3)
    m1.metric(f"Each extra {x1_col} adds", f"{model.coef_[0]:,.3f}")
    m2.metric(f"Each extra {x2_col} adds", f"{model.coef_[1]:,.3f}")
    m3.metric("R2 on this data", f"{model.score(x, y):.2f}")

    # The user types a value for each input, and the app reads the answer from the model.
    st.subheader("Try it")
    v1, v2 = st.columns(2)
    value1 = v1.number_input(f"Enter a value for {x1_col}", value=float(data[x1_col].mean()))
    value2 = v2.number_input(f"Enter a value for {x2_col}", value=float(data[x2_col].mean()))
    prediction = model.predict(pd.DataFrame({x1_col: [value1], x2_col: [value2]}))[0]
    st.metric(f"Predicted {y_col}", f"{prediction:,.1f}")

    # If a typed value is outside the range of the data, the app says so.
    for col, value in [(x1_col, value1), (x2_col, value2)]:
        low, high = data[col].min(), data[col].max()
        if value < low or value > high:
            st.warning(f"{value:,.2f} is outside the range of {col} the model learned from ({low:,.2f} to {high:,.2f}). Treat the number with caution.")
else:
    st.info("Upload a CSV file to get started. It needs at least three numeric columns.")
