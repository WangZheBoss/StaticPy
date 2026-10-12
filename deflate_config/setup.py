from __future__ import annotations

import os
from pathlib import Path

from setuptools import Extension, find_packages, setup


ROOT = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# libdeflate installation
#
# You can either:
#
#   1. Set LIBDEFLATE_PREFIX:
#
#      set LIBDEFLATE_PREFIX=C:\path\to\libdeflate
#
#   Expected layout:
#
#      C:\path\to\libdeflate\
#          include\
#              libdeflate.h
#          lib\
#              deflate.lib
#
#   2. Or edit the fallback path below.
# ---------------------------------------------------------------------------

LIBDEFLATE_PREFIX = os.environ.get("LIBDEFLATE_PREFIX")

LIBDEFLATE_PREFIX = Path(LIBDEFLATE_PREFIX)


LIBDEFLATE_INCLUDE_DIR = LIBDEFLATE_PREFIX / "include"
LIBDEFLATE_LIBRARY_DIR = LIBDEFLATE_PREFIX / "lib"


# If your compiled library has another name, change this value.
#
# Common possibilities:
#
#   deflate.lib
#   libdeflate_static.lib
#
LIBDEFLATE_LIBRARY = "deflate"


if os.name == "nt":
    WINDOWS_LIBRARIES = [
        "Ws2_32",
        "Version",
        "Shlwapi",
        "Bcrypt",
    ]
else:
    WINDOWS_LIBRARIES = []


extension = Extension(
    name="deflate._deflate",
    sources=[
        str("src/_deflate.c"),
    ],
    include_dirs=[
        str(LIBDEFLATE_INCLUDE_DIR),
    ],
    library_dirs=[
        str(LIBDEFLATE_LIBRARY_DIR),
    ],
    libraries=[
        LIBDEFLATE_LIBRARY,
        *WINDOWS_LIBRARIES,
    ],
    language="c",
)


setup(
    name="deflate",
    version="0.9.0",
    description="Python wrapper for libdeflate.",
    url="https://github.com/dcwatson/deflate",
    author="Dan Watson",
    author_email="danwatson@gmail.com",
    license="",
    package_dir={"": "src"},
    packages=find_packages("src"),
    ext_modules=[
        extension,
    ],
    package_data={
        "deflate": [
            "*.pyi",
            "py.typed",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)