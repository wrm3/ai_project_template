#!/usr/bin/env python3
"""
Oracle APEX Application Export Utility
Exports APEX applications from Oracle database
"""

import argparse
import subprocess
import os
from datetime import datetime

def export_apex_app(host, port, service, username, password, app_id, output_dir):
    """Export APEX application using SQLcl"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(output_dir, f'f{app_id}_{timestamp}.sql')
    
    sqlcl_commands = f"""
    apex export {app_id}
    exit
    """
    
    connection_string = f"{username}/{password}@{host}:{port}/{service}"
    
    try:
        process = subprocess.Popen(
            ['sql', connection_string],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(sqlcl_commands)
        
        if process.returncode == 0:
            print(f"✓ Application {app_id} exported successfully")
            print(f"  Output: {output_file}")
            return True
        else:
            print(f"✗ Export failed: {stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Export Oracle APEX application')
    parser.add_argument('--host', required=True, help='Database host')
    parser.add_argument('--port', default='1521', help='Database port')
    parser.add_argument('--service', required=True, help='Database service name')
    parser.add_argument('--username', required=True, help='Database username')
    parser.add_argument('--password', required=False, help='Database password')
    parser.add_argument('--app-id', required=True, type=int, help='APEX application ID')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    
    args = parser.parse_args()
    
    # Prompt for password if not provided
    if not args.password:
        import getpass
        args.password = getpass.getpass('Password: ')
    
    # Create output directory if not exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Export application
    success = export_apex_app(
        args.host, args.port, args.service, 
        args.username, args.password, 
        args.app_id, args.output_dir
    )
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
