/* version.h - version and build information for the whole project
 *
 * Copyright 2021 Oleg Iarygin <oleg@arhadthedev.net>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef FECER_BROVSER_HEADER_H
#define FECER_BROVSER_HEADER_H

#define FECER_BROWSER_VERSION_MAJOR 0
#define FECER_BROWSER_VERSION_MINOR 1
#define FECER_BROWSER_VERSION_PATCH 0
#ifndef FECER_BROWSER_VERSION_SUFFIX
#	error "build with CMake to generate FECER_BROWSER_VERSION_SUFFIX"
#endif

#define STRINGIFY_LITERAL_PARAMETER(token) #token
#define STR(arg) STRINGIFY_LITERAL_PARAMETER(arg)

#define FECER_BROWSER_VERSION_STRING STR(FECER_BROWSER_VERSION_MAJOR) "." \
                                     STR(FECER_BROWSER_VERSION_MINOR) "." \
                                     STR(FECER_BROWSER_VERSION_PATCH) \
                                     FECER_BROWSER_VERSION_SUFFIX

enum FECER_BROWSER_BUILD_TYPES {
	FECER_BROWSER_RELEASE,
	FECER_BROWSER_INDEV,
	FECER_BROWSER_PRIVATE
};
#ifndef FECER_BROWSER_BUILD_TYPE
#	error "build with CMake to generate FECER_BROWSER_BUILD_TYPE"
#endif

#endif  /*  FECER_BROVSER_HEADER_H */
