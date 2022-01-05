#!/usr/bin/env python3
import score_keeper
import jinja2


def create_ip_based_list(db_dict):
    pass


def create_aleo_addr_based_list(db_dict):
    pass


def main():
    # load db into dictionary
    db = score_keeper.load_db()
    # create ip descending list of block counts
    count_dict = {}  # {'x.x.x.x' : {'count': NUM, 'aleo_addr': 'aleo1XYZZZZ' }  }
    score_list = []
    for k, v in db.items():
        ip = v['ip']
        aleo_addr = v['aleo_addr']
        # print(f"IP: {ip}")
        if ip not in count_dict.keys():
            count_dict[ip] = {'count': 1, "aleo_addr": aleo_addr}
        else:
            curr_count_item = count_dict[ip]
            count = curr_count_item['count']
            count += 1
            curr_count_item['count'] = count
            count_dict[ip] = curr_count_item
    # create aleo addr descending list of block counts
    for k, v in count_dict.items():
        score_list.append((k, v['count'], v['aleo_addr']))
    sorted_scores = sorted(score_list, key=lambda ip: ip[1], reverse=True)
    for item in sorted_scores:
        print(item)

    # call template fn to generate html
    # save html file


if __name__ == "__main__":
    main()
