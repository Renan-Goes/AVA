import matplotlib.pyplot as plt
import csv
from collections import Counter
import pandas as pd

def get_data(filename):
    data = {
        "number": [],
        "time": [],
        "src_ip": [],
        "dest_ip": [],
        "ip_to_ip": {
            'ips': [],
            'time_found': []
        },
        "protocol": [],
        "length": [],
        "info": []
    }

    with open(filename, 'r') as f:
        reader = csv.reader(f)

        for data_line in reader:
            number, time, source, destination, protocol, length, info = data_line
            data['number'].append(number)
            data['time'].append(time)
            data['src_ip'].append(source)
            data['dest_ip'].append(destination)
            data['ip_to_ip']['ips'].append(source+'->'+destination)
            data['ip_to_ip']['time_found'].append(time)
            data['protocol'].append(protocol)
            data['length'].append(length)
            data['info'].append(info)

    return data

def data_visualization_protocols(data):
    dict_protocols = Counter(data['protocol'])
    protocols = []
    num_protocols = []
    
    for protocol in dict_protocols:
        protocols.append(protocol)
        num_protocols.append(dict_protocols[protocol])

    fig1, ax1 = plt.subplots()
    wedges, texts = ax1.pie(num_protocols, startangle=0)
    ax1.legend(wedges, protocols, title='Protocols', loc='center left', bbox_to_anchor=(-0.3, 0.5))
    ax1.set_title("Protocols pie chart:")

    plt.savefig('protocols.png')

def data_visualization_server_client(data):
    dict_src_original = Counter(data['src_ip'])
    dict_dest_original = Counter(data['dest_ip'])
    dict_src = {k: v for k, v in dict_src_original.items() if v >= 100}
    dict_dest = {k: v for k, v in dict_dest_original.items() if v >= 100}
    src_ips = []
    dest_ips = []
    num_src_ips = []
    num_dest_ips = []

    for src_ip, dest_ip in zip(dict_src, dict_dest):
        src_ips.append(src_ip)
        num_src_ips.append(dict_src[src_ip])
        dest_ips.append(dest_ip)
        num_dest_ips.append(dict_dest[dest_ip])

    fig1 = plt.figure(figsize=(15, 5))
    ax1 = fig1.add_axes([0,0,1,1])
    ax1 = fig1.add_subplot(111)
    ax1.bar(src_ips, num_src_ips)
    plt.savefig('source_ips.png')

    fig2 = plt.figure(figsize=(15, 5))
    ax2 = fig2.add_axes([0,0,1,1])
    ax2 = fig2.add_subplot(111)
    ax2.bar(dest_ips, num_dest_ips)
    plt.savefig('destination_ips.png')

def data_visualization_flow_rate(data):
    dict_ips_original = Counter(data['ip_to_ip']['ips'])
    dict_ips = {k: v for k, v in dict_ips_original.items() if v >= 100}
    
    for ips in dict_ips:
        print(f'___\n{data["ip_to_ip"][ips]}')

    
data = get_data('capture.csv')
data_visualization_protocols(data)
data_visualization_server_client(data)
data_visualization_flow_rate(data)