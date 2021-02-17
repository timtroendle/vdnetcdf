"""Tests for `vdnetcdf` package."""


def test_can_replay_read_of_netcdf(bash):
    output = bash.send("vd -b -p tests/sample_data/cmdlog-01.vd").split("\n")
    assert "replay complete" in output[-1]
