# CMakeLists.txt - a root build script
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

project(fecer_browser)

find_package(Git)
if(Git_FOUND)
    execute_process(COMMAND "${GIT_EXECUTABLE}" describe --exact-match --tags
                    RESULT_VARIABLE BUILD_IS_AHEAD_OF_TAG
                    OUTPUT_QUIET
                    ERROR_QUIET)
    if(BUILD_IS_AHEAD_OF_TAG)
        execute_process(COMMAND "${GIT_EXECUTABLE}" rev-parse --short HEAD
                        OUTPUT_VARIABLE BUILD_COMMIT_ID
                        ERROR_QUIET
                        OUTPUT_STRIP_TRAILING_WHITESPACE)
        set(BUILD_TYPE FECER_BROWSER_INDEV)
        set(VERSION_SUFFIX "-prealpha.${BUILD_COMMIT_ID}")
    else()
        set(BUILD_TYPE FECER_BROWSER_RELEASE)
        set(VERSION_SUFFIX "")
    endif()
else()
    message(WARNING "Git not found; use current date as a version")
    string(BUILD_TIMESTAMP PROJECT_BUILD_TIME "%Y%m%d%H%M%S")
    set(BUILD_TYPE FECER_BROWSER_ARCHIVE)
    set(VERSION_SUFFIX "-privbuild.${BUILD_TIMESTAMP}")
endif()
add_compile_definitions(FECER_BROWSER_BUILD_TYPE=${BUILD_TYPE})
add_compile_definitions(FECER_BROWSER_VERSION_SUFFIX="${VERSION_SUFFIX}")

if(WIN32)
    add_subdirectory(src/application_winapi)
endif()
