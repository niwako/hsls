#!/usr/bin/env python3


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
        for ordered_code in ("Strongly agree", "Agree", "Disagree", "Strongly disagree")
    )


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
