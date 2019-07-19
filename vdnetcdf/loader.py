from visidata import Sheet, Column, ColumnItem, Progress, anytype, asyncthread, ENTER


def open_nc(path):
    return VariablesSheet(path.name, source=path)


class VariablesSheet(Sheet):
    rowtype = 'variables'  # rowdef: xr.DataArray

    columns = [
        Column('variable', getter=lambda col, row: row[0]),
        Column('dtype', getter=lambda col, row: row[1].dtype),
    ]

    def reload(self):
        import xarray as xr
        ds = xr.open_dataset(str(self.source))
        self.rows = []
        for r in ds.data_vars.items():
            vs = DataArraySheet(r[0], source=r[1])
            self.rows.append((r[0], r[1], vs))


VariablesSheet.addCommand(ENTER, 'dive-row', 'vd.push(cursorRow[2])')


class DataArraySheet(Sheet):
    rowtype = 'data'  # rowdef: pd.DataFrame row

    @asyncthread
    def reload(self):
        da = self.source
        df = da.to_dataframe().reset_index()

        self.columns = []
        self.rows = []

        rows = [row for idx, row in df.iterrows()]

        for column in df:
            self.addColumn(ColumnItem(column, type=type_mapping(df[column].dtype)))

        for r in Progress(rows):
            self.addRow(r)


def type_mapping(dtype):
    if dtype.str[1] == "f":
        return float
    elif dtype.str[1] == "i":
        return int
    else:
        return anytype
