from visidata import IndexSheet, TableSheet, Column, ItemColumn, Progress, anytype, date


def open_nc(path):
    return DatasetSheet(path.name, source=path)


class DatasetSheet(IndexSheet):
    rowtype = 'variables'  # rowdef: xr.DataArray

    columns = [
        Column('variable', getter=lambda col, row: row.source.name),
        Column('dtype', getter=lambda col, row: row.source.dtype),
        Column('size', getter=lambda col, row: row.source.size),
        Column('dimensions', getter=lambda col, row: row.source.dims),
    ]

    def iterload(self):
        import xarray as xr
        ds = xr.open_dataset(str(self.source))
        for r in ds.data_vars.items():
            yield DataArraySheet(source=r[1])

    def attributeSheet(self):
        import xarray as xr
        ds = xr.open_dataset(str(self.source))
        return AttributeSheet(f"{self.name}-attrs", source=ds)


class DataArraySheet(TableSheet):
    rowtype = 'datapoints'  # rowdef: map

    def iterload(self):
        da = self.source

        self.columns = []

        for dim in list(da.dims) + [coords for coords in da.coords if coords not in da.dims]:
            self.addColumn(ItemColumn(dim, type=type_mapping(da[dim].dtype)))
        self.addColumn(ItemColumn(da.name, type=type_mapping(da.dtype)))
        for row in Progress(da.to_dataframe().reset_index().iterrows(), total=da.size):
            yield row[1].to_dict()

    def attributeSheet(self):
        return AttributeSheet(f"{self.name}-attrs", source=self.source)


class AttributeSheet(TableSheet):
    rowtype = 'attributes'  # rowdef: attributes

    columns = [
        Column('key', getter=lambda col, row: row[0]),
        Column('value', getter=lambda col, row: row[1]),
    ]

    def iterload(self):
        for k, v in Progress(self.source.attrs.items()):
            yield (k, v)


DatasetSheet.addCommand('^A', 'show-attributes', 'vd.push(attributeSheet())')
DataArraySheet.addCommand('^A', 'show-attributes', 'vd.push(attributeSheet())')


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
