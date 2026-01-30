#!/usr/bin/env python3
"""
Run Java test methods with Maven

Configuration:
    Reads from ~/.skills/java-skill.conf (created on first run)
    Can override with --config option

Usage:
    run_java_test.py <test_class_or_method> [--config CONFIG] [--java-home JAVA_HOME]
                     [--maven-settings SETTINGS] [--maven-args ARGS]

Examples:
    run_java_test.py com.example.MyTest
    run_java_test.py com.example.MyTest#testMethod
    run_java_test.py src/test/java/com/example/MyTest.java
    run_java_test.py src/test/java/com/example/MyTest.java#testMethod
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

# Import config manager
try:
    from config_manager import load_config
except ImportError:
    # If running from different directory, try to import from same directory
    script_dir = Path(__file__).parent
    sys.path.insert(0, str(script_dir))
    from config_manager import load_config


def resolve_test_name(input_str):
    """
    Convert file path to test class name or return test name as-is

    Examples:
        src/test/java/com/example/MyTest.java -> com.example.MyTest
        src/test/java/com/example/MyTest.java#testMethod -> com.example.MyTest#testMethod
        com.example.MyTest#testMethod -> com.example.MyTest#testMethod
    """
    # Split method name if present
    method_name = None
    if '#' in input_str:
        input_str, method_name = input_str.split('#', 1)

    if input_str.endswith('.java'):
        # Convert file path to class name
        path = Path(input_str)

        # Find src/test/java in path
        parts = path.parts
        try:
            if 'src' in parts:
                src_idx = parts.index('src')
                # Skip src/test/java
                if src_idx + 2 < len(parts) and parts[src_idx + 1] == 'test' and parts[src_idx + 2] == 'java':
                    class_parts = parts[src_idx + 3:]
                else:
                    class_parts = parts[src_idx + 1:]

                # Remove .java extension from last part
                class_parts = list(class_parts)
                class_parts[-1] = class_parts[-1].replace('.java', '')

                class_name = '.'.join(class_parts)
            else:
                # Fallback: just remove .java and convert slashes to dots
                class_name = input_str.replace('.java', '').replace('/', '.').replace('\\', '.')
        except (ValueError, IndexError):
            class_name = input_str.replace('.java', '').replace('/', '.').replace('\\', '.')
    else:
        class_name = input_str

    # Add method name back if present
    if method_name:
        return f"{class_name}#{method_name}"

    return class_name


def run_java_test(test_name, config, java_home=None, maven_settings=None,
                  maven_args=None, project_dir=None):
    """Run Java test with Maven"""

    # Override config with command line arguments
    if java_home:
        config['java_home'] = java_home
        os.environ['JAVA_HOME'] = java_home
    elif config['java_home']:
        os.environ['JAVA_HOME'] = config['java_home']

    if maven_settings:
        config['maven_settings'] = maven_settings

    # Resolve test name if it's a file path
    test_name = resolve_test_name(test_name)

    # Find project directory (look for pom.xml)
    if not project_dir:
        project_dir = Path.cwd()
        while project_dir != project_dir.parent:
            if (project_dir / 'pom.xml').exists():
                break
            project_dir = project_dir.parent
        else:
            print("Error: Could not find pom.xml in current or parent directories", file=sys.stderr)
            return 1

    # Build Maven command
    maven_cmd = os.path.join(config['maven_home'], 'bin', 'mvn')
    if sys.platform == 'win32':
        maven_cmd += '.cmd'

    cmd = [maven_cmd, 'test']

    # Add Maven settings
    if config['maven_settings']:
        cmd.extend(['-s', config['maven_settings']])

    # Add test filter
    cmd.append(f'-Dtest={test_name}')

    # Add Maven arguments
    if maven_args:
        cmd.extend(maven_args.split())
    elif config.get('default_maven_args'):
        cmd.extend(config['default_maven_args'])

    # Run command
    print(f"Running test: {test_name}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)

    try:
        result = subprocess.run(cmd, cwd=project_dir)
        return result.returncode
    except Exception as e:
        print(f"Error running test: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Run Java test methods with Maven'
    )
    parser.add_argument('test_name', help='Test class or method (e.g., com.example.MyTest or com.example.MyTest#testMethod)')
    parser.add_argument('--config', help='Path to config.json file')
    parser.add_argument('--java-home', help='Java home directory')
    parser.add_argument('--maven-settings', help='Maven settings.xml path')
    parser.add_argument('--maven-args', help='Additional Maven arguments')
    parser.add_argument('--project-dir', help='Project directory (default: auto-detect)')

    parsed_args = parser.parse_args()

    # Load configuration
    config = load_config(parsed_args.config)

    # Run test
    return run_java_test(
        parsed_args.test_name,
        config,
        java_home=parsed_args.java_home,
        maven_settings=parsed_args.maven_settings,
        maven_args=parsed_args.maven_args,
        project_dir=parsed_args.project_dir
    )


if __name__ == "__main__":
    sys.exit(main())
