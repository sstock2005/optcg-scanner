# TCG Player Card Tracker

TCG Player Card Tracker is a Python-based application designed to help collectors and gamers track the market value of playing cards. It scrapes card data from [tcgplayer.com](https://tcgplayer.com) and uses computer vision techniques with machine learning to detect cards from images. The tool displays the current market price of detected cards and keeps a history, making it easier to monitor profits from pulling cards from packs.

## Why This Project?

Many collectors and gamers spend valuable time manually checking prices and evaluating card pulls. This project was created to automate the process by:
- **Scraping Data:** Automatically retrieving up-to-date images and market prices from tcgplayer.com.
- **Card Detection:** Utilizing machine learning to accurately detect cards from live video feeds.
- **Profit Tracking:** Maintaining a history of detected cards and their market prices to help users assess overall profitability.

## Features

- **Automated Data Collection:** Retrieves card images and pricing data.
- **Machine Learning Detection:** Uses ORB feature matching for card recognition.
- **Real-Time Price Display:** Shows the market price for detected cards.
- **Historical Tracking:** Records a history of card pulls and corresponding prices.
- **Cross-Platform:** Compatible with both Windows and Unix-based systems.

## Installation

### Prerequisites

- Python 3.7 or higher
- Required Python libraries:
  - `requests`
  - `opencv-python`
  - `numpy`

### On Windows

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/tcg-player-card-tracker.git
   cd tcg-player-card-tracker
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### On Unix (Linux/Mac)

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/tcg-player-card-tracker.git
   cd tcg-player-card-tracker
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### On Windows

1. **Activate Your Virtual Environment:**

   ```bash
   venv\Scripts\activate
   ```

2. **Run the Main Script:**

   ```bash
   python main.py
   ```

3. **Follow the On-Screen Prompts:**
   - Enter the set code (e.g., `OP10`).
   - Choose the interface (default is `0`).

### On Unix (Linux/Mac)

1. **Activate Your Virtual Environment:**

   ```bash
   source venv/bin/activate
   ```

2. **Run the Main Script:**

   ```bash
   python main.py
   ```

3. **Follow the On-Screen Prompts:**
   - Enter the set code (e.g., `OP10`).
   - Choose the interface (default is `0`).

## Project Structure

```
├── main.py
├── scripts
│   ├── api.py
│   ├── constants.py
│   └── scanner.py
├── sources
│   ├── (scraped images and price data will be stored here)
└── README.md
```

## Preview

*add later*