#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import re

from utils import parser_log
from datetime import datetime
from common import hlog, config
import shutil

hlog = hlog

ip_emails = {}
old_denied_ips_len = 0
new_denied_ips_len = 0


class RequestData:
    def __init__(self, ip: str, register_time: str, status: str):
        self.ip_address = ip
        self.reg_time = register_time
        self.status = int(status)
        self.fields = {}

    def add_field(self, field_name, field_value):
        self.fields[field_name] = field_value

    def as_str(self):
        output = f"IP地址: {self.ip_address}\n"
        output += f"响应状态码: {self.status}\n"
        output += f"注册时间: {self.reg_time}\n"
        for field_name, field_value in self.fields.items():
            output += f"字段名: {field_name}\n"
            output += f"值: {field_value}\n"
        output += "---\n"
        return output


def analyze_log_files(log_file: str, old_denied_ips: dict) -> dict:
    global ip_emails
    global old_denied_ips_len
    global new_denied_ips_len
    old_denied_ips_len = len(old_denied_ips)
    register_list = []
    ip_counts = {}
    # 存储提取的HTTP请求段
    requests = []
    # 临时存储单个HTTP请求段的行
    request = ''

    parser_log(log_file)

    # 从文件中读取日志内容
    with open('cache/nginx_parse.log', 'r', encoding='UTF-8') as file:
        log_content = file.readlines()

    # 遍历日志内容的每一行
    for line in log_content:
        if line.strip() == '"':
            request += line
            requests.append(request)
            request = ''
        else:
            request += line

    for log in requests:
        # 匹配IP地址
        ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        ip_match = re.search(ip_pattern, log)
        ip_address = ip_match.group(0) if ip_match else None

        # 匹配访问时间
        timestamp_pattern = r'\[\d{2}/[A-Za-z]{3}/\d{4}:\d{2}:\d{2}:\d{2}'
        timestamp_match = re.search(timestamp_pattern, log)
        timestamp = timestamp_match.group(0) if timestamp_match else None
        input_format = "%d/%b/%Y:%H:%M:%S"
        dt = datetime.strptime(timestamp.replace('[', ''), input_format)
        output_format = "%Y-%m-%d %H:%M:%S"
        formatted_reg_time = dt.strftime(output_format)

        # 匹配响应状态码
        status_code_pattern = r'"\s(\d{3})\s'
        status_code_match = re.search(status_code_pattern, log)
        status_code = status_code_match.group(1) if status_code_match else None

        request_data = RequestData(ip_address, formatted_reg_time, status_code)

        # 匹配请求body
        fields = re.findall(r'name="([^"]+)"\s*([\w.@]+)', log)

        # 匹配字段名和对应的值
        for field in fields:
            k, v = field
            request_data.add_field(k, v)

        if request_data.status in [200, 302]:
            register_list.append([request_data.ip_address, request_data.reg_time,
                                  request_data.fields.get('email'),
                                  request_data.fields.get('company'),
                                  request_data.fields.get('address_1'),
                                  request_data.fields.get('address_2'),
                                  request_data.fields.get('city')])

    # 统计IP地址出现次数 统计IP地址注册的邮箱
    for reg in register_list:
        ip_address = reg[0]
        reg_time = reg[1]
        email = reg[2]

        if ip_address in ip_emails:
            ip_emails[ip_address].append((reg_time, email))
        else:
            ip_emails[ip_address] = [(reg_time, email)]

        if ip_address in ip_counts:
            ip_counts[ip_address] += 1
        else:
            ip_counts[ip_address] = 1

    for reg in register_list:
        ip_address = reg[0]
        company = reg[3]
        address_1 = reg[4]
        address_2 = reg[5]
        city = reg[6]

        request_count = ip_counts.get(ip_address)

        if request_count >= 3 and (company == "google" or address_1 == address_2 == city):
            # 统计本次封禁IP的数量
            old_denied_ips[ip_address] = ip_address
    new_denied_ips_len = len(old_denied_ips) - old_denied_ips_len
    return old_denied_ips


def load_denied_ip_auto_conf(file: str) -> dict:
    denied_ips = dict()

    try:
        with open(file, mode='r', encoding='UTF-8') as f:
            lines = f.readlines()
            for line in lines:
                ip = line.strip().split()[1].replace(';', '')
                denied_ips[ip] = ip
    except FileNotFoundError:
        pass

    return denied_ips


def get_emails_from_dict(dictionary: dict, key: str) -> str | list:
    value = dictionary.get(key)
    if value is None:
        return "added"
    else:
        return value


def dump_denied_ip_auto_conf(denied_ips: dict):
    with open(config.denied_ip_auto_conf, mode='w', encoding='UTF-8') as f:
        for k, v in denied_ips.items():
            hlog.info('deny ip->%s %s' % (k, get_emails_from_dict(ip_emails, k)))
            f.write('deny %s;' % k + '\n')


def main():
    nginx_log_file = config.nginx_log_file
    denied_ip_auto_conf = config.denied_ip_auto_conf

    old_denied_ips = load_denied_ip_auto_conf(denied_ip_auto_conf)
    new_denied_ips = analyze_log_files(nginx_log_file, old_denied_ips)

    dump_denied_ip_auto_conf(new_denied_ips)

    hlog.info('The newly IP added number %s' % new_denied_ips_len)

    shutil.rmtree('cache')


if __name__ == '__main__':
    main()
