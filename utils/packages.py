def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

def get_list(query):
    stuff = [dict(record) for record in query]
    stuff = [list(record.values()) for record in query]
    stuff = [record[0] for record in query]
    return stuff