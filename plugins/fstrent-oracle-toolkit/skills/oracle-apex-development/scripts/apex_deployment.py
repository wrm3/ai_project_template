#!/usr/bin/env python3
"""
Oracle APEX Multi-Environment Deployment
Deploys APEX applications to multiple environments
"""

import yaml
import argparse
from apex_export import export_apex_app
from apex_import import import_apex_app

def load_config(config_file):
    """Load deployment configuration from YAML"""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def deploy_to_environment(config, env_name, app_id, version):
    """Deploy application to specific environment"""
    env = config['environments'][env_name]
    
    print(f"\n{'='*60}")
    print(f"Deploying to {env_name.upper()}")
    print(f"{'='*60}")
    
    # Export from source
    source = config['source']
    temp_file = f'/tmp/f{app_id}_{version}.sql'
    
    print("\n1. Exporting from source...")
    if not export_apex_app(
        source['host'], source['port'], source['service'],
        source['username'], source['password'],
        app_id, '/tmp'
    ):
        return False
    
    # Import to target
    print(f"\n2. Importing to {env_name}...")
    if not import_apex_app(
        env['host'], env['port'], env['service'],
        env['username'], env['password'],
        temp_file, env['workspace']
    ):
        return False
    
    print(f"\n✓ Deployment to {env_name} completed successfully")
    return True

def main():
    parser = argparse.ArgumentParser(description='Deploy APEX application')
    parser.add_argument('--config', required=True, help='Deployment config file (YAML)')
    parser.add_argument('--app-id', required=True, type=int, help='Application ID')
    parser.add_argument('--version', required=True, help='Version number')
    parser.add_argument('--env', required=True, choices=['dev', 'test', 'prod'],
                       help='Target environment')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Deploy
    success = deploy_to_environment(config, args.env, args.app_id, args.version)
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
