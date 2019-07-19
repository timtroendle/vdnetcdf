from itertools import product
from functools import reduce

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
    rowtype = 'data'  # rowdef: coords mapping

    @asyncthread
    def reload(self):
        da = self.source

        self.columns = []
        self.rows = []

        for dim in da.dims:
            self.addColumn(ColumnItem(dim, type=type_mapping(da[dim].dtype)))
        self.addColumn(Column(da.name, type=type_mapping(da.dtype), getter=lambda col, row: da.loc[row]))

        number_rows = reduce(lambda x, y: x * y, da.sizes.values())
        coords_iterator = product(*[da.coords[dim].values for dim in da.dims])
        for coords in Progress(coords_iterator, total=number_rows):
            self.addRow(dict(zip(list(da.dims), coords)))


def type_mapping(dtype):
    if dtype.str[1] == "f":
        return float
    elif dtype.str[1] == "i":
        return int
    else:
        return anytype
