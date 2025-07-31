# Logging Strategy

This document outlines the logging strategy for the `sudo-SQL` project.

## Chosen Library: Loguru

We use the `Loguru` library for all logging purposes. It provides a simple, powerful, and flexible logging solution with minimal configuration.

## Log Levels

The following log levels are used in this project:

- **`DEBUG`**: Detailed information, typically of interest only when diagnosing problems. This includes full schemas, generated SQL for every item, etc.
- **`INFO`**: Confirmation that things are working as expected. This includes major steps in the pipeline, model loading, etc.
- **`WARNING`**: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. 'disk space low'). The software is still working as expected.
- **`ERROR`**: Due to a more serious problem, the software has not been able to perform some function.
- **`CRITICAL`**: A serious error, indicating that the program itself may be unable to continue running.

## Configured Sinks

Two sinks are configured in `sudo_sql/logger_config.py`:

### 1. Console Sink

- **Target**: Standard Error (the console).
- **Log Level**: `INFO`.
- **Format**: Human-readable, colorful format.
- **Purpose**: To provide immediate, high-level feedback to the user running the application interactively.

### 2. File Sink

- **Target**: `logs/sudo-sql.log`.
- **Log Level**: `DEBUG`.
- **Format**: A more detailed, plain-text format.
- **Rotation**: The log file will automatically rotate when it reaches 10 MB.
- **Retention**: Old log files will be kept for 7 days.
- **Purpose**: To provide a complete, persistent record of the application's execution for post-mortem analysis and debugging.

## How to Use the Logger

To use the logger in any module, simply import it from the central configuration:

```python
from sudo_sql.logger_config import logger

logger.info("This is an info message.")
logger.debug("This is a debug message.")
```
