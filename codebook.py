#!/usr/bin/env python3
import functools
import pandas as pd


REVERSED_CATEGORIES = {
    "X1SEX",
    "S1MTCHMFDIFF",
    "S1STCHMFDIFF",
    "S1MPERSON1",
    "S2MPERSON1",
    "S4MPERSON1",
    "S1SPERSON1",
    "S2SPERSON1",
    "S4SPERSON1",
}


@functools.cache
def variable_labels():
    labels = {}
    name = None

    with open("Codebook.txt", "r") as fp:
        for line in fp:
            if line.strip() == "":
                name = None
                continue

            if line.startswith("Name:"):
                name = line[12:].strip()
                continue

            if line.startswith("Label:"):
                labels[name] = line[12:].strip()
                continue

    return labels


@functools.cache
def student_encodings():
    DEFAULT = 0
    VALUE = 1

    state = DEFAULT
    encodings = {}
    name = None

    with open("Layout_STUDENT.txt", "r") as fp:
        for line in fp:
            if line.strip() == "":
                state = DEFAULT
                continue

            if line.strip() == "/* Variable Value Labels */":
                state = VALUE
                continue

            if state == VALUE:
                if not line.startswith(" "):
                    name = line.strip()
                    encodings[name] = {}
                else:
                    code, desc = line.strip().split(" = ")
                    if name in ("X2UNIV1", "X3UNIV1", "X4UNIV1"):
                        encodings[name][code] = eval(desc)
                    else:
                        encodings[name][eval(code)] = eval(desc)

    return encodings


def is_ordered(*, encoding):
    return any(
        ordered_code in encoding.values()
        for ordered_code in (
            "Strongly agree",
            "Agree",
            "Disagree",
            "Strongly disagree",
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
        )
    )


def to_categorical(column):
    encodings = student_encodings()
    categories = [v for k, v in encodings[column.name].items() if k >= 0]
    return (
        column.astype("category")
        .cat.rename_categories(encodings[column.name])
        .cat.set_categories(
            reversed(categories) if column.name in REVERSED_CATEGORIES else categories,
            ordered=is_ordered(encoding=encodings[column.name]),
        )
    )


def relabel(df, axis=1):
    labels = variable_labels()

    if type(df) == pd.Series:
        df = df.rename(labels[df.name])

    if type(df) == pd.DataFrame:
        if df.index.name in labels:
            df.index = df.index.rename(labels[df.index.name])
        if df.columns.name in labels:
            df.columns = df.columns.rename(labels[df.columns.name])
        if axis in (0, "index", 2, "both"):
            df = df.rename(variable_labels(), axis=0)
        if axis in (1, "column", 2, "both"):
            df = df.rename(variable_labels(), axis=1)

    return df