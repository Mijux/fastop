#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from datetime import datetime, timedelta
from sys import argv
from requests import post as rpost
from os.path import join
from json import loads, dumps
from multiprocessing import Process
from urllib3.exceptions import InsecureRequestWarning
from requests import packages

from colorama import Fore, Style

packages.urllib3.disable_warnings(category=InsecureRequestWarning)

OP_URL = ""
OP_TIME_ENTRIE = "api/v3/time_entries"

BODY = '{"comment":{"format":"plain","raw":"","html":""},"spentOn":"2024-03-01","hours":"PT1H","customField4":null,"_links":{"workPackage":{"href":"/api/v3/work_packages/"},"activity":{"href":"/api/v3/time_entries/activities/1","title":"Normal"},"self":{"href":null}}}'


def post_activity(
    apikey: str, date: str, nb_hours: int, wp_id: int, verify: bool, comment=""
) -> int:
    url = join(OP_URL, OP_TIME_ENTRIE)
    headers = {"Content-Type": "application/json"}

    body = loads(BODY)

    body["comment"]["raw"] = comment
    body["spentOn"] = date
    body["hours"] = f"PT{nb_hours}H"
    body["_links"]["workPackage"]["href"] = f"/api/v3/work_packages/{wp_id}"

    res = rpost(
        url=url,
        headers=headers,
        data=dumps(body),
        auth=("apikey", apikey),
        verify=verify,
    )

    if res.status_code <= 299 and res.status_code >= 200:
        print(
            f" - {Fore.GREEN}L'activité a bien été ajoutée{Style.RESET_ALL} au {date} pour le workpackage {wp_id} pour {nb_hours} "
        )
    else:
        print(f"{Fore.RED}Aie aie aie petite erreur{Style.RESET_ALL}")
        with open("./logerreur", "w") as errfile:
            errfile.write(str(res.content))


def arg_parser() -> Namespace:
    parser = ArgumentParser(description="FASTOP - Fill your openproject faster")

    parser.add_argument(
        "--host",
        type=str,
        help="Your openproject hostname. ex: openproject.example.com",
        required=True,
    )

    parser.add_argument(
        "--api",
        type=str,
        help="Your openproject api key",
        required=True,
    )

    action_to_perform = parser.add_mutually_exclusive_group(required=True)
    action_to_perform.add_argument(
        "-d",
        "--date",
        type=str,
        help="Date of your activity in the following format year-month-day. ex: -d 2024-01-25",
    )
    action_to_perform.add_argument(
        "-r",
        "--date-range",
        nargs=2,
        type=str,
        help="Your range of activity in the following format year-month-day year-month-day. ex: -r year-month-day year-month-day",
    )

    parser.add_argument(
        "-k",
        "--verify",
        action="store_true",
        help="If you don't want to verify ssl certificat",
    )

    parser.add_argument(
        "-wp",
        "--workpackage-id",
        nargs="+",
        type=int,
        help="Your workpages ID. ex: -wp 4 or -wp 5 4 2",
        required=True,
    )

    parser.add_argument(
        "-c",
        "--comment",
        nargs="+",
        type=str,
        help='Comments on your activity. ex: -c "Working on xxx"',
        required=False,
    )

    parser.add_argument(
        "-hs",
        "--hours",
        nargs="+",
        type=float,
        help="How many hours on your activity. ex: -hs 7 or -hs 7 7 6",
        required=True,
    )

    return parser.parse_args(argv[1:])


if __name__ == "__main__":

    print(
        f"""{Fore.BLUE}_____________________________________________ 
___  ____/__    |_  ___/__  __/_  __ \__  __ \\
__  /_   __  /| |____ \__  /  _  / / /_  /_/ /
_  __/   _  ___ |___/ /_  /   / /_/ /_  ____/ 
/_/      /_/  |_/____/ /_/    \____/ /_/      v0.1{Style.RESET_ALL}
             """
    )

    parsed_arg = arg_parser()
    OP_URL = (
        parsed_arg.host
        if (
            parsed_arg.host.startswith("https://")
            or parsed_arg.host.startswith("http://")
        )
        else f"https://{parsed_arg.host}"
    )
    # print(parsed_arg)

    if parsed_arg.date_range is None:
        post_activity(
            apikey=parsed_arg.api,
            date=parsed_arg.date,
            nb_hours=parsed_arg.hours[0],
            wp_id=parsed_arg.workpackage_id[0],
            verify=False if parsed_arg.verify else True,
            comment=parsed_arg.comment[0] if parsed_arg.comment is not None else None,
        )
    else:
        starting_date = datetime.strptime(parsed_arg.date_range[0], "%Y-%m-%d")
        ending_date = datetime.strptime(parsed_arg.date_range[1], "%Y-%m-%d")

        all_process: list[Process] = []

        current_date = starting_date
        index = 0
        while current_date <= ending_date:
            if current_date.weekday() < 5:

                nb_hours = (
                    parsed_arg.hours[index]
                    if len(parsed_arg.hours) > 1
                    else parsed_arg.hours[0]
                )

                wp_id = (
                    parsed_arg.workpackage_id[index]
                    if len(parsed_arg.workpackage_id) > 1
                    else parsed_arg.workpackage_id[0]
                )

                if parsed_arg.comment is None:
                    comment = None
                else:
                    comment = (
                        parsed_arg.comment[index]
                        if len(parsed_arg.comment) > 1
                        else parsed_arg.comment[0]
                    )

                verify = False if parsed_arg.verify else True

                p = Process(
                    target=post_activity,
                    args=(
                        parsed_arg.api,
                        current_date.strftime("%Y-%m-%d"),
                        nb_hours,
                        wp_id,
                        verify,
                        comment,
                    ),
                )
                p.start()

                all_process.append(p)
                index += 1

            current_date += timedelta(days=1)

        for p in all_process:
            p.join()
