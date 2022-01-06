#!/usr/bin/env python3
import re
import sys
import json
import html_generator
import s3_push


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


def parse_log(filename="operator.log"):
    '''
    Parse a log file, and return a dictionary of all info
    key = datetime stamp
    value = dictionary of our info
    '''
    log_dict = {}
    with open(filename, 'r') as myfile:
        for line in myfile:
            # TODO FOR JEFF - grep out our info here (done in previous commit)
            line_dict = {"dt": dt,
                         "ip": ip,
                         "aleo_addr": aleo_addr,
                         "block": block}
            log_dict[dt] = line_dict
    return log_dict


def main(filename=None):
    db_dict = load_db()
    log_dict = parse_log(filename)

    # Update db_dict if value not already in it
    for key in log_dict.keys():
        if key not in db_dict.keys():  # meaning it is new
            db_dict[key] = log_dict[key]
    save_db(db_dict)  # so that db can be used later

    # Create html file
    if filename == "operator.log":  # don't create / post a new html if we're ingesting older log files
        html_generator.main()
        s3_push.main()  # requires credentials on the server already e.g. ~/.aws/credentials file


if __name__ == "__main__":
    '''This allows us to add an already used log to our database, or to use the current one by default'''
    filename = "operator.log"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    main(filename)

'''
def main():
    count_dict = {}
    for fn in sorted(glob.glob("operator.log*")):
        pattern = "Operator received a valid share from"
        with open(fn, 'r') as f:
            for line in f:
                if re.search(pattern, line):
                    # result returns list with datetime, ip, miner address, block
                    result = re.findall(
                        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z).*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}).*?\((aleo.*?)\) for block (\d+)", line)
                    # returns just datetimes
                    dt = re.findall(
                        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z)", line)
                    # returns just ips
                    ip = re.findall(
                        r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})", line)
                    # returns just miner addresses
                    aleo_addr = re.findall(r"\((aleo.*?)\)", line)
                    # returns just block
                    block = re.findall(r"for block (\d+)", line)
                    #l_dict = {'dt':dt, 'ip':ip, 'aleo_addr':aleo_addr, 'block':block}
                    if len(result) > 0:
                        res = result[0]
                        if res in count_dict:
                            count_dict[res] = count_dict[res] + 1
                        else:
                            count_dict[res] = 1

    for k, v in count_dict.items():
        # print(k,v)
        with open("sk_db.json", "w") as f:
            json.dump(list(count_dict), f)
'''
