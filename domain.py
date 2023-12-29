#!/usr/bin/env python3
import socket
def get_ip_addresses(domain):
    try:
        # 使用gethostbyname_ex获取域名对应的IP地址列表
        _, _, ip_addresses = socket.gethostbyname_ex(domain)
        return ip_addresses
    except socket.gaierror as e:
        print(f"Error resolving domain: {e}")
        return []

# 示例用法
domain_to_lookup = "stun.parsec.app"
ip_addresses = get_ip_addresses(domain_to_lookup)

print(f"IP Addresses for {domain_to_lookup}: {ip_addresses}")
