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
