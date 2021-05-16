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

This versioning policy is respected for builds generated on official clones
of the Fecer Browser repository:

- <https://github.com/arhadthedev/fecer-browser>


### Branching

The repository uses a GitLab flow with release branches. A `nextver` branch is
a master, where actual development of features and bugfixes for the next version
is performed. From this branch, release branches `{x}.{y}` are spawned. They are
used to store bugfixes backported from `nextver` to every minor version ever
published. The intent is to make life of distribution package maintainers
easier. Inside a release branch, tags with proper `x.y.z` version numbers are
created.

Builds based on non-tagged commits are considered development, so their version
is set to a pre-release _x_._y_._z_-dev+git._short_commit_id_.


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
