"""Tests for `vdnetcdf` package."""


def test_can_replay_read_of_netcdf(bash):
    bash.send("vd -b -p tests/sample_data/cmdlog-01.vd --config tests/.visidatarc").split("\n")
    assert bash.last_return_code == 0
