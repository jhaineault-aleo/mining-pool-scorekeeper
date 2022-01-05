#!/usr/bin/env python3
import re
import json

# TODO:  Use some sort of cli argument passing library to support  (docopt / argparse and etc)
# -f input file (optional file name)
# -h html file (true/false)
# -s3 bucket name to push to (optional name)


DB_FILE = "sk_db.json"
# reads continuously running "operator.log" file and counts the number of times each ip address appears with "Operator received a valid share from IP"
# prints "<ip> : <count>" in descending order and gives the total count of all ips at the end.

# Press Enter to run on current "operator.log" or enter ".<number>" of any previous "operator.log" files to get previous scores.


# datetime = re.findall(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", line)
# ip = re.findall(r"valid share from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
# miner_address = re.findall(r"\(.*?\)", line)
# block = re.findall(r"for block (\d+)", line)

def load_db(filename=DB_FILE):
    data = {}
    try:
        f = open(filename)
        data = json.load(f)
    except Exception as e:
        #print(f"Can't read db file, will use empty dictionary. {e}")
        pass
    return data


def save_db(db_dict):
    with open(DB_FILE, "w") as outfile:
        json.dump(db_dict, outfile)
    return


def main():
    '''Creates mining pool db, html file of results, pushes to S3 bucket'''
    count_dict = {}
    filename = input("Enter operator.log number: ")
    with open('operator.log' + filename, 'r') as f:
        for line in f:
            matches = re.findall(
                r"valid share from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
            if len(matches) > 0:
                ip = matches[0]
                if ip in count_dict:
                    count_dict[ip] = count_dict[ip] + 1
                else:
                    count_dict[ip] = 1


if __name__ == "__main__":
    main()
