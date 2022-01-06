#!/usr/bin/env python3
import re
import sys
import json
import html_generator
import s3_push

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
    pattern = "Operator received a valid share from"
    with open(filename, 'r') as myfile:
        for line in myfile:
            if re.search(pattern, line):
                # return just datetimes
                dt = re.findall(
                    r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z)", line)
                # return just ips
                ip = re.findall(
                    r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})", line)
                # return just miner addresses
                aleo_addr = re.findall(r"\((aleo.*?)\)", line)
                # return just block
                block = re.findall(r"for block (\d+)", line)
                
                line_dict = {"dt": dt[0],
                            "ip": ip[0],
                            "aleo_addr": aleo_addr[0],
                            "block": block[0]}
                log_dict['dt'] = line_dict
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
                        

if __name__ == "__main__":
    main()
