
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def draw_cat_plot():
    # Import the data
    df = pd.read_csv("medical_examination.csv")

    # Add an overweight column
    df["overweight"] = (
        df["weight"] / ((df["height"] / 100) ** 2) > 25
    ).astype(int)

    # Normalize cholesterol and glucose
    df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
    df["gluc"] = (df["gluc"] > 1).astype(int)

    # Convert the data to long format
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=[
            "cholesterol",
            "gluc",
            "smoke",
            "alco",
            "active",
            "overweight",
        ],
    )

    # Group and reformat the data
    df_cat = (
        df_cat.groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )

    # Draw the categorical plot
    grid = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar",
        order=[
            "active",
            "alco",
            "cholesterol",
            "gluc",
            "overweight",
            "smoke",
        ],
    )

    grid.set_axis_labels("variable", "total")
    grid.set_titles("cardio = {col_name}")

    # Return the Matplotlib Figure
    fig = grid.figure
    fig.savefig("catplot.png")

    return fig


def draw_heat_map():
    # Import the data
    df = pd.read_csv("medical_examination.csv")

    # Add an overweight column
    df["overweight"] = (
        df["weight"] / ((df["height"] / 100) ** 2) > 25
    ).astype(int)

    # Normalize cholesterol and glucose
    df["cholesterol"] = (df["cholesterol"] > 1).astype(int)
    df["gluc"] = (df["gluc"] > 1).astype(int)

    # Clean the data
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"])
        & (df["height"] >= df["height"].quantile(0.025))
        & (df["height"] <= df["height"].quantile(0.975))
        & (df["weight"] >= df["weight"].quantile(0.025))
        & (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Mask the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heat map
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        square=True,
        center=0,
        vmax=0.3,
        vmin=-0.3,
        cbar_kws={"shrink": 0.5},
        ax=ax,
    )

    # Save and return the figure
    fig.savefig("heatmap.png")

    return fig
