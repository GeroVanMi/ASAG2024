import pandas as pd
from altair import (
    Chart,
    Color,
    Column,
    FieldName,
    Header,
    RangeScheme,
    Row,
    TitleParams,
    Undefined,
    X,
    Y,
    hconcat,
)

from configuration import data_source_colors


def altair_boxplot(
    dataframe: pd.DataFrame,
    y_variable: str,
    x_variable: str,
    title: str = "",
    y_name: str = "",
    domainMax: int | float = Undefined,
    width=100,
    height=250,
    boxplot_size=50,
):
    return (
        Chart(dataframe)
        .mark_boxplot(size=boxplot_size)
        .encode(
            x=X(x_variable).axis().title(""),
            y=Y(y_variable).title(y_name).scale(domainMax=domainMax),
            color=Color(x_variable, legend=None),
        )
        .properties(
            width=width,
            height=height,
            title=title,
        )
    )


def altair_distribution_plot(
    dataframe: pd.DataFrame,
    columns: list[str | FieldName],
    title: str,
    row_sort_order: str | list[str] = "ascending",
    number_of_bins=6,
    x_max_value=1,
):
    header = Header(labelFontWeight="bold")
    type_fold_name = "Type"
    grade_fold_name = "PredictedGrade"

    data_sources = dataframe["data_source"].unique()
    charts = []
    for data_source in data_sources:
        filtered_df = dataframe[dataframe["data_source"] == data_source]
        charts.append(
            Chart(filtered_df)  # type: ignore
            .transform_fold(columns, as_=[type_fold_name, grade_fold_name])
            .mark_bar(opacity=1, binSpacing=0)
            .encode(
                x=X(f"{grade_fold_name}:Q")
                .bin(maxbins=number_of_bins)
                .title("")
                .scale(domainMax=x_max_value),
                y=Y("count()").title(""),
                color=Color("data_source", legend=None),
                column=Column("data_source", header=header).title(""),
                row=Row(
                    f"{type_fold_name}:N", header=header, sort=row_sort_order
                ).title(""),
            )
            .resolve_scale(y="shared")
            .properties(width=200)
        )

    return (
        hconcat(*charts)
        .configure_range(category=RangeScheme(data_source_colors))
        .properties(
            title=TitleParams(
                title,
                fontSize=20,
                dy=-30,
                anchor="middle",
                align="center",
                fontWeight="bold",
            ),
        )
    )
