import numpy as np


def equilibriumMositureContent(realtiveHumidity, temperature):
    if (realtiveHumidity <= 10.0):
        equilibriumMositureContent = 0.03229 + 0.281073 * realtiveHumidity - 0.000578 * realtiveHumidity * temperature

    elif (10.0 < realtiveHumidity <= 50.0):
        equilibriumMositureContent = 2.22749 + 0.160107 * realtiveHumidity - 0.01478 * temperature;

    elif (realtiveHumidity > 50.0):
        equilibriumMositureContent = 21.0606 + 0.005565 * realtiveHumidity * realtiveHumidity - 0.00035 * realtiveHumidity * temperature - 0.483199 * realtiveHumidity

    # print(equilibriumMositureContent)

    return equilibriumMositureContent;


def moistureDampingCoefficient(equilibriumMositureContent):
    equilibriumMositureContent30 = equilibriumMositureContent / 30

    moistureDampingCoefficient = 1 - (2 * equilibriumMositureContent30) + 1.5 * (
                equilibriumMositureContent30 * equilibriumMositureContent30) - 0.5 * (
                                             equilibriumMositureContent30 * equilibriumMositureContent30 * equilibriumMositureContent30)
    # print(moistureDampingCoefficient)
    return moistureDampingCoefficient


def FWI(moistureDampingCoefficient, windSpeed):
    powWindSpeed = windSpeed * windSpeed;

    fwi = (moistureDampingCoefficient * np.sqrt(1 + powWindSpeed)) / 0.3002
    # fwi=moistureDampingCoefficient*[(1+windSpeed^2)^0.5]/0.3002
    return fwi;


def getRisk(temperature,windSpeed,relaiveHumidity):
    e = equilibriumMositureContent(relaiveHumidity, temperature)
    m = moistureDampingCoefficient(e)
    fwi = FWI(m,windSpeed)
    risk=""

    ratingSacle = fwi % 100

    if (ratingSacle < 5.2):
        risk="Very Low Risk"

    elif (5.2 <= ratingSacle < 11.2):
        risk="Low Risk"

    elif (11.2 <= ratingSacle < 21.3):
        risk="Moderate Risk"

    elif (21.3 <= ratingSacle < 38.0):
        risk="High Risk"

    elif (38.0 <= ratingSacle < 50.0):
        risk="Very High Risk"

    else:
        risk="Extreme"

    return risk

