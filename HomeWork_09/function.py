TABLE_WIDTH = 140


def format_phone_num(pn: str) -> str:
    return f"+{pn[:3]}({pn[3:5]}){pn[5:8]}-{pn[8:10]}-{pn[10:]}"


def sanitize_phone_num(pn: str) -> str:
    tel_code = {9: "380", 10: "38"}
    snz_phone = "".join([ch for ch in pn if ch.isdecimal()])
    if len(snz_phone) not in (9, 10, 12):
        raise ValueError(f"Entered phone '{pn}' is incorrect.")
    return tel_code.get(len(snz_phone), "") + snz_phone


def easy_table(data: list, cell_sep=' | ', header_separator=True) -> str:
    rows = len(data)
    cols = len(data[0])

    cols_align = ["R" for _ in range(cols)]
    first_data_row = 1 if header_separator else 0
    for num, item in enumerate(data[first_data_row]):
        try:
            float(item)
        except ValueError:
            cols_align[num] = "L"

    header_row = 0 if header_separator else -1
    max_area_width = TABLE_WIDTH - cols * 3
    col_max_width = int(max_area_width / cols)
    out_list = []

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        max_col_width = len(max(columns, key=len))
        col_width.append(max_col_width if max_col_width < col_max_width else col_max_width)

    free_size = max_area_width - sum(col_width)
    if free_size:
        col_trunc_qty = len([i for i in col_width if i == col_max_width])
        if col_trunc_qty:
            add_size = int(free_size / col_trunc_qty)
            for idx in range(len(col_width)):
                if col_width[idx] == col_max_width:
                    col_width[idx] += add_size

    separator = "-+-".join('-' * n for n in col_width)

    out_list.append(separator)
    for i, row in enumerate(range(rows)):
        if i == 1 and header_separator:
            out_list.append(separator)

        col_pos = [0] * cols
        while True:
            result = []
            for col in range(cols):
                idx_start = col_pos[col]
                idx_end = idx_start + col_width[col]
                sub_str = data[row][col][idx_start:idx_end+1].replace("\n", " ")
                if len(sub_str.rstrip()) > col_width[col]:
                    ind_spc = sub_str.rfind(" ")
                    if ind_spc != -1:
                        sub_str_t = sub_str[0:ind_spc]
                        if sub_str_t.strip():
                            sub_str = sub_str_t
                            idx_end = idx_start + len(sub_str) + 1  # fact
                        else:
                            sub_str = sub_str[0:col_width[col]]
                    else:
                        sub_str = sub_str[0:col_width[col]]
                    item = sub_str.strip().ljust(col_width[col])
                else:
                    item = sub_str.rstrip().ljust(col_width[col])

                if row > header_row and cols_align[col] == "R":
                    item = sub_str.strip().rjust(col_width[col])
                result.append(item)
                col_pos[col] = idx_end
            if "".join(result).strip():
                out_list.append(cell_sep.join(result))
            else:
                break
    out_list.append(separator)
    return "\n".join(out_list)
