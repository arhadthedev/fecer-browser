# CMakeLists.txt - a build script for fecer_browser.exe
#
# Copyright 2021 Oleg Iarygin <oleg@arhadthedev.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 3.1)

add_executable(fecer_browser WIN32 res/fecer_browser.rc main.c)
target_include_directories(fecer_browser PRIVATE "../../include")

set(ICON_IN doc/logo.png)
set(ICON_OUT ${CMAKE_CURRENT_BINARY_DIR}/main.ico)
execute_process(COMMAND python util/mypng2ico.py ${ICON_IN} ${ICON_OUT} 256
                WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
target_compile_definitions(fecer_browser PRIVATE FECER_BROWSER_ICON="${ICON_OUT}")
