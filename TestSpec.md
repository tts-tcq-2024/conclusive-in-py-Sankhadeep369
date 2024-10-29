# Test Specification Document

## Overview

This document specifies the tests for the `Typewise Battery Temperature Monitoring System`, detailing:

1. **Test Cases**: Core functions and expected behaviors.
2. **Objectives**: Validate correct functionality, error handling, and output.
3. **Coverage**: Key functions (`infer_breach`, `classify_temperature_breach`, `check_and_alert`) with tests for normal, boundary, and erroneous conditions.

### Test Suite Structure

The test cases are organized into three sections, aligned with the main functions:
- `infer_breach`
- `classify_temperature_breach`
- `check_and_alert`

---

## Test Cases

### 1. Test Case: `infer_breach` Function

**Objective**: Verify that `infer_breach` correctly identifies if a temperature value is `TOO_LOW`, `TOO_HIGH`, or `NORMAL`.

| Test ID | Test Scenario      | Input (`value`, `lower_limit`, `upper_limit`) | Expected Output |
|---------|---------------------|-----------------------------------------------|-----------------|
| TIB-01  | Value below limit  | `20`, `50`, `100`                             | `TOO_LOW`      |
| TIB-02  | Value above limit  | `80`, `50`, `70`                              | `TOO_HIGH`     |
| TIB-03  | Value within limit | `55`, `50`, `100`                             | `NORMAL`       |

---

### 2. Test Case: `classify_temperature_breach` Function

**Objective**: Verify that `classify_temperature_breach` correctly classifies temperature breaches based on cooling type and temperature. 

| Test ID     | Test Scenario              | Input (`cooling_type`, `temperature_in_c`) | Expected Output  |
|-------------|----------------------------|--------------------------------------------|------------------|
| TCB-01      | `PASSIVE_COOLING`, normal  | `PASSIVE_COOLING`, `25`                    | `NORMAL`        |
| TCB-02      | `PASSIVE_COOLING`, high    | `PASSIVE_COOLING`, `36`                    | `TOO_HIGH`      |
| TCB-03      | `HI_ACTIVE_COOLING`, high  | `HI_ACTIVE_COOLING`, `46`                  | `TOO_HIGH`      |
| TCB-04      | `MED_ACTIVE_COOLING`, high | `MED_ACTIVE_COOLING`, `41`                 | `TOO_HIGH`      |
| TCB-05      | Unknown cooling type       | `UNKNOWN_COOLING`, `20`                    | Exception raised (`ValueError`) |

**Special Notes**:
- **Boundary Testing**: `TCB-02`, `TCB-03`, and `TCB-04` test conditions at or just above limits for each cooling type.
- **Exception Testing**: `TCB-05` checks for proper error handling when an unknown cooling type is passed.

---

### 3. Test Case: `check_and_alert` Function

**Objective**: Validate alert dispatch functionality for different alert targets (`TO_CONTROLLER`, `TO_EMAIL`) and confirm correct output messages.

| Test ID      | Test Scenario              | Input (`alert_target`, `battery_char`, `temperature_in_c`)  | Expected Output                                     |
|--------------|----------------------------|-------------------------------------------------------------|-----------------------------------------------------|
| TCA-01       | Send alert to controller   | `TO_CONTROLLER`, `{coolingType: PASSIVE_COOLING}`, `40`     | Printed message: `65261, TOO_HIGH`                 |
| TCA-02       | Send alert via email, low  | `TO_EMAIL`, `{coolingType: PASSIVE_COOLING}`, `5`           | Printed message: `To: a.b@c.com`, followed by `Hi, the temperature is too low` |
| TCA-03       | Send alert via email, high | `TO_EMAIL`, `{coolingType: PASSIVE_COOLING}`, `40`          | Printed message: `To: a.b@c.com`, followed by `Hi, the temperature is too high` |

**Mocking and Validation**:
- **Standard Output Mocking**: `TCA-01`, `TCA-02`, and `TCA-03` use `unittest.mock` to mock the `print` function, capturing output to validate against expected messages.
- **Boundary Conditions**: Testing at temperature limits for each type ensures the correct breach level and proper alert dispatch.
  
**Special Notes**:
- The tests focus on confirming that each alert target correctly handles various breach types and outputs the exact formatted messages expected by stakeholders.

---

## Test Execution and Coverage

### Execution
- Each test case can be executed independently via `unittest`.
- `mock.patch` is used to capture print output, ensuring that actual hardware or email services are not triggered during tests.

### Coverage
- **Branch Coverage**: Tests cover multiple branches, including different cooling types, breach conditions, and alerts.
- **Exception Paths**: Specific tests handle invalid inputs, ensuring robust error reporting and code stability.

---

## Summary

This test specification document outlines a thorough approach to testing the `Typewise Battery Temperature Monitoring System`. With clear objectives, boundary testing, and extensive validation of outputs, the tests ensure that the system performs reliably under various conditions and provides appropriate feedback in error scenarios.
