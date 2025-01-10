def apply_filters(data, filters):
    # Примитивная реализация фильтра
    return [item for item in data if all(f(item) for f in filters)]