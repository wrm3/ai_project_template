import platform
import os
import psutil
import json

class SystemInfo:
    @staticmethod
    def get_os_info():
        """Get detailed information about the operating system."""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'architecture': platform.architecture(),
            'node': platform.node()
        }
    
    @staticmethod
    def get_memory_info():
        """Get system memory information."""
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free
        }
    
    @staticmethod
    def get_disk_info():
        """Get disk usage information for all mounted partitions."""
        disk_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.mountpoint] = {
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            except Exception:
                continue
        return disk_info

    @staticmethod
    def get_all_info():
        """Get all system information in a single call."""
        return {
            'os': SystemInfo.get_os_info(),
            'memory': SystemInfo.get_memory_info(),
            'disk': SystemInfo.get_disk_info()
        }

    @staticmethod
    def to_json(info):
        """Convert system information to JSON string."""
        return json.dumps(info, indent=2)

if __name__ == '__main__':
    # Example usage
    system_info = SystemInfo()
    all_info = system_info.get_all_info()
    print(SystemInfo.to_json(all_info)) 