from itertools import product
from functools import reduce

from visidata import Sheet, Column, ColumnItem, Progress, anytype, asyncthread, ENTER


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
        self.rows = []

        for dim in da.dims:
            self.addColumn(ColumnItem(dim, type=type_mapping(da[dim].dtype)))
        non_dim_coords = [coords for coords in da.coords if coords not in da.dims]
        for non_dim_coord in non_dim_coords:
            self.addColumn(ColumnItem(non_dim_coord, type=type_mapping(da[non_dim_coord].dtype)))
        self.addColumn(ColumnItem(da.name, type=type_mapping(da.dtype)))

        number_rows = reduce(lambda x, y: x * y, da.sizes.values())
        coords_iterator = product(*(da.coords[dim].values for dim in da.dims))
        for coords in Progress(coords_iterator, total=number_rows):
            row = dict(zip(list(da.dims), coords))
            row[da.name] = da.loc[row].item()
            for non_dim_coord in non_dim_coords:
                idx = {k: v for k, v in row.items() if k in da[non_dim_coord].dims}
                row[non_dim_coord] = da[non_dim_coord].loc[idx].item()
            self.addRow(row)


def type_mapping(dtype):
    if dtype.str[1] == "f":
        return float
    elif dtype.str[1] == "i":
        return int
    else:
        return anytype
