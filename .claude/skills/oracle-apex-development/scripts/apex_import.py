#!/usr/bin/env python3
"""
Oracle APEX Application Import Utility
Imports APEX applications to Oracle database
"""

import argparse
import subprocess
import os

def import_apex_app(host, port, service, username, password, file_path, workspace):
    """Import APEX application using SQLcl"""
    
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        return False
    
    sqlcl_commands = f"""
    SET DEFINE OFF
    WHENEVER SQLERROR EXIT SQL.SQLCODE
    
    BEGIN
        apex_application_install.set_workspace('{workspace}');
        apex_application_install.generate_offset;
        apex_application_install.set_schema('&APP_SCHEMA.');
        apex_application_install.set_application_alias('&APP_ALIAS.');
    END;
    /
    
    @{file_path}
    
    COMMIT;
    
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
            print(f"✓ Application imported successfully to workspace: {workspace}")
            print(f"  From file: {file_path}")
            return True
        else:
            print(f"✗ Import failed: {stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Import Oracle APEX application')
    parser.add_argument('--host', required=True, help='Database host')
    parser.add_argument('--port', default='1521', help='Database port')
    parser.add_argument('--service', required=True, help='Database service name')
    parser.add_argument('--username', required=True, help='Database username')
    parser.add_argument('--password', required=False, help='Database password')
    parser.add_argument('--file', required=True, help='APEX application file (.sql)')
    parser.add_argument('--workspace', required=True, help='Target workspace')
    
    args = parser.parse_args()
    
    # Prompt for password if not provided
    if not args.password:
        import getpass
        args.password = getpass.getpass('Password: ')
    
    # Import application
    success = import_apex_app(
        args.host, args.port, args.service,
        args.username, args.password,
        args.file, args.workspace
    )
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
