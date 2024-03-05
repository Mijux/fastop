<br/>
<p align="center">
  <a href="https://github.com/Mijux/fastop">
    <img src="https://cdn-icons-png.flaticon.com/512/1740/1740222.png" alt="Logo" width="125" height="125">
  </a>

  <h3 align="center">FastOP</h3>

  <p align="center">
    Short script to add time entries to your open project. This saves you having to repeat the same clicks over and over again
    <br/>
    <br/>
    <a href="https://github.com/Mijux/fastop/issues">Report Bug</a>
    .
    <a href="https://github.com/Mijux/fastop/issues">Request Feature</a>
  </p>
</p>

![Contributors](https://img.shields.io/github/contributors/Mijux/fastop?color=dark-green) ![Issues](https://img.shields.io/github/issues/Mijux/fastop) ![License](https://img.shields.io/github/license/Mijux/fastop) 

## About The Project

Open Project is a software package that allows you to allocate hours. It can be used for project management, for example. But when you have to allocate the same things, you have no choice but to do everything manually.

That's why I've developed this little script that makes it easy to add up your hours, by day or by week.

## Built With



* [Python 🐍](https://www.python.org/)

## Getting Started

You will find the steps to setup the project

### Prerequisites

You need python3 and the following dependencies:
- requests
- colorama

```bash
python3 -m pip install -r requirements.txt
```


### Installation

1. Clone the repo

```bash
git clone https://github.com/Mijux/fastop.git
```

2. Install dependencies

```sh
python3 -m pip install -r requirements.txt
```

4. Enter your API in `config.js`

That's all ! ✨

## Usage

```bash
python3 main.py [-h] --host HOST --api API (-d DATE | -r DATE_RANGE DATE_RANGE) [-k] -wp WORKPACKAGE_ID [WORKPACKAGE_ID ...] [-c COMMENT [COMMENT ...]] -hs HOURS [HOURS ...]
```

There are several options:

| option name | required | description | example |
| -------------- | --------- | ------------ | ---------- |
| -h / --help    | False       | Display the help |  |
| --host           | True        |  Your open project instance | --host openproject.example.org |
| --api             | True        | Your open project api key | --api <key> |
| -d / --date | True | The date of your time entrie - date format: year-month-day | -d 2024-03-21 |
| -r / --date-range | True | The range of days of your time entries | -r 2024-03-21 2024-04-05 |
| -k / --verify | False | If you don't want to check the TLS certificate | |
| -wp / --workpackage-id | True |  ID of your workpackage | -wp 4 |
| -hs / --hours | True | Number of hours in day on your activities | -hs 7 |
| -c / --comment | False | Comment on your activitie | -c "Write the Readme" |

Options -d and -r are required but exclusive i.e. it is either -d either -r, not both. When you use the option -r you have two choices.
1. Just put one value
2. Put one value per day, for that just add values after anothers: -hs 7 7 8

Below some examples:

1. This will add the workpackage 2 on 1 January 2024 for 9 hours with a comment.
```bash
python3 main.py --host <host> --api <apikey> -d 2024-01-01 -wp 2 -hs 9 -c "Sleeping"
```

2. This will add the workpackage 2 from 1 January 2024 to 4 January 2024 for 9 hours per day with a comment. 
```bash
python3 main.py --host <host> --api <apikey> -r 2024-01-01 2024-01-04 -wp 2 -hs 9 -c "Sleeping"
```

3. This will add workpackage 2 from 1 January 2024 to 2 January 2024 for 9 and 8 hours per day then workpackage 4 on the 3 January 2024 for 8 hours and finally the workpackage 5 on the 4 January 2024 for 2 hours. In this example, all time entries has an unique comment.
```bash
python3 main.py --host <host> --api <apikey> -r 2024-01-01 2024-01-04 -wp 2 2 4 5 -hs 9 8 8 2 -c "Comm 1" "Comm 2" "Comm 3" "Comm 4"
```

4. Like above but 9 hours each days and no comment
```bash
python3 main.py --host <host> --api <apikey> -r 2024-01-01 2024-01-04 -wp 2 2 4 5 -hs 9 
```

**WARNING**: Pay attention on the data you provide to the script. There is not any verification on data provided and there is not rollback on your action.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/Mijux/fastop/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/Mijux/fastop/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/Mijux/fastop/blob/main/LICENSE.md) for more information.

## Authors

* **Mijux** - *Cybersec* - [Mijux](https://github.com/Mijux/) - *Maintainer*

## Acknowledgements

* [ImgShields](https://shields.io/)
