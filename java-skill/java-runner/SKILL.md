---
name: java-runner
description: Run Java main classes and test methods using Maven with configurable Java home and Maven settings. Use when users need to execute Java applications, run unit tests, or run specific test methods in Maven projects. Supports both fully qualified class names (com.example.Main) and file paths (src/main/java/com/example/Main.java). Handles JVM arguments, program arguments, and Maven configuration.
---

# Java Runner

## Overview

This skill enables running Java main classes and test methods in Maven projects with full control over Java home, Maven settings, and runtime parameters. It automatically resolves Maven classpath and supports both class names and file paths.

## Quick Start

### Running a Main Class

Use the `run_java_class.py` script to execute Java main classes:

```bash
# Using class name
python scripts/run_java_class.py com.example.Main

# Using file path
python scripts/run_java_class.py src/main/java/com/example/Main.java

# With program arguments
python scripts/run_java_class.py com.example.Main --args "arg1 arg2"

# With JVM arguments
python scripts/run_java_class.py com.example.Main --jvm-args "-Xmx4g -Denv=dev"
```

### Running Tests

Use the `run_java_test.py` script to execute JUnit tests:

```bash
# Run all tests in a class
python scripts/run_java_test.py com.example.MyTest

# Run specific test method
python scripts/run_java_test.py com.example.MyTest#testMethod

# Using file path
python scripts/run_java_test.py src/test/java/com/example/MyTest.java

# With Maven arguments
python scripts/run_java_test.py com.example.MyTest --maven-args "-X"
```

## Configuration

### First Time Setup

When you first run the skill, it will automatically prompt you to configure:

```bash
# First run will trigger configuration wizard
python scripts/run_java_class.py com.example.Main
```

The configuration wizard will ask for:
- Java Home 路径
- Maven Home 路径
- Maven settings.xml 路径（可选）
- 默认 JVM 参数（可选）
- 默认 Maven 参数（可选）

Configuration is saved to: `~/.skills/java-skill.conf`

### Manual Configuration

You can also manually initialize or reconfigure:

```bash
# Initialize or reset configuration
python scripts/init_config.py

# Show current configuration
python scripts/init_config.py show
```

### Configuration File Location

The configuration is stored in your home directory:
- **Linux/Mac**: `~/.skills/java-skill.conf`
- **Windows**: `C:\Users\<username>\.skills\java-skill.conf`

### Configuration Format

```json
{
  "java_home": "C:/Program Files/Java/jdk-17",
  "maven_home": "C:/apache-maven-3.9.0",
  "maven_settings": "C:/Users/username/.m2/settings.xml",
  "default_jvm_args": ["-Xmx2g", "-Xms512m"],
  "default_maven_args": []
}
```

### Override Configuration

You can override the default configuration with a custom config file:

```bash
python scripts/run_java_class.py com.example.Main --config /path/to/custom-config.json
```

### Configuration Priority

Configuration values are resolved in this order (highest to lowest priority):

1. Command-line arguments (`--java-home`, `--maven-settings`)
2. Custom configuration file (`--config custom.json`)
3. Default configuration file (`~/.skills/java-skill.conf`)
4. Interactive prompt (first time only)

## Running Java Classes

### Basic Usage

The `run_java_class.py` script executes Java main classes with Maven classpath:

```bash
python scripts/run_java_class.py <class_name> [options]
```

### Input Formats

**Fully qualified class name:**
```bash
python scripts/run_java_class.py com.example.Main
```

**File path (automatically converted to class name):**
```bash
python scripts/run_java_class.py src/main/java/com/example/Main.java
```

### Options

- `--config CONFIG`: Path to configuration file
- `--java-home JAVA_HOME`: Override Java home directory
- `--maven-settings SETTINGS`: Override Maven settings.xml path
- `--args ARGS`: Program arguments (space-separated)
- `--jvm-args JVM_ARGS`: JVM arguments (space-separated)
- `--project-dir DIR`: Project directory (default: auto-detect from pom.xml)

### Examples

**Run with custom JVM memory:**
```bash
python scripts/run_java_class.py com.example.Main --jvm-args "-Xmx4g -Xms1g"
```

**Run with system properties:**
```bash
python scripts/run_java_class.py com.example.Main --jvm-args "-Denv=dev -Dlog.level=DEBUG"
```

**Run with program arguments:**
```bash
python scripts/run_java_class.py com.example.Main --args "input.txt output.txt"
```

**Run with custom Maven settings:**
```bash
python scripts/run_java_class.py com.example.Main --maven-settings /path/to/settings.xml
```

## Running Tests

### Basic Usage

The `run_java_test.py` script executes JUnit tests using Maven:

