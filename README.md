# Netspider: Web Scraping Tool for Cybercrime Investigation
NetSpider is a web scraping tool designed to assist in the investigation of cybercrimes by automating the process of data collection from various websites. The tool helps investigators by extracting relevant information and saving it for later analysis, making it easier to track and gather evidence.

[![HSI Web Scraper](https://github.com/dfgrisales5078/HSI-Web-Scraper/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/dfgrisales5078/HSI-Web-Scraper/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Software Overview Document: <a href="Netspider Final Report.pdf">Final Report 2023-2024</a>

# Project Overview Presentation
<p align="center">
  <a href="https://docs.google.com/presentation/d/1tBXKREY9hA72LFQHfF9SY9RlOABc-vO6arp6WOSfq2M/edit?usp=sharing">Project Overview Presentation</a>
</p>


[![AltText](photos/readmeImages/Screenshot%202024-09-20%20113707.png)](https://docs.google.com/presentation/d/1tBXKREY9hA72LFQHfF9SY9RlOABc-vO6arp6WOSfq2M/edit?usp=sharing)

# Censored Demo
<p align="center">
   <a href="https://drive.google.com/file/d/1DItKe31nMTbkqE_HVSeL2_9LD99FNy4W/view?resourcekey">Censored DEMO 3.1v</a></h2>
</p>

[![AltText](photos/readmeImages/Screenshot%202024-09-20%20114023.png)](https://drive.google.com/file/d/1DItKe31nMTbkqE_HVSeL2_9LD99FNy4W/view?resourcekey)


## Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How to Use](#how-to-use)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Evolution of Netspider](#evolution-of-netspider)
- [Future Development](#future-development)
- [Contributions](#contributions)
- [Team](#team)
- [Sponsors and Mentors](#sponsors-and-mentors)
- [License](#license)
- [Contact](#contact)
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
   git clone https://github.com/paulodrefahl/netspider.git
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

## Usage

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

## Team

* **Paulo Drefahl** - Full Stack Developer
* **Zach Sutton** - Full Stack Developer
* **Kevin Kostage** - Full Stack Developer
* **Alyssa Chiego** - Frontend Developer
* **Greg Bateham** - Frontend Developer
* **Corey Record** - Backend Developer
* **Dylan Garcia** - Frontend Developer

## Sponsors and Mentors

* **Sponsor**: Clinton Thompson
* **Mentor**: Dr. Fernando Gonzalez

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

* **Paulo Drefahl** - pdrefahl@fgcu.edu
* **Zachary Sutton** - zesutton2619@eagle.fgcu.edu

## Disclaimer

The complete version of Netspider can only be used by authorized cybercrime investigators, this open source version does not include any sensitive data or exclusive features. Users are responsible for ensuring their use of this tool complies with all applicable laws and regulations. The developers of Netspider are not responsible for any misuse or illegal application of this tool.
