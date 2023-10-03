# License: Apache 2.0. See LICENSE file in root directory.
# Copyright(c) 2019 Intel Corporation. All Rights Reserved.
#  minimum required cmake version: 3.1.0
cmake_minimum_required(VERSION 3.1.0)

project(RealsenseExamplesSaveToDisk)
set(DEPENDENCIES realsense2)
add_executable(papamon-save-to-disk rs-save-to-disk.cpp)
set_property(TARGET papamon-save-to-disk PROPERTY CXX_STANDARD 11)
target_link_libraries(papamon-save-to-disk ${DEPENDENCIES})
include_directories(/home/papamon/librealsense/common /home/papamon/librealsense/third-party/third-party /home/papamon/librealsense/third-party/third-party/tclap/include)
set_target_properties (papamon-save-to-disk PROPERTIES FOLDER "Examples")
install(TARGETS papamon-save-to-disk RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
