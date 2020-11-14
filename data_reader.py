import matplotlib.pyplot as plt
import csv
from collections import Counter

def get_data(filename):
    data = {
        "number": [],
        "time": [],
        "src_ip": [],
        "dest_ip": [],
        "ip_to_ip": [],
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
            data['ip_to_ip'].append(source+'->'+destination)
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
    ax1 = fig1.add_subplot(111)
    ax1.bar(src_ips, num_src_ips)
    plt.savefig('source_ips.png')

    fig2 = plt.figure(figsize=(15, 5))
    ax2 = fig2.add_subplot(111)
    ax2.bar(dest_ips, num_dest_ips)
    plt.savefig('destination_ips.png')

def data_visualization_flow_rate_one(data, user_ip, service_ip):
    times_found_download = []
    times_found_upload = []
    sizes_found_download = []
    sizes_found_upload = []

    for index in range(len(data['time'])):
            if data['ip_to_ip'][index] == (user_ip + '->' + service_ip):
                times_found_download.append(int(float(data['time'][index])))
                sizes_found_download.append(int(float(data['length'][index])))

            elif data['ip_to_ip'][index] == (service_ip + '->' + user_ip):
                times_found_upload.append(int(float(data['time'][index])))
                sizes_found_upload.append(int(float(data['length'][index])))

    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)

    plt.plot(times_found_download, sizes_found_download, label='Download')
    plt.plot(times_found_upload, sizes_found_upload, label='Upload')

    plt.legend(loc='center', bbox_to_anchor=(-0.1, 0.4))

    plt.savefig('flow_rate_specific.png')

    
def data_visualization_flow_rate_all(data):
    dict_ip_to_ip_original = Counter(data['ip_to_ip'])
    dict_ip_to_ip = {k: v for k, v in dict_ip_to_ip_original.items() if v >= 100}
    
    dict_ips = {}

    for ips in dict_ip_to_ip:
        times_found = []
        sizes_found = []
        for index in range(len(data['time'])):
            if data['ip_to_ip'][index] == ips:
                times_found.append(data['time'][index])
                sizes_found.append(data['length'][index])
        dict_ips[ips] = {
            'times': times_found,
            'sizes': sizes_found
        }
        
    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)
    
    for ips in dict_ips:
        plt.plot([int(float(i)) for i in dict_ips[ips]['times']], [int(float(i)) for i in dict_ips[ips]['sizes']], label=ips)

    plt.legend(title='Packets', loc='center right', bbox_to_anchor=(0.1, 0.2))

    plt.savefig('flow_rate.png')
    
data = get_data('capture.csv')
print('\nData has been read!')
data_visualization_protocols(data)
print('Protocol pie chart generated...')
data_visualization_server_client(data)
print('Server and client bar chart generated...')
data_visualization_flow_rate_all(data)
print('Flow rate graph generated...')
data_visualization_flow_rate_one(data, '104.237.167.26', '192.168.0.112')
print('Flow rate graph for specific ip\'s generated...\n')