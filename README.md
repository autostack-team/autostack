![Logo](https://raw.githubusercontent.com/autostack-team/autostack/develop/Logo.png)

<p align="center">
    <a href="https://travis-ci.com/autostack-team/autostack/">
        <img src="https://travis-ci.com/autostack-team/autostack.svg?branch=master"
            alt="Build status"/>
    </a>
    <a href="https://codeclimate.com/github/autostack-team/autostack/test_coverage">
        <img src="https://api.codeclimate.com/v1/badges/4dc7775be0fef62e5492/test_coverage" 
            alt="Code coverage"/>
    </a>
    <a href="https://codeclimate.com/github/autostack-team/autostack/maintainability">
        <img src="https://api.codeclimate.com/v1/badges/4dc7775be0fef62e5492/maintainability" 
            alt="Maintainability"/>
    </a>
    <a href="https://github.com/autostack-team/autostack">
        <img src="https://img.shields.io/github/commit-activity/m/autostack-team/autostack"
            alt="GitHub commit activity"/>
    </a>
    <a href="https://pypi.org/project/autostack/">
        <img src="https://img.shields.io/pypi/dm/autostack"
             alt="PyPI - Downloads"/>
    </a>
    <a href="https://pypi.org/project/autostack/">
        <img src="https://img.shields.io/pypi/v/autostack"
             alt="PyPI"/>
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-orange.svg"
             alt="License"/>
    </a>
    <a href="https://teams.microsoft.com/join/1oa3o6vva07n">
        <img src="https://img.shields.io/badge/Chat-MSTeams-orange.svg"
             alt="Chat"/>
    </a>
    <a href="https://twitter.com/intent/follow?screen_name=autostackteam">
        <img src="https://img.shields.io/twitter/follow/autostackteam.svg?style=social&logo=twitter"
             alt="Follow on Twitter"/>
    </a>
    <a href="https://www.patreon.com/autostack">
        <img src="https://img.shields.io/badge/Support-Patreon-red?logo=patreon"
             alt="Support on Patreon"/>
    </a>
    <a href="https://instagram.com/retractablebearfist?igshid=7qlm4fol0o50">
        <img src="https://img.shields.io/badge/logo%20by-RBF-purple?logo=instagram"
             alt="Logo designer's instagram"/>
    </a>
</p>

autostack is a command-line debugging tool for Python projects that automatically displays Stack Overflow answers for thrown errors.

What is the first thing you do when a confusing error message is displayed in your terminal window? You search for an answer on Stack Overflow, of course! With autostack, you no longer have to search for answers on Stack Overflow, they are found for you. Gone are the days of scowering the internet for hours to find an answer to your development questions! autostack is here to automate the debugging process and in turn, expedite Python project development.

## Table of Contents

* [Installation](#Installation)
* [Usage](#Usage)
* [Contributing](#Contributing)
* [License](#License)
* [Authors](#Authors)

## Installation

**1. Clone the repo and use the install script.**

Clone the repo.
```sh
git clone https://github.com/autostack-team/autostack.git
```

Navigate to the project directory, and run the install bash script.
```sh
cd /path/to/project/
chmod +x install.sh
./install.sh 
```

**2. Or just use pip to install.**

```sh
pip3 install autostack
```

## Usage 

In one terminal window, execute the autostack command to listen for errors.
```sh
autostack
```

In another terminal window, execute autostack-termal which will inform the autostack listener to listen for errors in the terminal.
```sh
autostack-terminal
``` 

To stop running autostack, use the exit command in the autostack-terminal windows. This automatically stops the terminal window listening for errors.
```sh
exit
```

## Contributing

For information on how to get started contributing to autostack, see the [contributing guidlines](https://github.com/autostack-team/autostack/blob/master/CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors
* [Elijah Sawyers](https://github.com/elijahsawyers)
* [Benjamin Sanders](https://github.com/BenOSanders)
* [Caleb Werth](https://github.com/cwerth1)
