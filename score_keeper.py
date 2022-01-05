import re
from collections import Counter

#reads continuously running "operator.log" file and counts the number of times each ip address appears with "Operator received a valid share from IP"
#prints "<ip> : <count>" in descending order and gives the total count of all ips at the end.
count_dict = {}

with open('operator.log', 'r') as f:
    for line in f:
        matches = re.findall(r"valid share from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
        if len(matches) > 0:
            ip = matches[0]
            if ip in count_dict:
                count_dict[ip] = count_dict[ip] + 1
            else:
                count_dict[ip] = 1

result_list = []
for key in count_dict:
    result_list.append({ 'ip': key, 'count': count_dict[key]})

def comparator(item):
    return item['count']

result_list.sort(key=comparator, reverse=True)

total = 0
for item in result_list:
    total += item['count']
    print(f"{item['ip']}: {item['count']}")

print(f"Total: {total}")
