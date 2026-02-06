# AI-Driven Airline Operations & Predictive Flight Management Automation System

A comprehensive Python-based airline operations control center (OCC) simulation that monitors aircraft health, predicts flight delays, optimizes crew scheduling, analyzes passenger load trends, and generates operational reports—similar to systems used by major airlines like Air India, Indigo, Emirates, and others.

---

## 🎯 Project Overview

This system simulates real-world airline operations by:
- Ingesting data from multiple aviation log sources (engine, cabin, weather, crew, passenger)
- Detecting maintenance issues and health anomalies
- Predicting flight delays with specific reasons and estimated minutes
- Validating crew availability and regulatory compliance
- Forecasting passenger load and identifying booking risks
- Generating daily operational reports and critical alerts

---

## ✨ Key Features

### 1. Multi-Source Log Ingestion
Reads and integrates data from:
- **Engine Performance Logs** (thrust, vibration, fuel burn)
- **Cabin Pressure Logs** (pressure, temperature, turbulence)
- **Weather Data Logs** (crosswind, visibility, thunderstorms)
- **Airspeed & Altitude Logs** (airspeed, altitude, status)
- **Crew Schedule Files** (availability, duty hours, rest compliance)
- **Passenger Load Data** (bookings, capacity, historical trends)

### 2. Predictive Delay Engine
Detects potential delays based on:

**Weather Issues:**
- Crosswind > 40 knots
- Thunderstorm flags
- Visibility < 1500 meters

**Maintenance Issues:**
- Engine thrust deviation > 20%
- Sudden cabin pressure drops

**Operational Issues:**
- Runway queue > 25 minutes
- Excessive boarding time
- Crew unavailability

### 3. Aircraft Health Monitoring
Real-time alerts for:
- High engine vibration
- Severe turbulence
- Abnormal fuel burn
- High cabin temperature

### 4. Crew Scheduling Validation
Ensures:
- Minimum crew requirements met
- Rest-hour compliance (10+ hours)
- Daily duty limits (max 14 hours)
- No double-booking

### 5. Passenger Load Prediction
Uses moving averages to:
- Predict passenger count
- Flag overbooking risks
- Identify under-utilized flights

### 6. Automated Reporting
Generates:
- Console dashboard with key metrics
- Daily text reports with full analysis
- Separate log files for health alerts and critical issues

---

## 📁 Project Structure

\`\`\`text

"airline_ops_automation/

│── airline_config.json          # Thresholds and operational rules
│── main.py                      # Main execution controller
│── requirements.txt             # Project dependencies
│── README.md                    # Project documentation
│── modules/                     # Core logic modules
│   ├── log_processor.py
│   ├── delay_predictor.py
│   ├── crew_optimizer.py
│   ├── load_predictor.py
│   ├── health_monitor.py
│   ├── dashboard.py
│   └── reporter.py
│── data/                        # Simulated input logs & CSVs
│   ├── engine_performance.log
│   ├── cabin_pressure.log
│   ├── weather_data.log
│   ├── airspeed_altitude.log
│   ├── crew_schedule.csv
│   └── passenger_load.csv
│── logs/                        # Auto-generated critical alerts
│   ├── aircraft_health_alerts.log
└── output/                      # Auto-generated reports
    └── reports/
        └── aviation_report_YYYY-MM-DD.txt"
\`\`\`

## ⚙️ Installation & Setup

1. **Clone the repository** (or extract the project folder):
   \`\`\`bash
   git clone https://github.com/Rohith19w/AI-Driven-Airline-Operations-Predictive-Flight-Management-Automation-System.git
   cd AI-Driven-Airline-Operations-Predictive-Flight-Management-Automation-System
   \`\`\`

2. **Create a Virtual Environment** (Recommended):
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   \`\`\`

3. **Install Dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## 🚀 How to Run

Execute the main controller script from the root directory:
\`\`\`bash
python main.py
\`\`\`

### What to expect upon execution:
1. The **Log Processor** will ingest all files from the `data/` directory.
2. The **Dashboard** will print directly to your terminal, displaying flight status, delays, and alerts in a formatted grid.
3. Any critical aircraft issues will be appended to `logs/aircraft_health_alerts.log`.
4. A full daily summary report will be generated in `output/reports/`.

## 🛠️ Configuration
You can easily tweak the system's operational rules without changing the code. Open `airline_config.json` to adjust:
* Weather thresholds (e.g., maximum safe crosswind speed).
* Maintenance thresholds (e.g., maximum allowed engine vibration).
* Crew rules (e.g., minimum rest hours required).

## 👨‍💻 Author
**Jakkireddy Rohith Raghavendra Reddy**  
*Python Intern @ Flipkart Pvt Ltd*
