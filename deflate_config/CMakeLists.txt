cmake_minimum_required(VERSION 3.26...3.29)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module ${SKBUILD_SABI_COMPONENT})

python_add_library(_deflate MODULE WITH_SOABI src/_deflate.c)

if(NOT DEFINED ENV{LIBDEFLATE_PREFIX})
    message(FATAL_ERROR
        "LIBDEFLATE_PREFIX must point to MonolithPy's dependency prefix")
endif()

set(LIBDEFLATE_PREFIX "$ENV{LIBDEFLATE_PREFIX}")

find_path(LIBDEFLATE_INCLUDE_DIR
    NAMES libdeflate.h
    PATHS "${LIBDEFLATE_PREFIX}/include"
    NO_DEFAULT_PATH
    REQUIRED
)

if(WIN32 AND NOT MINGW)
    set(_libdeflate_names deflatestatic)
else()
    set(_libdeflate_names deflate)
endif()

find_library(LIBDEFLATE_STATIC_LIBRARY
    NAMES ${_libdeflate_names}
    PATHS "${LIBDEFLATE_PREFIX}/lib"
    NO_DEFAULT_PATH
    REQUIRED
)

target_include_directories(_deflate PRIVATE
    "${LIBDEFLATE_INCLUDE_DIR}"
)

target_link_libraries(_deflate PRIVATE
    "${LIBDEFLATE_STATIC_LIBRARY}"
)

install(TARGETS _deflate LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME})
