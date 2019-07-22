from visidata import Sheet, Column, ColumnItem, anytype, date, asyncthread, ENTER


def open_nc(path):
    return DatasetSheet(path.name, source=path)


class DatasetSheet(Sheet):
    rowtype = 'variables'  # rowdef: xr.DataArray

    columns = [
        Column('variable', getter=lambda col, row: row[0]),
        Column('dtype', getter=lambda col, row: row[1].dtype),
        Column('dimensions', getter=lambda col, row: row[1].dims),
        Column('size', getter=lambda col, row: row[1].size)
    ]

    def reload(self):
        import xarray as xr
        ds = xr.open_dataset(str(self.source))
        self.rows = []
        for r in ds.data_vars.items():
            vs = DataArraySheet(r[0], source=r[1])
            self.rows.append((r[0], r[1], vs))


DatasetSheet.addCommand(ENTER, 'dive-row', 'vd.push(cursorRow[2])')


class DataArraySheet(Sheet):
    rowtype = 'data'  # rowdef: map

    @asyncthread
    def reload(self):
        da = self.source

        self.columns = []

        for dim in list(da.dims) + [coords for coords in da.coords if coords not in da.dims]:
            self.addColumn(ColumnItem(dim, type=type_mapping(da[dim].dtype)))
        self.addColumn(ColumnItem(da.name, type=type_mapping(da.dtype)))

        self.rows = da.to_dataframe().reset_index().to_dict(orient="records")


def type_mapping(dtype):
    type_char = dtype.str[1]
    if type_char == "f":
        return float
    elif type_char == "i":
        return int
    elif type_char == "M":
        return date
    else:
        return anytype
