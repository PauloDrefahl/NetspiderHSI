## Disclaimer

Netspider is a school project developed as part of a senior capstone course at Florida Gulf Coast University (FGCU), created in partnership with the HSI Fort Myers office.

This is an open-source educational tool, freely available for anyone to use, study, or build upon. It does not carry any security clearance, official certification, or endorsement, and it has no direct affiliation, partnership, or relationship with any government agency or institution other than FGCU.

Any mentions of government agencies refer strictly to the academic collaboration context of this capstone project and do not imply ongoing institutional support, sponsorship, or operational deployment by any agency.

Use of this software is at the user's own discretion and risk. The authors make no warranties regarding its fitness for any particular purpose, including investigative or law enforcement use.


# Netspider: Web Scraping Tool
NetSpider is a web scraping tool developed by students from FGCU – Florida Gulf Coast University as part of their senior capstone course requirements. The tool is designed to assist in scraping the internet for signs of suspicious or harmful activity by automating the collection of data from various websites. This open-source tool helps community members, researchers, and investigators extract relevant information and save it for later analysis — making it easier to track patterns and gather leads.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)


## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How to Use](#how-to-use)
- [Troubleshooting](#troubleshooting)
- [Evolution of Netspider](#evolution-of-netspider)
- [Future Development](#future-development)
- [Contributions](#contributions)
- [Team](#team)
- [Sponsors and Mentors](#sponsors-and-mentors)
- [License](#license)
- [Disclaimer](#disclaimer)

## Overview

Netspider allows users to navigate through complex web structures, extract data based on keywords, and automatically capture screenshots. The scraped data is organized into folders named after the website and the time/date the scrape was run. In addition to saving the data as .png and .xlsx files, Netspider compiles the screenshots into a .pdf to simplify reviewing for investigators.

## Key Features

- **Web scraping for evidence collection**: Automatically scrape relevant websites based on custom keywords or keysets.
- **Data storage**: Organizes scraped data (screenshots, text, emails, phone numbers, etc.) in a structured folder system.
- **Keyword customization**: Investigators can add or remove keywords and keysets for tailored searches.
- **Multi-format outputs**: Data can be saved as .png, .xlsx, and compiled into a .pdf.
- **Supported websites**: Escort Alligator, Eros, Megapersonals, Skip the Game, Rub Ratings, YesBackpage.

## Requirements

- Python 3.8 or higher
- Internet connection
- Sufficient storage space for scraped data

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/PauloDrefahl/NetspiderHSI.git
   ```

2. Navigate to the project directory:
   ```bash
   cd netspider
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. In Client Directory, enter:
   ```bash
    npm init
    ```

6. install electron in client:
    ```bash
    npm install --save-dev electron
    ```


## Usage

Start the Client without the main Executable script:
1. In the Client Directory, in the terminal enter:
    ```bash
    npm start
    ```

2. Then run app.py in server directory to start the backend.
3. Input the port shown in consol into both open_ports.txt files.
4. rerun app.py



Start the scraper by running the main script:

  ```bash
  python netspider.py
  ```

Follow the prompts in the UI to configure your keyword sets and begin scraping.

## How to Use

1. **Start**: Select the desired keywords or keysets and start the scraper process by clicking "Start Scraper."
2. **Login**: Log in with your authorized username and password.
3. **Configure**: Upload custom keywords or keysets, or use the default provided by the tool.
4. **Run Scraper**: The tool will start extracting information and save the results in the designated folder.
5. **Analyze**: To view the results, navigate to the "Open Results Folder" and select the relevant scrape to see the data collected.

## Security Considerations
- This is an open source software and FGCU is not responsible for its use.
- Always use Netspider on a secure, isolated network.
- Regularly update the tool and its dependencies to ensure you have the latest security patches.
- Use strong, unique passwords for authentication.
- Be cautious when handling sensitive data extracted by the tool.

## Troubleshooting

- **Issue**: Scraper fails to start
  **Solution**: Ensure all dependencies are correctly installed and you're using a compatible Python version.

- **Issue**: Unable to access certain websites
  **Solution**: Check your internet connection and verify that the target website is operational.

- For more issues, please check our [FAQ](link-to-faq) or open an issue on GitHub.

## Evolution of Netspider

- **Netspider 1v (September 2023)**: Initial release with basic scraping and file selection functionality.
- **Netspider 3v (February 2024)**: Expanded feature set, including improved keyword search and multi-format outputs.

## Future Development

- Integration with machine learning models for advanced data analysis
- Support for additional websites and data sources
- Enhanced reporting capabilities

## Contributions

Contributions to the project are welcome! If you would like to suggest a feature or fix an issue:

1. Fork the repository.
2. Create a new branch for your changes.
3. Commit your changes and open a pull request.

Please read our [Contributing Guidelines](link-to-contributing-guidelines) for more information.

## Students on the Netspider 23-24 Team

* **Paulo Drefahl** - Full Stack Developer
* **Zach Sutton** - Full Stack Developer
* **Kevin Kostage** - Full Stack Developer
* **Alyssa Chiego** - Frontend Developer
* **Greg Bateham** - Frontend Developer
* **Corey Record** - Backend Developer
* **Dylan Garcia** - Frontend Developer

## Students on the Netspider 24-25 Team

* **William Murphy** - Full Stack Developer
* **Caleb Newman** - Full Stack Developer
* **William Ward** - Full Stack Developer
* **Daniel Kareh** - Backend Developer

## Students on the Netspider 25-26 Team
* **Aaron Cole** - Full Stack and Backend Developer
* **Martin Patterson** - Full Stack and Backend Developer

## Sponsors and Mentors

* **Sponsor**: Clinton Thompson
* **Mentor**: Dr. Fernando Gonzalez

## 25-26 Sponsors and Mentors
* **Sponsor**: Dave Loerzel
* **Mentor**: Dr. Fernando Gonzalez

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
