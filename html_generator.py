#!/usr/bin/env python3
import sys
import score_keeper
import jinja2
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_ip_based_list(db):
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
        # removing port num for display purposes
        aleo_addr_ip = k.split(":")[0]
        score_list.append((aleo_addr_ip, v['count'], v['aleo_addr']))
    sorted_scores = sorted(score_list, key=lambda ip: ip[1], reverse=True)
    return sorted_scores


def create_aleo_addr_based_list(db_dict):
    pass


def main():
    # load db into dictionary
    db = score_keeper.load_db()
    ip_sorted_list = create_ip_based_list(db)
    # for item in ip_sorted_list:
    #    print(item)

    # call template fn to generate html
    env = Environment(
        # loader=PackageLoader("yourapp"),
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    template = env.get_template("base.html")
    html_file = template.render(vars=ip_sorted_list)
    try:
        outfile = open("leaderboard.html", "w")
        outfile.write(html_file)
        outfile.close()
    except Exception as e:
        print(f"Unable to save html file, {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
