def snake_to_camelcase(value: str):
    [first, *rest] = value.split("_")
    rest = map(lambda x: x.capitalize(), rest)
    return "".join([first, *rest])
