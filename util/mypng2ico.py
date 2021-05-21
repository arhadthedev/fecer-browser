#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Pack a PNG image into an ICO container in specified size variants.

NOTE: This is NOT png2ico by Matthias S. Benkmann; it just follows intuitive
"{input}2{output}" naming convention.
"""

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

from argparse import ArgumentParser, FileType

from PIL import Image


def process_image(in_stream, out_stream, color_count, sizes):
    """Reduce colors and save an image as an ICO image set.

    Args:
        in_stream: A stream with input content of a PNG image.
        out_stream: A stream for output content of an ICO image set.
        color_count: How many colors reduce an image to.
        sizes: A list of resized square variants put into an output.

    """
    original = Image.open(in_stream)
    paletted = original.quantize(colors=color_count, dither=Image.NONE)
    paletted.save(out_stream, format='ICO', sizes=[(wh, wh) for wh in sizes])


def get_arguments():
    """Parse command line into a dict of arguments; abort on `-h`.

    Returns:
        a dict `{'infile': <stream>, 'outfile': <stream>, 'colors': <int>,
        'add_size': [<int>, ...], custom_size_only: <bool>}`

    """
    about = 'Convert a PNG image into an ICO with multiple sizes'
    note = 'NOTE: This is NOT `png2ico` by Matthias S. Benkmann'
    parser = ArgumentParser(description=about, epilog=note)

    parser.add_argument('infile', type=FileType('rb'), help='path to a .png')
    parser.add_argument('outfile', type=FileType('wb'), help='path to an .ico')
    parser.add_argument('colors', type=int, help='palette color count')

    parser.add_argument(
        '--add_size',
        type=int,
        metavar='N',
        action='append',
        help='generate a custom NxN icon size into an output',
    )
    parser.add_argument(
        '--custom_size_only',
        action='store_true',
        help='do not use default sizes 16, 32, 48, and 256px',
    )

    return parser.parse_args()


args = get_arguments()

sizes = [] if args.custom_size_only else [16, 32, 48, 256]
sizes += args.add_size or []

process_image(args.infile, args.outfile, args.colors, sizes)
