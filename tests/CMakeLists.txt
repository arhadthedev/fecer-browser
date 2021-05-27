# CMakeLists.txt - a build script for tests
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

# Boost::boost in FindBoost was introduced in 3.5
cmake_minimum_required(VERSION 3.5)

# Boost 1.59 because of Boose.Test v3 (BOOST_TEST generic assertion
# and data driven test cases)
#
# Reference: <https://www.boost.org/doc/libs/1_74_0/libs/test/doc/html/boost_test/change_log.html#boost_test.change_log.boost_test_v3_boost_1_59>
find_package(Boost 1.59 REQUIRED)         

add_executable(tests_unit EXCLUDE_FROM_ALL
               unit/shared.cpp)
target_link_libraries(tests_unit Boost::boost)
add_test(NAME unit COMMAND tests_unit)
