#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
from urllib.parse import unquote
from pathlib import Path
import shutil


def read_nginx_post_log(nginx_log: str):
    search_string = "/index.php?route=account/register"
    with open(nginx_log, mode='r', encoding='UTF-8') as f, open('tmp/nginx_decode.log', mode='w',
                                                                encoding='UTF-8') as f2:
        lines = f.readlines()
        for line in lines:
            if search_string in line:
                f2.write(line.replace("\\x", "%"))


def decode_nginx_post_log() -> None:
    with open('tmp/decode_post.log', mode='w', encoding='UTF-8') as f, open('tmp/nginx_decode.log', mode='r',
                                                                            encoding='UTF-8') as f2:
        decode_data = unquote(f2.read())
        f.write(decode_data)


def remove_log_blank_line(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='UTF-8') as file_in, open(output_file, 'w', encoding='UTF-8') as file_out:
        for line in file_in:
            if line.strip():
                file_out.write(line)


def parser_log(nginx_log: str):
    my_file = Path("tmp")
    if my_file.is_dir():
        shutil.rmtree(my_file)
        my_file.mkdir()
    else:
        my_file.mkdir()
    read_nginx_post_log(nginx_log)
    decode_nginx_post_log()
    remove_log_blank_line('tmp/decode_post.log', 'tmp/nginx_parse.log')
