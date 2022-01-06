#!/usr/bin/env python3
import re
import json
import glob


# TODO:  Use some sort of cli argument passing library to support  (docopt / argparse and etc)
# -f input file (optional file name)
# -h html file (true/false)
# -s3 bucket name to push to (optional name)
DB_FILE = "sk_db.json"

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
    count_dict = {}
    for fn in sorted(glob.glob("operator.log*")):
        pattern = "Operator received a valid share from"
        with open(fn, 'r') as f:
            for line in f:
                if re.search(pattern, line):
                    #result returns list with datetime, ip, miner address, block
                    result = re.findall(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}).*?\((aleo.*?)\) for block (\d+)", line)
                    #returns just datetimes
                    dt = re.findall(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z)", line)
                    #returns just ips
                    ip = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})", line)
                    #returns just miner addresses
                    aleo_addr = re.findall(r"\((aleo.*?)\)", line)
                    #returns just block
                    block = re.findall(r"for block (\d+)", line)
                    #l_dict = {'dt':dt, 'ip':ip, 'aleo_addr':aleo_addr, 'block':block}
                    if len(result) > 0:
                        res = result[0]
                        if res in count_dict:
                            count_dict[res] = count_dict[res] + 1
                        else:
                            count_dict[res] = 1
        f.close()
                            
    for k, v in count_dict.items():
        #print(k,v)
        with open("sk_db.json", "w") as f:
            json.dump(list(count_dict.items()), f)
        f.close()
          
                        


if __name__ == "__main__":
    main()
