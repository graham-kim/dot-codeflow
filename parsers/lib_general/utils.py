def prepend_clus_name(clus_full_name: str, text: str) -> str:
    if clus_full_name:
        return f"{clus_full_name}_{text}"
    else:
        return text

def escape_angular_brackets(label: str) -> str:
    return label.replace('<', '&lt;').replace('>', '&gt;')

def substitute_angular_brackets_after_escaping(label: str) -> str:
    return escape_angular_brackets(label)\
            .replace('[[', '<').replace(']]', '>').replace('\\n', '<BR/>')
