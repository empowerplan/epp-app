"""Module for smaller helper functions."""

import json
import pathlib

import numpy as np
import pandas as pd
from django.http import HttpRequest
from django.template import Template
from django.template.context import make_context
from scipy.interpolate import interp1d


def read_file(filename: str) -> str:
    """Read file."""
    with pathlib.Path(filename).open("r", encoding="utf-8") as f:
        return f.read()


def get_translated_json_from_file(json_filename: str, request: HttpRequest = None) -> dict:
    """
    Render JSON using translations.

    Parameters
    ----------
    json_filename: str
        Path to JSON file
    request: HttpRequest
        Used to create RequestContext and set language from request

    Returns
    -------
    dict
        translated JSON file as dictionary

    """
    with pathlib.Path(json_filename).open("r", encoding="utf-8") as json_file:
        # add {% load i18n %} to file to make django detect translatable strings
        t = Template("{% load i18n %}" + json_file.read())
        c = make_context({}, request)
        translated_json_string = t.render(c)
        return json.loads(translated_json_string)


def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Recursively merge two dictionaries.

    Parameters
    ----------
    dict1: dict
        Containing the first chart structure. Objects will be first.
    dict2: dict
        Containing the second chart structure. Objects will be last and
        if they have the same name as ones from dict1 they overwrite the ones in first.

    Returns
    -------
    dict
        First chart modified and appended by second chart.

    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            merge_dicts(dict1[key], value)
        elif key in dict1 and isinstance(dict1[key], list) and isinstance(value, list):
            dict1[key].extend(value)
        else:
            dict1[key] = value
    return dict1


def interpolate_year_from_dataframe(df: pd.DataFrame, year: int) -> pd.Series:
    """
    Return series from dataframe for given year.

    If the given year is not present in dataframe columns, interpolate the data given available years.
    """
    # Keep only columns which can be converted to an integer (=year)
    no_year_columns = [column for column in df.columns if not isinstance(column, int) and not str.isdigit(column)]
    df = df.drop(no_year_columns, axis=1)

    years = df.columns.astype(float).to_numpy()
    values = df.to_numpy()

    f = interp1d(years, values, axis=1, kind="linear", fill_value="extrapolate", assume_sorted=True)

    return pd.Series(f(year), index=df.index, name=year)


def interpolate_year_from_dict(data: dict, year: int) -> float:
    """Extract or interpolate value from dict for given year."""
    # Sort by year
    data = {int(y): v for y, v in data.items()}
    years = np.array(sorted(data.keys()), dtype=float)
    values = np.array([data[y] for y in years], dtype=float)

    # If exact year exists
    if year in data:
        return data[year]

    f = interp1d(years, values, kind="linear", fill_value="extrapolate", assume_sorted=True)

    return float(f(year))
