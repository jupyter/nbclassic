"""Tests for installing nbextensions from archives."""

import io
import tarfile

import pytest

from nbclassic.nbextensions import install_nbextension


def _make_tar(path, name, data=b"x"):
    with tarfile.open(path, "w:gz") as tar:
        info = tarfile.TarInfo(name)
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))


def test_install_tarball(tmp_path):
    nbext = tmp_path / "nbextensions"
    nbext.mkdir()
    tgz = tmp_path / "ext.tar.gz"
    _make_tar(tgz, "myext/main.js")
    install_nbextension(str(tgz), nbextensions_dir=str(nbext))
    assert (nbext / "myext" / "main.js").read_bytes() == b"x"


@pytest.mark.parametrize("name", ["../escaped.js", "myext/../../escaped.js"])
def test_install_tarball_path_traversal(tmp_path, name):
    nbext = tmp_path / "nbextensions"
    nbext.mkdir()
    tgz = tmp_path / "evil.tar.gz"
    _make_tar(tgz, name)
    with pytest.raises((ValueError, tarfile.TarError)):
        install_nbextension(str(tgz), nbextensions_dir=str(nbext))
    assert not (tmp_path / "escaped.js").exists()
