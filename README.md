# <img src="doc/logo.png" width="32" alt=""> Fecer Browser

A blazing fast web browser with a little memory footprint capable of hundreds of
tabs at the same time.


## How to contribute

See CONTRIBUTING.md.


## For developers

### Branching

Fecer Browser repository uses a GitLab flow with release branches, so you can
choose any major or minor version by checking out the corresponding branch.

`nextver` branch is the main one (known in Git as master), where actual
development of features and bug fixes for the next version is performed.

From `nextver`, release branches `{x}.{y}` are spawned. They are used to store
bugfixes backported from `nextver`, so UNIX and Linux distributions may obtain
fixes into stable and oldstable editions with no extra effort.

Inside a release branch, tags with proper `x.y.z` version numbers are created
for commits used to generate installers and other deployment artifacts.

### How to get sources

A central development point is a Git repository which equally treated mirrors
are spread across some hostings:

- <https://github.com/arhadthedev/fecer-browser>

Since each hosting has its own issue tracker, you can use any; every one of them
is tracked.

Also, source code is available as `fecer-browser-dev` package in <del>Chocolatey</del>,
<del>Ubuntu PPA</del>, and <del>Debian Sid package repository</del>.

### Directory structure

The original source code directory contains the following subdirectories:

#### .github

GitHub-specific files like a code of conduct, issue and pull request templates,
configuration files for GitHub Actions.

#### doc

Doxygen-generated documentation for public API (`api_autogen`), source files for
man pages (`man`), source files for a manual installed to users (`user_manual`).

#### include

Public header files available both to other components of Fecer Browser and to
external programs.

- fecer_browser/os/\*.h  — declarations from src/browser_engine_\*
- fecer_browser/widgets/{qt, winapi}/\*.h — declarations from
  src/browser_engine_\* related to widgets
- fecer_browser/script/\*.h  — declarations from src/script_engine_\*
- fecer_browser/\*.h  — declarations from src/browser_engine

#### src

Each directory contains artifacts required to compile some library or
an executable:

- application_* — a thin GUI wrapper around browser_engine. Also an example of
  how to use libfecer_browser

- browser_engine — system-independent logic of how a web browser needs to work
  and how its parts interact. Compiled into a static library libfecer_browser

- browser_engine_* — system-dependent shims that turn abstract queries to OS
  objects to system-defined API calls. Compiled into a static library
  libfecer_browser_system_*

  Also, this directory contains widgets compiled into a dynamic library for Qt
  and Gtk, and a static library for Windows.

- script_engine — an SSA function-less type-annotated virtual machine and AOT
  optimizing compiler for ECMAScript (ECMA-262) and W3C WebAssembly. Compiled
  into a static library libfecer_browser_script

Libraries are static because they are included in widget dynamic libraries
that wrap bare C functions into conventions used by a GUI framework a library
is designed for (like Qt), or just reexports selected functions anyway.

#### tests

Unit and conformance test for everything located in `src` directory. They are
not built by default; you need to install extra development dependencies and
explicitly build `tests` target; see section “How to build sources - Building
and running - Tests” below.

#### util

Programs and scripts used to generate source files and other input artifacts
used in the compilation of shipped components.

### How to build sources

1. Install a development environment:

   For Windows it can be, for example, one of the following sets:

   - CMake, Ninja, LLVM+Visual Studio Build Tools, Windows SDK
   - CMake, Ninja, MinGW-w64
   - Visual Studio >= 16.8 (2019, when C11 support was added)

   Technically, C99 only is needed. However, Microsoft denies its support
   because of its insecure on-stack variable-length arrays. Instead, it supports
   C11 that makes such a feature optional.

   Then, install Python >= 3.2 (because of argparse) to run scripts from `util`.

   NOTE: Mac OS X toolkit is not supported because Apple's App Store Review
   Guidelines state, therefore banning Fecer Browser on Apple ecosystem:

   > 2.5.6. Apps that browse the web must use the iOS WebKit framework
   > and WebKit Javascript.

   *Reference: <https://developer.apple.com/app-store/review/guidelines/#software-requirements>.*

   Any browser there is just a thin wrapper around WebKit with their competitive
   engines stripped away. Apple's Safari, though, uses a more modern Nitro
   engine.

