def prepend_clus_name(clus_full_name: str, text: str) -> str:
    if clus_full_name:
        return f"{clus_full_name}_{text}"
    else:
        return text