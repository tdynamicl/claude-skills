#!/usr/bin/env python3
"""
Configuration manager for java-runner skill

Manages configuration stored in ~/.skills/java-skill.conf
"""

import os
import json
from pathlib import Path


def get_config_path():
    """Get the path to the configuration file"""
    home = Path.home()
    config_dir = home / '.skills'
    config_file = config_dir / 'java-skill.conf'
    return config_dir, config_file


def prompt_for_config():
    """Prompt user to input configuration values"""
    print("=" * 80)
    print("Java Runner Skill - 首次配置")
    print("=" * 80)
    print("\n配置文件不存在，请输入以下配置信息：\n")

    config = {}

    # Java Home
    java_home_default = os.environ.get('JAVA_HOME', '')
    if java_home_default:
        java_home_prompt = f"Java Home 路径 (默认: {java_home_default}): "
    else:
        java_home_prompt = "Java Home 路径 (例如: C:/Program Files/Java/jdk-17): "

    java_home = input(java_home_prompt).strip()
    if not java_home and java_home_default:
        java_home = java_home_default
    config['java_home'] = java_home

    # Maven Home
    maven_home_default = os.environ.get('MAVEN_HOME', '')
    if maven_home_default:
        maven_home_prompt = f"Maven Home 路径 (默认: {maven_home_default}): "
    else:
        maven_home_prompt = "Maven Home 路径 (例如: C:/apache-maven-3.9.0): "

    maven_home = input(maven_home_prompt).strip()
    if not maven_home and maven_home_default:
        maven_home = maven_home_default
    config['maven_home'] = maven_home

    # Maven Settings
    default_settings = str(Path.home() / '.m2' / 'settings.xml')
    maven_settings_prompt = f"Maven settings.xml 路径 (可选，默认: {default_settings}，直接回车跳过): "
    maven_settings = input(maven_settings_prompt).strip()
    if not maven_settings:
        # Check if default settings.xml exists
        if Path(default_settings).exists():
            maven_settings = default_settings
        else:
            maven_settings = ""
    config['maven_settings'] = maven_settings

    # Default JVM Args
    print("\n默认 JVM 参数 (可选，多个参数用空格分隔，例如: -Xmx2g -Xms512m)")
    jvm_args_input = input("JVM 参数 (直接回车跳过): ").strip()
    if jvm_args_input:
        config['default_jvm_args'] = jvm_args_input.split()
    else:
        config['default_jvm_args'] = []

    # Default Maven Args
    print("\n默认 Maven 参数 (可选，多个参数用空格分隔)")
    maven_args_input = input("Maven 参数 (直接回车跳过): ").strip()
    if maven_args_input:
        config['default_maven_args'] = maven_args_input.split()
    else:
        config['default_maven_args'] = []

    return config


def save_config(config):
    """Save configuration to file"""
    config_dir, config_file = get_config_path()

    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)

    # Save configuration
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"\n✓ 配置已保存到: {config_file}")


def load_config(custom_config_path=None):
    """
    Load configuration from file

    Priority:
    1. Custom config path (if provided)
    2. ~/.skills/java-skill.conf
    3. Environment variables
    4. Prompt user for input (first time)
    """
    # If custom config path is provided, use it
    if custom_config_path:
        custom_path = Path(custom_config_path)
        if custom_path.exists():
            with open(custom_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"警告: 指定的配置文件不存在: {custom_config_path}")
            print("将使用默认配置文件")

    # Try to load from default location
    config_dir, config_file = get_config_path()

    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    else:
        # First time setup - prompt user
        print(f"\n配置文件不存在: {config_file}")
        print("开始首次配置...\n")

        config = prompt_for_config()
        save_config(config)

        print("\n配置完成！现在可以使用 java-runner 了。")
        print(f"\n如需修改配置，请编辑: {config_file}")
        print("=" * 80)
        print()

        return config


def show_config():
    """Display current configuration"""
    config_dir, config_file = get_config_path()

    if not config_file.exists():
        print(f"配置文件不存在: {config_file}")
        return

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("=" * 80)
    print(f"当前配置 ({config_file})")
    print("=" * 80)
    print(json.dumps(config, indent=2, ensure_ascii=False))
    print("=" * 80)


def reset_config():
    """Reset configuration by prompting user again"""
    config = prompt_for_config()
    save_config(config)
    print("\n配置已重置！")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'show':
            show_config()
        elif command == 'reset':
            reset_config()
        else:
            print("用法:")
            print("  python config_manager.py show   - 显示当前配置")
            print("  python config_manager.py reset  - 重置配置")
    else:
        # Test loading config
        config = load_config()
        print("\n配置加载成功！")
        show_config()
