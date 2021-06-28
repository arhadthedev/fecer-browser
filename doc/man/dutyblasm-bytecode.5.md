% dutyblasm-bytecode(5)
% Oleg Yarigin
% June 25, 2021

# Name

dutyblasm-bytecode - format of dutyblasm bytecode


# Description

A dutyblasm bytecode format is an intermediate representation (IR) for dutyblasm
virtual machine. It is designed to simplify: 1) optimizations of dynamic
inferred structural values, 2) static analysis for early errors, 2) bytecode
itself by moving as much features as possible into generalized backend
heuristics.

The virtual machine is register based. However, registers are not assignable;
instead, each command gets its own, implicit output register accessible by
a sequential number of a command. If a command does not produce a result or
has a greater sequential number than the current one, its output register
behaves like it contains *undefined* value (see Register value types below).

All commands have no side effects; they take up to three register numbers and
produce a value into their implicit output register. For *map*s and *list*s,
a setter command produces a copy; it is up to a virtual machine to translate
such an approach into Copy-on-Write or some other semantics via static analysis.

Since commands may operate values only, execution control branching is done via
grouping commands into basic blocks that capture values into registers on input,
shifting command sequential numbers and do value-based branching on output. Each
basic block may have up to 256 registers, split between commands and captures
of specified global integers, reals, buffers, basic block references,
and registers of caller basic blocks.

Basic blocks, along with global literal capturable data are placed into
a module. This page describes a format of module content stream; a format of
a container, stream encoding and start&end determination is set on case by case
basis.

A virtual machine is able to run a single module. So all modules need to be
merged and probably optimized using routines provided by **dutyblasm(1)** or
**dutyblasm(3)**.

Execution of a module is synchronous with a host; however, each host thread may
start its own that will be concurrent with others inside a bytecode. To start,
a host prepares some registers and passes them to a virtual machine. The machine
calls the first (entry) basic block of a module pretending it was called by some
other block with the registers set to the passed values. The first block then
may pass control to other blocks in the same module. Finally, some block passes
control to a special exit block not defined by a module, but obtained by a host
and passed along with other values. It causes a virtual machine to end bytecode
execution and return registers of the last block to a host. A host can repeat
the procedure until a virtual machine is released.


## Register value types

A value in a register may be one of the following types:

- *undefined*, a token returned when accessing a yet non-existing value;
- *boolean*,   a value that can be either 0 or 1;
- *integer*,   a 32-bit signed two-complement integer number;
- *real*,      a double-precision IEEE 754-2019 binary number;
- *buffer*,    a list of octets that can be dynamically treated as a list
               of arbitrary-length signed/unsigned integers;
- *map*,       an ordered sequence of tagged values.

The type defines behavior of commands. For example, adding numbers sums them up;
adding octet buffers concatenates them into a copy.


## Commands

If no allowed combination for a command is available, a virtual machine
immediately returns to a host with a null pointer instead of a list of registers
of the last basic block executed.

Legend:

- *number* means that both *integer* and *real* are allowed;
- *any* means that anything described in Register value types is allowed.

| Opcode | Command semantic | Output | Input 1 | Input 2 | Input 3 |
| ---: | --- | --- | --- | --- | --- |
| 00 | numeric addition | *number* | a: *number* | b: *number* | ignored |
|    | concatenation | *buffer* | a: *buffer* | b: *buffer* | ignored |
| 01 | arithmetic negation | *number* | x: *number* | ignored | ignored
| 02 | multiplication | *number*  | a: *number* | b: *number* | ignored |
| 03 | division of one | *number* | x: *number* | ignored | ignored |
| 04 | logical NOT | *boolean* | x: *boolean* | ignored | ignored |
|    | bitwise NOT | *integer* | x: *integer* | ignored | ignored |
| 05 | logical AND | *boolean* | a: *boolean* | b: *boolean* | ignored |
|    | bitwise AND | *integer* | a: *integer* | b: *integer* | ignored |
| 06 | logical OR | *boolean* | a: *boolean* | b: *boolean* | ignored |
|    | bitwise OR | *integer* | a: *integer* | b: *integer* | ignored |
| 07 | bitwise exclusive OR | *integer* | a: *integer* | b: *integer* | ignored |
| 08 | type | *integer* | value: *any* | ignored | ignored |
| 09 | count | *integer* | buffer: *buffer* | ignored | ignored | 
| 0a | get map element | any | contaner: *map* | key: *buffer* or *map* | ignored |
|    | get buffer element | any | contaner: *buffer* | type: *integer* | id: *integer* |
| 0b | set map element | *map* | container: *map* | key: *buffer* or *map* | value: *any* |
|    | set buffer element | *buffer* | container: *buffer* | type: *integer* | id: *integer* |
| ff | (continuation) | | | | |
|    | ... set buffer element | *undefined* | value: *any* | ignored | ignored |


## Module stream format

A module starts with a header:

```c
#define DUTYBLASM_MAGIC_1_PLAIN      'D'
#define DUTYBLASM_MAGIC_1_COMPRESSED 'd'
#define DUTYBLASM_MAGIC_2            'T'
#define DUTYBLASM_MAGIC_3            'B'
#define DUTYBLASM_MAGIC_4            'L'

struct dutyblasm_module_header {
	uint8_t magic[4];
	uint8_t placeholder_alignment;

	uint16_t global_basic_block_count;
	uint16_t global_integer_count;
	uint16_t global_real_count;
	uint16_t global_buffer_count;
};
```

Then, an array of `global_basic_block_count` records follows of the following
format:

```c
struct dutyblasm_basic_block_header {
	uint8_t caller_count;
	uint8_t prepopulated_value_count;
	uint8_t calculated_value_count;

	uint8_t exit_branching_condition_value;
	uint8_t exit_branching_true_value;
	uint8_t exit_branching_false_value;
}

```

These fixed length headers are used for instant navigation by basic block ids.

Then, an array of `global_basic_block_count` records follows, one per each
`dutyblasm_basic_block_header` declared above, in the same order:

```c
struct dutyblasm_basic_block_registers {
	uint8_t caller_capture_count;
	uint8_t caller_register_ids[caller_count * caller_capture_count];
	uint8_t captures[prepopulated_value_count];

	uint8_t integer_capture_count;
	uint16_t global_integer_ids[integer_capture_count]; // unaligned

	uint8_t real_capture_count;
	uint16_t global_real_ids[real_capture_count]; // unaligned

	uint8_t buffer_capture_count;
	uint16_t global_buffer_ids[buffer_capture_count]; // unaligned

	uint8_t block_capture_count;
	uint16_t block_captures_count[buffer_capture_count]; // unaligned

	uint8_t generated_map_count;

	struct expression {
		uint8_t opcode;
		uint8_t arg1;
		uint8_t arg2;
		uint8_t arg3;
	} calculated_values[calculated_value_count];
};
```

Each element of `*_ids` arrays followed in declaration order consumes a register
in a basic block like there is a proper command.

Then, global (caplurable) values follow:

```c
struct dutyblasm_buffer {
	uint32_t byte_count;
	char content[byte_count];
}

int32_t global_integer_values[global_integer_count];
double global_real_values[global_real_count];
struct dutyblasm_buffer global_buffer_values[global_buffer_count];
```


# See also

dutyblasm-assembly(5) dutyblasm(1)

# History

Dutyblasm bytecode was initially designed to be ... ECMAScript for Fecer Browser.
However, its features allow 

# Copyright

Copyright 2021 Oleg Iarygin <oleg@arhadthedev.net>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
