#!/usr/bin/env python3
"""
Run Java main class with Maven classpath

Configuration:
    Reads from ~/.skills/java-skill.conf (created on first run)
    Can override with --config option

Usage:
    run_java_class.py <class_name> [--config CONFIG] [--java-home JAVA_HOME]
                      [--maven-settings SETTINGS] [--args ARGS] [--jvm-args JVM_ARGS]

Examples:
    run_java_class.py com.example.Main
    run_java_class.py com.example.Main --args "arg1 arg2"
    run_java_class.py com.example.Main --jvm-args "-Xmx4g -Denv=dev"
    run_java_class.py src/main/java/com/example/Main.java
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


def resolve_class_name(input_str):
    """
    Convert file path to class name or return class name as-is

    Examples:
        src/main/java/com/example/Main.java -> com.example.Main
        com.example.Main -> com.example.Main
    """
    if input_str.endswith('.java'):
        # Convert file path to class name
        path = Path(input_str)

        # Find src/main/java or src/test/java in path
        parts = path.parts
        try:
            if 'src' in parts:
                src_idx = parts.index('src')
                # Skip src/main/java or src/test/java
                if src_idx + 2 < len(parts) and parts[src_idx + 1] in ['main', 'test'] and parts[src_idx + 2] == 'java':
                    class_parts = parts[src_idx + 3:]
                else:
                    class_parts = parts[src_idx + 1:]

                # Remove .java extension from last part
                class_parts = list(class_parts)
                class_parts[-1] = class_parts[-1].replace('.java', '')

                return '.'.join(class_parts)
        except (ValueError, IndexError):
            pass

        # Fallback: just remove .java and convert slashes to dots
        return input_str.replace('.java', '').replace('/', '.').replace('\\', '.')

    return input_str


def get_maven_classpath(maven_home, maven_settings, project_dir):
    """Get classpath from Maven"""
    maven_cmd = os.path.join(maven_home, 'bin', 'mvn')
    if sys.platform == 'win32':
        maven_cmd += '.cmd'

    cmd = [maven_cmd, 'dependency:build-classpath', '-DincludeScope=runtime']

    if maven_settings:
        cmd.extend(['-s', maven_settings])

    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        # Parse classpath from output
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines):
            if '[INFO] Dependencies classpath:' in line and i + 1 < len(lines):
                return lines[i + 1].strip()

        # Alternative: look for classpath in output
        for line in lines:
            if line and not line.startswith('[') and os.pathsep in line:
                return line.strip()

    except Exception as e:
        print(f"Error getting Maven classpath: {e}", file=sys.stderr)

    return ""


def run_java_class(class_name, config, java_home=None, maven_settings=None,
                   args=None, jvm_args=None, project_dir=None):
    """Run Java class with Maven classpath"""

    # Override config with command line arguments
    if java_home:
        config['java_home'] = java_home
    if maven_settings:
        config['maven_settings'] = maven_settings

    # Resolve class name if it's a file path
    class_name = resolve_class_name(class_name)

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

    # Get Maven classpath
    classpath = get_maven_classpath(
        config['maven_home'],
        config['maven_settings'],
        project_dir
    )

    # Add target/classes to classpath
    target_classes = project_dir / 'target' / 'classes'
    if target_classes.exists():
        classpath = str(target_classes) + os.pathsep + classpath

    # Build Java command
    java_cmd = os.path.join(config['java_home'], 'bin', 'java')
    if sys.platform == 'win32':
        java_cmd += '.exe'

    cmd = [java_cmd]

    # Add JVM arguments
    if jvm_args:
        cmd.extend(jvm_args.split())
    elif config.get('default_jvm_args'):
        cmd.extend(config['default_jvm_args'])

    # Add classpath
    cmd.extend(['-cp', classpath])

    # Add main class
    cmd.append(class_name)

    # Add program arguments
    if args:
        cmd.extend(args.split())

    # Run command
    print(f"Running: {class_name}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 80)

    try:
        result = subprocess.run(cmd, cwd=project_dir)
        return result.returncode
    except Exception as e:
        print(f"Error running Java class: {e}", file=sys.stderr)
        return 1


def main():
    parser = argparse.ArgumentParser(
        description='Run Java main class with Maven classpath'
    )
    parser.add_argument('class_name', help='Fully qualified class name or file path')
    parser.add_argument('--config', help='Path to config.json file')
    parser.add_argument('--java-home', help='Java home directory')
    parser.add_argument('--maven-settings', help='Maven settings.xml path')
    parser.add_argument('--args', help='Program arguments')
    parser.add_argument('--jvm-args', help='JVM arguments')
    parser.add_argument('--project-dir', help='Project directory (default: auto-detect)')

    parsed_args = parser.parse_args()

    # Load configuration
    config = load_config(parsed_args.config)

    # Run Java class
    return run_java_class(
        parsed_args.class_name,
        config,
        java_home=parsed_args.java_home,
        maven_settings=parsed_args.maven_settings,
        args=parsed_args.args,
        jvm_args=parsed_args.jvm_args,
        project_dir=parsed_args.project_dir
    )


if __name__ == "__main__":
    sys.exit(main())
