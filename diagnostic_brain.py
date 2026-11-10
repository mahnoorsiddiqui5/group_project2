import csv
import math
from pathlib import Path

import data_simulator


RADIATION_LIMIT_SV = 0.0013

HEART_RATE_MIN = 50
HEART_RATE_MAX = 100
SLEEP_MIN_HOURS = 6
OXYGEN_MIN = 95
TEMPERATURE_MIN = 36
TEMPERATURE_MAX = 38
SYSTOLIC_BP_MIN = 90
SYSTOLIC_BP_MAX = 120


def get_recent_days(number_of_days=3):
    csv_file = Path(__file__).with_name("astronaut_vitals.csv")

    try:
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        return rows[-number_of_days:]

    except FileNotFoundError:
        return []


def evaluate_health(data, recent_data=None):
    if not data:
        return {
            "status": "No Data",
            "alerts": ["No health data available."],
            "recommendations": ["Generate or load health data first."]
        }

    alerts = []
    recommendations = []

    try:
        heart_rate = float(data["heart_rate"])
        sleep_hours = float(data["sleep_hours"])
        oxygen = float(data["blood_oxygen"])
        temperature = float(data["core_bodyTemp"])
        blood_pressure = float(data["systolic_bloodPressure"])
        radiation = float(data["radiation_exposure"])

        measurements = [
            heart_rate,
            sleep_hours,
            oxygen,
            temperature,
            blood_pressure,
            radiation
        ]

        if not all(
            math.isfinite(value) and value >= 0
            for value in measurements
        ):
            raise ValueError

    except (KeyError, TypeError, ValueError):
        return {
            "status": "Invalid Data",
            "alerts": ["One or more measurements are missing or invalid."],
            "recommendations": [
                "Check the CSV column names and values."
            ]
        }

    if heart_rate < HEART_RATE_MIN or heart_rate > HEART_RATE_MAX:
        alerts.append("Heart rate is outside the starter check range.")
        recommendations.append("Flag the heart-rate measurement for review.")

    if sleep_hours < SLEEP_MIN_HOURS:
        alerts.append("Sleep duration is below the starter check.")
        recommendations.append("Review the sleep record.")

    if oxygen < OXYGEN_MIN:
        alerts.append("Blood oxygen is below the starter check.")
        recommendations.append("Flag the oxygen measurement for review.")

    if temperature < TEMPERATURE_MIN or temperature > TEMPERATURE_MAX:
        alerts.append("Core body temperature is outside the example range.")
        recommendations.append("Flag the temperature measurement for review.")

    if blood_pressure < SYSTOLIC_BP_MIN or blood_pressure > SYSTOLIC_BP_MAX:
        alerts.append("Systolic blood pressure is outside the example range.")
        recommendations.append("Flag the blood-pressure measurement for review.")

    if (
        RADIATION_LIMIT_SV is not None
        and radiation > RADIATION_LIMIT_SV
    ):
        alerts.append("Daily radiation exposure exceeds the project limit.")
        recommendations.append("Flag daily radiation exposure for review.")

    if recent_data is None:
        recent_data = get_recent_days(3)

    three_day_sleep_check = False

    if len(recent_data) >= 3:
        try:
            last_three_sleep_values = [
                float(day["sleep_hours"])
                for day in recent_data[-3:]
            ]

            if all(
                math.isfinite(value) and value >= 0
                for value in last_three_sleep_values
            ):
                three_day_sleep_check = all(
                    value < SLEEP_MIN_HOURS
                    for value in last_three_sleep_values
                )

        except (KeyError, TypeError, ValueError):
            three_day_sleep_check = False

    if three_day_sleep_check:
        alerts.append(
            "Sleep duration has been below the starter threshold "
            "for three consecutive recorded days."
        )
        recommendations.append(
            "Flag the three-day sleep pattern for review."
        )

    if three_day_sleep_check or len(alerts) >= 2:
        status = "Action Required"
    elif alerts:
        status = "Caution"
    else:
        status = "Nominal"

    if not recommendations:
        recommendations.append(
            "No starter-rule alerts were triggered."
        )

    return {
        "status": status,
        "alerts": alerts,
        "recommendations": recommendations
    }


if __name__ == "__main__":
    print("Recent astronaut data:")

    data = data_simulator.latest()
    print(data)

    result = evaluate_health(data)

    print("\nHealth Evaluation:")
    print(result)