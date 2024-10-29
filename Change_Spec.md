# Typewise Battery Temperature Monitoring System

## Overview

This project is designed to monitor battery temperature and prevent damage by:

1. Classifying the temperature measurement as too high, too low, or normal, based on the type of cooling.
2. Transmitting the classification to take action:
   - If a controller is available, sending the classification to the controller.
   - If no controller is available, sending the classification via email.

The project includes enhanced testing, complexity reduction, and exception handling to improve maintainability and reliability.

## Key Changes and Improvements

### 1. Refactoring for Cyclomatic Complexity

The initial legacy code contained functions with high cyclomatic complexity. We refactored the following functions to reduce complexity and improve readability:

- **`classify_temperature_breach`**:
  - Refactored to use a dictionary (`BATTERY_LIMITS`) to store cooling types and their respective temperature limits.
  - Simplified the function logic by directly referencing temperature limits based on `coolingType`.

- **`check_and_alert`**:
  - Replaced conditionals with a dictionary (`alert_functions`) for alert dispatch based on `alertTarget`.
  - This change enables easier addition of new alert types in the future.

### 2. Enhanced Error Handling

The refactored code now includes better error handling for unsupported cooling types:

- **`classify_temperature_breach`**:
  - Added validation to raise a `ValueError` for unknown `coolingType` values.
  - This prevents unintended behavior and ensures explicit handling of all supported cooling types.

### 3. Improved Test Coverage

We expanded the test suite to cover multiple scenarios and increase overall code coverage:

- **Test Cases Added**:
  - **`test_infer_breach_as_per_limits`**: Validates the `infer_breach` function across different value ranges to ensure correct breach detection.
  - **`test_classify_temperature_breach`**: Tests `classify_temperature_breach` across all valid cooling types and with an invalid type to validate error handling.
  - **`test_check_and_alert`**: Simulates alert dispatches to both the controller and email, verifying expected output using mocked print statements.

### 4. Mocking and Output Validation

To ensure that alerts were correctly dispatched, we used the `unittest.mock` library:

- **Controller and Email Output Validation**:
  - Mocked the `print` function to capture its output during testing.
  - Added assertions to check specific output messages without dependency on `sys.stdout`, ensuring robustness across test environments.

## Summary of Improvements

1. **Code Quality**: Reduced complexity by replacing nested conditionals with dictionaries for flexibility.
2. **Error Handling**: Validated cooling type input and raised appropriate exceptions.
3. **Test Coverage**: Increased coverage by adding tests for all logical branches, including error scenarios.
4. **Robustness in Testing**: Used mock assertions to directly validate output, ensuring accurate test results.

This refactoring makes the codebase more maintainable, testable, and extensible for future requirements.
