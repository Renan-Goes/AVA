import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import csv
from collections import Counter

def get_data(filename):
    data = {    # dictionary to store the necessary information
        "time": [],
        "src_ip": [],
        "dest_ip": [],
        "ip_to_ip": [], # this will store the specific link between ip's
        "protocol": [],
        "length": []
    }

    with open(filename, 'r') as f:
        reader = csv.reader(f)

        for data_line in reader:    # reads each line and stores the given information
            number, time, source, destination, protocol, length, info = data_line
            data['time'].append(time)
            data['src_ip'].append(source)
            data['dest_ip'].append(destination)
            data['ip_to_ip'].append(source+'->'+destination)
            data['protocol'].append(protocol)
            data['length'].append(length)

    return data

def data_visualization_protocols(data):
    dict_protocols_original = Counter(data['protocol'])
    dict_protocols = {k: v for k, v in dict_protocols_original.items() if v >= 100}
    protocols = []
    num_protocols = []
    
    for protocol in dict_protocols:
        protocols.append(protocol)
        num_protocols.append(dict_protocols[protocol])

    fig1, ax1 = plt.subplots()
    wedges, texts = ax1.pie(num_protocols, startangle=0)
    ax1.legend(wedges, protocols, title='Protocols', loc='center left', bbox_to_anchor=(-0.3, 0.5))
    ax1.set_title("Protocols pie chart:")

    plt.savefig('data/protocols.png')
    
    table = [[protocol, num_protocol] for protocol, num_protocol in zip(protocols, num_protocols)]

    fig2, ax2 = plt.subplots(2,1) 
    ax2[0].axis('tight')
    ax2[0].axis('off')
    table_fig = ax2[0].table(cellText=table, loc='center')
    ax2[1].plot(num_protocols, protocols)

    plt.savefig('data/protocols_table.png')

def data_visualization_volumes(data):
    volume_ip_to_ip = {}

    for ip_to_ip in set(data['ip_to_ip']):
        volume = 0
        for index in range(1, len(data['length'])):
            if data['ip_to_ip'][index] == ip_to_ip:
                volume += float(data['length'][index])
        volume_ip_to_ip[ip_to_ip] = volume
    
    filtered_volume_ip_to_ip = {k: v for k, v in volume_ip_to_ip.items() if v >= 5000000}
    ips = []
    volumes = []
    for ip_to_ip, volume in filtered_volume_ip_to_ip.items():
        ips.append(ip_to_ip)
        volumes.append(volume)
        
    fig = plt.figure(figsize=(25, 15))
    ax = fig.add_subplot(111)
    plt.xticks(rotation=30)
    plt.ylabel("Volume")
    ax.bar(ips, volumes)
    plt.savefig('data/volumes.png')

def data_visualization_volume_in_time_one(data, client_ip, service_ip):
    times_found_download = []
    times_found_upload = []
    sizes_found_download = []
    sizes_found_upload = []

    for index in range(len(data['time'])):
            if data['ip_to_ip'][index] == (client_ip + '->' + service_ip):
                times_found_download.append(int(float(data['time'][index])))
                sizes_found_download.append(int(float(data['length'][index])))

            elif data['ip_to_ip'][index] == (service_ip + '->' + client_ip):
                times_found_upload.append(int(float(data['time'][index])))
                sizes_found_upload.append(int(float(data['length'][index])))

    fig = plt.figure(figsize=(15, 5))
    ax = fig.add_subplot(111)
    plt.ylabel("Volume")
    plt.xlabel("Time")

    plt.plot(times_found_download, sizes_found_download, label='Download')
    plt.plot(times_found_upload, sizes_found_upload, label='Upload')

    plt.legend(title=f'{client_ip} {service_ip}', loc='center', bbox_to_anchor=(0, 0.035))

    plt.savefig('data/flow_rate_specific.png')

    
def data_visualization_volume_in_time_all(data):
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
    plt.ylabel("Volume")
    plt.xlabel("Time")
    
    for ips in dict_ips:
        plt.plot([float(i) for i in dict_ips[ips]['times']], [float(i) for i in dict_ips[ips]['sizes']], label=ips)

    fontP = FontProperties()
    fontP.set_size('xx-small')
    plt.legend(title='Source->Destination', loc='center right', bbox_to_anchor=(1.125, 0.75), prop=fontP)

    plt.savefig('data/flow_rate.png')
    
whatsapp_ip = '157.240.216.60'
discord_ip = '38.113.165.110'
youtube_ip = '185.41.140.16'

data = get_data('capture2.csv')
print('\nData has been read!')
data_visualization_protocols(data)
print('Protocol pie chart generated...')
data_visualization_volumes(data)
print('Total volumes bar chart generated...')
data_visualization_volume_in_time_all(data)
print('Flow rate graph generated...')
data_visualization_volume_in_time_one(data, '192.168.0.112', youtube_ip)
print('Flow rate graph for 1.04.237.167.26, 192.168.0.112 communication...\n')