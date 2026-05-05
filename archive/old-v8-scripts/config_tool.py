#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Configuration Tool
Features: Auto-start settings, sensitivity filter, DeepSeek V4 connection
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'core'))

from nwacs_manager import NWACSManager

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("    NWACS Configuration Tool")
    print("=" * 60)

    manager = NWACSManager()

    auto_start = manager.check_auto_start()
    sensitivity = manager.config.get('sensitivity', {})
    model_version = manager.config.get('model_version', 'Unknown')

    print("\n[Current Status]")
    print("-" * 40)
    print("* DeepSeek Version:", model_version)
    print("* Sensitivity Filter Type:", sensitivity.get('content_type', 'Not set'))
    print("* Auto Start:", 'Enabled' if auto_start.get('enabled') else 'Disabled')

    while True:
        print("\n[Options]")
        print("-" * 40)
        print("1. Configure DeepSeek V4")
        print("2. Set Sensitivity Filter (Political only)")
        print("3. Enable Auto Start")
        print("4. Disable Auto Start")
        print("5. View Full Configuration")
        print("0. Exit")

        choice = input("\nEnter your choice [0-5]: ").strip()

        if choice == '1':
            configure_deepseek_v4(manager)
        elif choice == '2':
            manager.set_sensitivity_filter('political')
            print("\nSensitivity filter set to: political")
        elif choice == '3':
            manager.enable_auto_start()
        elif choice == '4':
            manager.disable_auto_start()
        elif choice == '5':
            manager.show_config()
        elif choice == '0':
            print("\nConfiguration completed!")
            break
        else:
            print("Invalid choice, please try again")

def configure_deepseek_v4(manager):
    """Configure DeepSeek V4"""
    print("\n[Configure DeepSeek V4]")
    print("-" * 40)
    print("DeepSeek V4 API Configuration:")
    print("* API URL: https://api.deepseek.com/v1")
    print("* Model: deepseek-chat")
    print("* Get API Key from DeepSeek official website")
    print("\nVisit https://platform.deepseek.com/ to get your API Key")

    api_key = input("\nEnter DeepSeek API Key: ").strip()

    if api_key:
        manager.config['api_key'] = api_key
        manager.config['base_url'] = 'https://api.deepseek.com/v1'
        manager.config['model'] = 'deepseek-chat'
        manager.config['model_version'] = 'v4'
        manager.config['enabled'] = True
        manager._save_config()

        print("\nConfiguration successful!")
        print("  API URL: https://api.deepseek.com/v1")
        print("  Model: deepseek-chat")
        print("  Version: v4")
    else:
        print("\nNo API Key entered, configuration not saved")

if __name__ == "__main__":
    main()