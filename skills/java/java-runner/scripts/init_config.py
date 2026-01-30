#!/usr/bin/env python3
"""
Initialize or reconfigure java-runner skill

Usage:
    python init_config.py        - Initialize or reset configuration
    python init_config.py show   - Show current configuration
"""

import sys
from pathlib import Path

# Import config manager
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from config_manager import load_config, show_config, reset_config, get_config_path


def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        show_config()
    else:
        config_dir, config_file = get_config_path()

        if config_file.exists():
            print(f"配置文件已存在: {config_file}\n")
            choice = input("是否要重新配置？(y/N): ").strip().lower()
            if choice == 'y':
                reset_config()
            else:
                print("保持现有配置")
                show_config()
        else:
            print("开始初始化配置...\n")
            load_config()


if __name__ == "__main__":
    main()
