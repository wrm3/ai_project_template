#!/usr/bin/env python3
"""
Oracle APEX Workspace Backup Utility
Backs up all applications in a workspace
"""

import argparse
import subprocess
import os
from datetime import datetime

def get_workspace_apps(host, port, service, username, password, workspace):
    """Get list of applications in workspace"""
    query = f"""
    SELECT application_id, application_name
    FROM apex_applications
    WHERE workspace = '{workspace}'
    ORDER BY application_id
    """
    
    connection_string = f"{username}/{password}@{host}:{port}/{service}"
    
    try:
        process = subprocess.Popen(
            ['sql', '-S', connection_string],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(f"SET PAGESIZE 0 FEEDBACK OFF\n{query}\nexit")
        
        apps = []
        for line in stdout.strip().split('\n'):
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    apps.append((int(parts[0]), ' '.join(parts[1:])))
        
        return apps
        
    except Exception as e:
        print(f"✗ Error getting applications: {str(e)}")
        return []

def backup_workspace(host, port, service, username, password, workspace, output_dir):
    """Backup all applications in workspace"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(output_dir, f'{workspace}_{timestamp}')
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"Backing up workspace: {workspace}")
    print(f"Output directory: {backup_dir}\n")
    
    # Get applications
    apps = get_workspace_apps(host, port, service, username, password, workspace)
    
    if not apps:
        print("No applications found or error occurred")
        return False
    
    print(f"Found {len(apps)} applications\n")
    
    # Export each application
    success_count = 0
    for app_id, app_name in apps:
        print(f"Exporting {app_id}: {app_name}...")
        
        from apex_export import export_apex_app
        if export_apex_app(host, port, service, username, password, 
                          app_id, backup_dir):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Backup completed: {success_count}/{len(apps)} applications exported")
    print(f"{'='*60}")
    
    return success_count == len(apps)

def main():
    parser = argparse.ArgumentParser(description='Backup Oracle APEX workspace')
    parser.add_argument('--host', required=True, help='Database host')
    parser.add_argument('--port', default='1521', help='Database port')
    parser.add_argument('--service', required=True, help='Database service name')
    parser.add_argument('--username', required=True, help='Database username')
    parser.add_argument('--password', required=False, help='Database password')
    parser.add_argument('--workspace', required=True, help='Workspace name')
    parser.add_argument('--output-dir', default='./backups', help='Output directory')
    
    args = parser.parse_args()
    
    # Prompt for password if not provided
    if not args.password:
        import getpass
        args.password = getpass.getpass('Password: ')
    
    # Backup workspace
    success = backup_workspace(
        args.host, args.port, args.service,
        args.username, args.password,
        args.workspace, args.output_dir
    )
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
