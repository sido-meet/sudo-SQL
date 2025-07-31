# Pipeline Architecture

This document outlines the architecture of the `sudo-SQL` pipeline.

## Philosophy: The Strategy Pattern

The pipeline uses the **Strategy Pattern** to handle different modes of operation (e.g., `sft`, `rl`, `infer`). This approach avoids a single, monolithic class and promotes a clean, modular, and extensible design.

## Core Components

### `sudo_sql/pipeline/`

This directory contains the core pipeline logic, organized into the following modules:

- **`base.py`**: Defines the `BasePipeline` abstract class. This class contains all the shared logic common to all pipeline modes, such as configuration loading, dataset loading, and the PPO trainer initialization.

- **`inference.py`**, **`sft.py`**, **`rl.py`**: These files contain the concrete implementations of the `BasePipeline` for each specific mode. Each module has a single class (e.g., `InferencePipeline`) that implements the `run()` method with the logic specific to that mode.

- **`__init__.py`**: This file acts as a factory. It contains the `get_pipeline()` function, which is the single entry point for the rest of the application. This function reads the `mode` from the configuration and returns an instance of the appropriate pipeline class.

### Class Hierarchy

```
          +----------------+
          |  BasePipeline  |
          +----------------+
                 ^
                 |
       +---------+---------+
       |         |         |
+------v------+ +------v-----+ +----v---+
|InferencePipe| | SFTPipeline| |RLPipeline|
+-------------+ +------------+ +--------+
```

### `main.py`

The main application entry point is now much cleaner. It simply:

1.  Imports the `get_pipeline` factory.
2.  Loads the configuration file.
3.  Calls `get_pipeline()` to get the correct pipeline instance.
4.  Calls `pipeline.run()`.

This architecture makes the codebase more maintainable, scalable, and easier to test.
