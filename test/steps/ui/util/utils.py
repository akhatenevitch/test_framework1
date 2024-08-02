def parse_str_table(table_with_headers):
    list_table_rows = table_with_headers.split("\n")
    list_headers = str(list_table_rows[0]).strip("|").split("|")
    dict_table = {}
    for header in list_headers:
        header_text = header.strip()
        lst_row = []
        for i in range(1, len(list_table_rows)):
            list_temp = list_table_rows[i].strip("|").split("|")
            lst_row.append(list_temp[list_headers.index(header)].strip())

        dict_table[header_text] = lst_row

    print(dict_table)
    return dict_table


def create_json_from_dict_table(dict_table):
    result_json = {}
    for key, value in dict_table.items():
        parts = key.split('.')
        data = result_json
        for part in parts[:-1]:
            if part not in data:
                data[part] = {}
            data = data[part]
        data[parts[-1]] = value

    return result_json
