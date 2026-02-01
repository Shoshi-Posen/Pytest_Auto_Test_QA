# Ammeter Emulators

This project provides emulators for different types of ammeters: Greenlee, ENTES, and CIRCUTOR. Each ammeter emulator runs on a separate thread and can respond to current measurement requests.

## Project Structure

- `Ammeters/`
  - `main.py`: Main script to start the ammeter emulators and request current measurements.
  - `Circutor_Ammeter.py`: Emulator for the CIRCUTOR ammeter.
  - `Entes_Ammeter.py`: Emulator for the ENTES ammeter.
  - `Greenlee_Ammeter.py`: Emulator for the Greenlee ammeter.
  - `base_ammeter.py`: Base class for all ammeter emulators.
  - `client.py`: Client to request current measurements from the ammeter emulators.
- `Utiles/`
  - `Utils.py`: Utility functions, including `generate_random_float`.

## Usage

# Ammeter Emulators

## Greenlee Ammeter

- **Port**: 5000
- **Command**: `MEASURE_GREENLEE -get_measurement`
- **Measurement Logic**: Calculates current using voltage (1V - 10V) and (0.1Ω - 100Ω).
- **Measurement method** : Ohm's Law: I = V / R

## ENTES Ammeter

- **Port**: 5001
- **Command**: `MEASURE_ENTES -get_data`
- **Measurement Logic**: Calculates current using magnetic field strength (0.01T - 0.1T) and calibration factor (500 - 2000).
- **Measurement method** : Hall Effect: I = B * K

## CIRCUTOR Ammeter

- **Port**: 5002
- **Command**: `MEASURE_CIRCUTOR -get_measurement`
- **Measurement Logic**: Calculates current using voltage values (0.1V - 1.0V) over a number of samples and a random time step (0.001s - 0.01s).
- **Measurement method** : Rogowski Coil Integration: I = ∫V dt

To start the ammeter emulators and request current measurements, run the `main.py` script:
```sh
python main.py
```

**## Bug Fixes & Technical Improvements - Shoshi Posen

- Fixed port numbers in main.py to match the documented ports(5000-5002 and not 5001-5003).
- Updated command strings to match the ammeter protocol. (for ex. b'MEASURE_GREENLEE -get_measurement' and not b'MEASURE_GREENLEE')
- Added init.py file to Ammeters folder, because it was not recognized as Python package.
- Developed the "_get_measurement" method in DataCollector.
- Added a while True loop to main.py, to prevent the emulator threads from terminating immediately, allowing the test framework to establish a connection.
- Updated the command for 'circutor' in test_config.yaml to the expected command (include the required -current flag.)
- Fixed a TypeError in "_advanced_analysis" method - by converting 'numpy.bool' type to standard Python types before saving results.
- Resolved a TypeError in result_analyzer.py by updating the scipy.stats.t.interval parameter from "alpha" to "confidence" (compatible with SciPy 1.7+).
- Raise KeyError in case the ammeter_type is invalid (the test case: test_invalid_ammeter_type)
- The system now automatically organizes all test results in a clear folder structure. Each test gets its own unique ID. (JSON and the visualization graphs)
- Implemented a logger to track the testing process in real-time and to save the logs.
- Added logic to quantify measurement precision and automatically identify the most reliable device based on consistency metrics.

- pip install seaborn 
- pip install matplotlib
- pip install pyyaml
- pip install numpy
- pip install scipy
