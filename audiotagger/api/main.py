# !/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
import os
import sys

import customlogging as cl
from audiotagger.core.generate_config import generate_config
from audiotagger.core.paths import audiotagger_config_path


def get_options():
    parser = optparse.OptionParser()
    parser.add_option(
        "-s",
        action="store",
        dest="src",
        help="Source directory or path for all audio files."
    )

    parser.add_option(
        "-x",
        action="store_true",
        dest="write_to_excel",
        help="Write metadata to Excel."
    )

    parser.add_option(
        "-t",
        "--tag_file",
        action="store_true",
        dest="tag_file",
        help="A .xlsx metadata file containing tags and the audio file "
             "paths of the files associated ."
    )

    parser.add_option(
        "-m",
        "--modifier",
        action="store",
        dest="modifier",
        help="Modifiers to apply to metadata."
    )

    parser.add_option(
        "-l",
        action="store",
        dest="log_dir",
        help="Set log directory."
    )

    parser.add_option(
        "-c",
        "--clear_tags",
        action="store",
        dest="clear_tags",
        help="Clears the tags for a given directory. ('all' clears all "
             "tags and 'excess' clears all tags not in desired base metadata)"
    )

    parser.add_option(
        "--cp",
        "--copy_file",
        action="store_true",
        dest="copy_file",
        help="Copies the audio file from the source path to destination path."
    )

    parser.add_option(
        "-d",
        "--dst",
        action="store",
        dest="dst",
        help="Base destination directory for file output (e.g. from "
             "file renaming or playlist generation."
    )

    parser.add_option(
        "-w",
        "--write_to_file",
        action="store_true",
        dest="write_to_file",
        help="Commit changes to audio file."
    )

    parser.add_option(
        "--generate-config",
        action="store_true",
        dest="generate_config",
        help="Create configuration file for the application."
    )

    parser.add_option(
        "--create-playlist",
        action="store",
        dest="playlist_query",
        help="Creates a playlist from the given query on the source."
    )

    parser.add_option(
        "--generate-metadata-template",
        action="store_true",
        dest="generate_metadata_template",
        help="Generates a .xlsx metadata template file."
    )

    return parser


if __name__ == "__main__":
    parser = get_options()
    options, args = parser.parse_args()

    # If the app was never configured, generate configuration once.
    if not os.path.exists(audiotagger_config_path()):
        print("Application will configure for the first time...")
        generate_config()
        sys.exit(0)

    # Reset app configurations.
    if options.generate_config:
        generate_config()
        sys.exit(0)

    # Generate metadata Excel template.
    if options.generate_metadata_template:
        from audiotagger.core.generate_metadata_template import \
            generate_metadata_template

        generate_metadata_template(dst_dir=options.dst)
        sys.exit(0)

    # RUN MAIN PROGRAM HERE.
    from audiotagger.api.api import AudioTaggerAPI

    # Set up logging.
    if options.log_dir is not None:
        log_dir = options.log_dir
    else:
        from audiotagger.settings.settings import LOG_DIRECTORY

        log_dir = LOG_DIRECTORY
    logger = cl.initialize_logger(log_dir=log_dir, name="audiotagger.log")
    logger.info(options)

    at = AudioTaggerAPI(logger=logger, options=options)
    at.run()
    logger.info("Done.")
