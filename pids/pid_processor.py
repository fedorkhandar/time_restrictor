import psutil
import subprocess
import json
import ctypes
from ctypes import wintypes


class PidProcessor:
    def __init__(self):
        # Constants from Windows API
        self.SW_FORCEMINIMIZE = 11
        self.SW_MINIMIZE = 6
        self.SW_SHOWMINIMIZED = 2

        # Load user32.dll
        self.user32 = ctypes.WinDLL('user32')
        self.kernel32 = ctypes.WinDLL('kernel32')

        # Set up function prototypes
        self.user32.GetWindowThreadProcessId.restype = wintypes.DWORD
        self.user32.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))

        self.user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
        self.user32.IsWindowVisible.argtypes = (wintypes.HWND,)

    
    # def get_processes(self):
    #     """Get list of current processes"""
    #     processes = []
    #     for proc in psutil.process_iter(['pid', 'name', 'exe']):
    #         try:
    #             processes.append({
    #                 'pid': proc.info['pid'],
    #                 'name': proc.info['name'],
    #                 'exe': proc.info['exe'] or 'N/A'
    #             })
    #         except (psutil.NoSuchProcess, psutil.AccessDenied):
    #             # Skip processes that can't be accessed
    #             continue
    #     return processes

    def get_windows(self):
        """Get list of current windows"""
        try:
            # Use PowerShell to get window information
            cmd = [
                'powershell', 
                '-Command',
                'Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object Id, ProcessName, MainWindowTitle | ConvertTo-Json'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and result.stdout.strip():
                try:
                    windows_data = json.loads(result.stdout)
                    # Handle both single object and array
                    if isinstance(windows_data, dict):
                        windows_data = [windows_data]
                    elif not isinstance(windows_data, list):
                        windows_data = []
                    
                    windows = []
                    for window in windows_data:
                        windows.append({
                            'pid': window.get('Id', 'N/A'),
                            'process_name': window.get('ProcessName', 'N/A'),
                            'title': window.get('MainWindowTitle', 'N/A')
                        })
                    return windows
                except json.JSONDecodeError:
                    return []
            else:
                return []
        except Exception:
            # Fallback method using psutil
            windows = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Check if process has windows (this is limited)
                    if proc.name():
                        windows.append({
                            'pid': proc.info['pid'],
                            'process_name': proc.info['name'],
                            'title': 'Unknown'  # psutil can't easily get window titles
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return windows
    
    # def freeze_process(self, pid):
    #     """Freeze a process by PID using Windows Taskkill command"""
    #     try:
    #         # Convert pid to integer if it's a string
    #         pid = int(pid)
            
    #         # Use taskkill to suspend the process
    #         # /PID specifies the process ID
    #         # /F forces the process to terminate (you might want to remove this for just freezing)
    #         cmd = ['taskkill', '/PID', str(pid), '/F']
            
    #         result = subprocess.run(cmd, capture_output=True, text=True)
            
    #         if result.returncode == 0:
    #             return True, f"Process {pid} terminated successfully"
    #         else:
    #             return False, f"Failed to terminate process {pid}: {result.stderr}"
                
    #     except ValueError:
    #         return False, "Invalid PID: must be a number"
    #     except Exception as e:
    #         return False, f"Error freezing process: {str(e)}"
    
    # def suspend_process(self, pid):
    #     """Suspend a process by PID (pause it without terminating)"""
    #     try:
    #         pid = int(pid)
    #         proc = psutil.Process(pid)
            
    #         # Suspend the process
    #         proc.suspend()
    #         return True, f"Process {pid} ({proc.name()}) suspended successfully"
            
    #     except psutil.NoSuchProcess:
    #         return False, f"Process {pid} not found"
    #     except psutil.AccessDenied:
    #         return False, f"Access denied to process {pid} - try running as administrator"
    #     except ValueError:
    #         return False, "Invalid PID: must be a number"
    #     except Exception as e:
    #         return False, f"Error suspending process: {str(e)}"
        
    # def resume_process(self, pid):
    #     """Resume a suspended process by PID"""
    #     try:
    #         pid = int(pid)
    #         proc = psutil.Process(pid)
            
    #         # Resume the process
    #         proc.resume()
    #         return True, f"Process {pid} ({proc.name()}) resumed successfully"
            
    #     except psutil.NoSuchProcess:
    #         return False, f"Process {pid} not found"
    #     except psutil.AccessDenied:
    #         return False, f"Access denied to process {pid} - try running as administrator"
    #     except ValueError:
    #         return False, "Invalid PID: must be a number"
    #     except Exception as e:
    #         return False, f"Error resuming process: {str(e)}"
    #     """Resume a suspended process by PID"""
    #     try:
    #         # Convert pid to integer if it's a string
    #         pid = int(pid)
            
    #         # Use PowerShell to resume the process
    #         cmd = [
    #             'powershell',
    #             '-Command',
    #             f'Get-Process -Id {pid} | ForEach-Object {{ $_.Resume() }}'
    #         ]
            
    #         result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
    #         if result.returncode == 0:
    #             return True, f"Process {pid} resumed successfully"
    #         else:
    #             # Fallback to using psutil
    #             try:
    #                 proc = psutil.Process(pid)
    #                 proc.resume()
    #                 return True, f"Process {pid} resumed successfully"
    #             except psutil.NoSuchProcess:
    #                 return False, f"Process {pid} not found"
    #             except psutil.AccessDenied:
    #                 return False, f"Access denied to process {pid}"
    #             except Exception as e:
    #                 return False, f"Failed to resume process {pid}: {str(e)}"
                    
    #     except ValueError:
    #         return False, "Invalid PID: must be a number"
    #     except Exception as e:
    #         return False, f"Error resuming process: {str(e)}"
        
    def minimize_window_by_pid(self, pid):
        """Minimize all windows belonging to the specified process ID"""
        # Callback function for EnumWindows
        def enum_windows_callback(hwnd, lParam):
            process_id = wintypes.DWORD()
            # Get the process ID associated with this window
            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(process_id))
            
            # Check if this window belongs to our target process
            if process_id.value == pid and self.user32.IsWindowVisible(hwnd):
                # Minimize the window
                self.user32.ShowWindow(hwnd, self.SW_MINIMIZE)
                print(f"Minimized window with handle: {hwnd}")
            return True
        
        # Enumerate all windows
        self.user32.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.c_void_p)(enum_windows_callback), 0)