```bash
python scripts/run_java_test.py <test_name> [options]
```

### Input Formats

**Test class:**
```bash
python scripts/run_java_test.py com.example.MyTest
```

**Test method:**
```bash
python scripts/run_java_test.py com.example.MyTest#testMethod
```

**File path:**
```bash
python scripts/run_java_test.py src/test/java/com/example/MyTest.java
python scripts/run_java_test.py src/test/java/com/example/MyTest.java#testMethod
```

### Options

- `--config CONFIG`: Path to configuration file
- `--java-home JAVA_HOME`: Override Java home directory
- `--maven-settings SETTINGS`: Override Maven settings.xml path
- `--maven-args ARGS`: Additional Maven arguments
- `--project-dir DIR`: Project directory (default: auto-detect from pom.xml)

### Examples

**Run all tests in a class:**
```bash
python scripts/run_java_test.py com.example.service.UserServiceTest
```

**Run specific test method:**
```bash
python scripts/run_java_test.py com.example.service.UserServiceTest#testCreateUser
```

**Run with Maven debug output:**
```bash
python scripts/run_java_test.py com.example.MyTest --maven-args "-X"
```

**Run tests with custom settings:**
```bash
python scripts/run_java_test.py com.example.MyTest --maven-settings /path/to/settings.xml
```

**Run tests in offline mode:**
```bash
python scripts/run_java_test.py com.example.MyTest --maven-args "-o"
```

## Advanced Usage

### Pattern Matching for Tests

Use wildcards to run multiple tests:

```bash
# Run all tests ending with "Test"
python scripts/run_java_test.py "*Test"

# Run all tests in a package
python scripts/run_java_test.py "com.example.service.*Test"
```

### Running Multiple Test Methods

```bash
# JUnit 4 style
python scripts/run_java_test.py "MyTest#testMethod1+testMethod2"

# JUnit 5 style
python scripts/run_java_test.py "MyTest#testMethod1,testMethod2"
```

### Custom Project Directory

If not in the project root, specify the project directory:

```bash
python scripts/run_java_class.py com.example.Main --project-dir /path/to/project
```

## Troubleshooting

### Common Issues

**"Could not find pom.xml"**
- Ensure you're running from within a Maven project
- Or use `--project-dir` to specify the project location

**"Error getting Maven classpath"**
- Verify Maven is installed and `maven_home` is correct
- Check that `mvn` command works in terminal
- Ensure project dependencies are downloaded (`mvn dependency:resolve`)

**"Class not found"**
- Verify the class name is correct
- Ensure project is compiled (`mvn compile` or `mvn test-compile`)
- Check that the class exists in `target/classes` or `target/test-classes`

**"JAVA_HOME not set"**
- Set `java_home` in config.json
- Or use `--java-home` command-line argument
- Or set `JAVA_HOME` environment variable

### Debugging

**Enable Maven debug output:**
```bash
python scripts/run_java_test.py MyTest --maven-args "-X"
```

**Check classpath:**
```bash
mvn dependency:build-classpath
```

**Verify Java version:**
```bash
"$JAVA_HOME/bin/java" -version
```

## Reference Documentation

For more detailed information, see:

- **[maven_commands.md](references/maven_commands.md)**: Comprehensive Maven command reference
- **[junit_patterns.md](references/junit_patterns.md)**: JUnit testing patterns and best practices

## Workflow Examples

### Example 1: Run Main Class with Custom Configuration

```bash
# 1. Create configuration file
cp assets/config.template.json my-config.json

# 2. Edit configuration
# Set java_home, maven_home, maven_settings

# 3. Run the main class
python scripts/run_java_class.py com.example.Application --config my-config.json
```

### Example 2: Run Specific Test Method

```bash
# 1. Find the test file
# src/test/java/com/example/UserServiceTest.java

# 2. Run specific test method
python scripts/run_java_test.py src/test/java/com/example/UserServiceTest.java#testCreateUser

# Or use class name
python scripts/run_java_test.py com.example.UserServiceTest#testCreateUser
```

### Example 3: Run with Different Maven Settings

```bash
# Run with production settings
python scripts/run_java_class.py com.example.Main --maven-settings ~/.m2/settings-prod.xml

# Run tests with test settings
python scripts/run_java_test.py MyTest --maven-settings ~/.m2/settings-test.xml
```

## Notes

- Scripts automatically detect the project root by searching for `pom.xml`
- Maven classpath is resolved dynamically using `mvn dependency:build-classpath`
- Both `target/classes` and Maven dependencies are included in classpath
- File paths are automatically converted to fully qualified class names
- Scripts work on Windows, Linux, and macOS