2. Optionally, to build tests, install Boost.Test.

### How to prepare a project

To generate build environment from CMakeLists.txt, create a separate directory
for out-of-source build (`build` in a root of `fecer-browser` is recommended
because it is explicitly hidden from versioning via .gitignore), navigate
a command line shell inside and run one of the following:

```bash
# A recommended variant
cmake -G Ninja -DCMAKE_BUILD_TYPE="Release" ..

# For UNIX and Linux users without Ninja installed
cmake -DCMAKE_BUILD_TYPE="Release" ..

# For MinGW Windows users without Ninja installed
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE="Release" ..

# For Visual Studio users no matter whether Ninja installed or not
cmake -G "Visual Studio 16 2019" ..

# For LLVM users see below
```

You need to run this command only once, for an empty build directory.
A generated environment has a built-in check for modifications of source
CMakeLists.txt files.

#### For LLVM+Visual Studio Build Tools users

To build `application_winapi`, a compiler for \*.rc files is required. The one
supplied with LLVM (llvm-rc) is incomplete, so use rc.exe supplied with Windows
SDK instead.

For this, you need to know where the SDK is installed (for example,
`C:/Program Files (x86)/Windows Kits/10`). Navigate into `Include` and `bin`
directories and copy a path to a version folder inside referred further as
`{INC}` and `{BIN}` (for example,
{INC}=`C:/Program Files (x86)/Windows Kits/10/Include/10.0.10240.0`,
{BIN}=`C:/Program Files (x86)/Windows Kits/10/bin/10.0.18362.0`).

Then, find out where Visual Studio tools are installed, referred further as
`{VC}` (for example,
{VC}=`C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.28.29910`).

Then, run a command as in "How to prepare a project", but with extra keys:

- -DCMAKE_RC_COMPILER="{BIN}/x86/rc.exe"
- -DCMAKE_RC_FLAGS="-I\"{INC}/um\" -I\"{INC}/shared\" -I\"{INC}/ucrt\" -I\"{VC}/include\""

### Building and running

#### Code

To build Fecer Browser components from a prepared environment directory, use:

```bash
cmake --build . --config Release
```

#### Tests

The command above does not build tests. You need to specify a target explicitly:

```bash
cmake --build . --config Release --target tests
```

To run tests from Visual Studio, make `tests` project active (menu
`Project -> Properties`, then category `Common Properties -> Startup Project`,
a field `Single startup project`).

#### Documentation

To generate API manual in `doc/api_autogen`, run Doxygen from `doc` directory.


# For users

## Versions

Fecer Browser follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Definitions:

- *API of a library*:
  - declarations in files inside `include/` directory
  - format of input/output data streams

- *API of an application*:
  - position and composition of GUI elements for a user with a monitor, a user
    with a reader, and an automation script
  - format of both profile and user files

- *initial development*: a state until the following test snapshots are passed:
  - <https://github.com/tc39/test262/commit/6d353a4>
  - <https://github.com/web-platform-tests/wpt/commit/07ae085>

This versioning policy is respected for builds generated on official clones
of the Fecer Browser repository:

- <https://github.com/arhadthedev/fecer-browser>

Builds based on non-tagged commits are considered development, so their version
is set to a pre-release _x_._y_._z_-prealpha._short_commit_id_.

Fecer Browser components are tightly coupled in features, so the whole
mono repository shares the same version number.


## How to get built binaries

Installers and portable builds are available via:

- official Fecer Browser download page: *to bo done*
- GitHub releases: <https://github.com/arhadthedev/fecer-browser/releases>

Also, some UNIX and Linux distributions provide `fecer-browser` package:

- *to be done; distribution names and corresponding versions*


## How to report bugs

*To be done*


## Legal information

Copyright © 2021 Oleg Iarygin <oleg@arhadthedev.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
