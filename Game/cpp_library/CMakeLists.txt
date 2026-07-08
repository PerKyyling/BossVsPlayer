cmake_minimum_required(VERSION 3.12)
project(astar_lib)

set(CMAKE_CXX_STANDARD 14)

execute_process(
    COMMAND python -c "import pybind11; print(pybind11.get_cmake_dir())"
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")

find_package(pybind11 REQUIRED)

pybind11_add_module(astar_lib main.cpp)

set(PYCHARM_PROJECT_DIR "C:/c++/Game")

add_custom_command(TARGET astar_lib POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:astar_lib> "${PYCHARM_PROJECT_DIR}/$<TARGET_FILE_NAME:astar_lib>"
    COMMENT "building lib"
)
