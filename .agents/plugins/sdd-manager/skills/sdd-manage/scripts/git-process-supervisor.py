"""Own one private publication worker and its descendants (Python 3.11+).

The Node publication controller supplies one bounded JSON request on stdin,
followed by an optional "cancel" line. EOF means the controller disappeared.
Worker input contains scope/options, never credential values. Only fixed-shape
supervision metadata is emitted here; worker protocol output shares stdout.

Windows assigns a suspended worker to a non-breakaway, kill-on-close Job Object.
Linux creates an isolated process group and becomes a child subreaper so orphaned
descendants can be killed and reaped. No shell or image-name process killing,
credential access, permission repair, external package or import effect is used.
This is a private backend, not a general-purpose public command interface.
"""
import ctypes
import json
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path


def emit(value):
    """Write ASCII protocol metadata, never exception text or command arguments."""
    sys.stdout.write(json.dumps(value, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def feed(write, close, data):
    """Deliver bounded worker input without blocking the supervision loop."""
    try:
        write(data)
    except (OSError, ValueError):
        pass
    finally:
        try:
            close()
        except OSError:
            pass


class LinuxTree:
    """Own a new session and reap descendants adopted by this process only."""
    def __init__(self):
        self.process = None
        # /proc can be mounted from an outer PID namespace. Use its visible
        # identity for relation checks, translating only verified children back
        # to this process's namespace before kill(2).
        visible = Path('/proc/self').resolve()
        self.visible_pid = int(visible.name)
        status = (visible / 'status').read_text()
        namespaces = next(line.split()[1:] for line in status.splitlines()
                          if line.startswith('NSpid:'))
        if int(namespaces[-1]) != os.getpid():
            raise OSError('supervision_unavailable')
        self.namespace_index = len(namespaces) - 1
        self.children_file = visible / 'task' / visible.name / 'children'
        # Some kernels omit the task/children interface. /proc relation checks
        # remain available there; only our own adopted children are eligible.
        self.children_interface = self.children_file.exists()
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(36, 1, 0, 0, 0) != 0:  # PR_SET_CHILD_SUBREAPER
            raise OSError("supervision_unavailable")

    def start(self, command, data):
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE,
                                        start_new_session=True)
        threading.Thread(target=feed, args=(self.process.stdin.write,
                         self.process.stdin.close, data), daemon=True).start()
        return self.process.pid

    def poll(self):
        return self.process.poll()

    def cleanup(self, deadline):
        if self.process is None:
            return True
        try:
            os.killpg(self.process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError:
            return False
        while time.monotonic() < deadline:
            self.process.poll()
            try:
                while True:
                    child, _ = os.waitpid(-1, os.WNOHANG)
                    if child == 0:
                        break
            except ChildProcessError:
                return True
            # A descendant that created another session is still our adopted
            # child after its parent dies. Verify that relation before killing.
            try:
                candidates = self.children_file.read_text().split() if self.children_interface else (
                    entry.name for entry in Path('/proc').iterdir() if entry.name.isdecimal())
                for item in candidates:
                    if time.monotonic() >= deadline:
                        return False
                    pid = int(item)
                    stat = Path("/proc") / str(pid) / "stat"
                    try:
                        raw = stat.read_text()
                        fields = raw[raw.rfind(")") + 2:].split()
                        if int(fields[1]) == self.visible_pid:
                            status = stat.with_name('status').read_text()
                            namespaces = next(line.split()[1:] for line in status.splitlines()
                                              if line.startswith('NSpid:'))
                            local_pid = int(namespaces[self.namespace_index])
                            os.kill(local_pid, signal.SIGKILL)
                    except (FileNotFoundError, ProcessLookupError):
                        pass
            except (OSError, ValueError, IndexError):
                return False
            time.sleep(0.01)
        return False

    def close(self):
        pass


class WindowsTree:
    """Create the process suspended, assign its Job Object, then resume it."""
    def __init__(self):
        from ctypes import wintypes as w
        self.w, self.process, self.thread, self.job = w, None, None, None
        self.input_fd = None
        self.k = ctypes.WinDLL("kernel32", use_last_error=True)
        size = ctypes.c_size_t

        class Startup(ctypes.Structure):
            _fields_ = [("cb", w.DWORD), ("reserved", w.LPWSTR),
                        ("desktop", w.LPWSTR), ("title", w.LPWSTR),
                        ("x", w.DWORD), ("y", w.DWORD), ("xs", w.DWORD),
                        ("ys", w.DWORD), ("xc", w.DWORD), ("yc", w.DWORD),
                        ("fill", w.DWORD), ("flags", w.DWORD),
                        ("show", w.WORD), ("reserved_size", w.WORD),
                        ("reserved_bytes", ctypes.POINTER(w.BYTE)),
                        ("stdin", w.HANDLE), ("stdout", w.HANDLE),
                        ("stderr", w.HANDLE)]

        class ProcessInfo(ctypes.Structure):
            _fields_ = [("process", w.HANDLE), ("thread", w.HANDLE),
                        ("pid", w.DWORD), ("tid", w.DWORD)]

        class Limits(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_longlong),
                        ("job_time", ctypes.c_longlong), ("flags", w.DWORD),
                        ("min_ws", size), ("max_ws", size),
                        ("active_limit", w.DWORD), ("affinity", size),
                        ("priority", w.DWORD), ("scheduling", w.DWORD)]

        class Extended(ctypes.Structure):
            _fields_ = [("basic", Limits), ("io", ctypes.c_ulonglong * 6),
                        ("process_memory", size), ("job_memory", size),
                        ("peak_process_memory", size), ("peak_job_memory", size)]

        class Accounting(ctypes.Structure):
            _fields_ = [("times", ctypes.c_longlong * 4),
                        ("page_faults", w.DWORD), ("total", w.DWORD),
                        ("active", w.DWORD), ("terminated", w.DWORD)]

        self.Startup, self.ProcessInfo = Startup, ProcessInfo
        self.Extended, self.Accounting = Extended, Accounting
        signatures = {
            "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
            "QueryInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD, ctypes.c_void_p], w.BOOL),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "TerminateProcess": ([w.HANDLE, w.UINT], w.BOOL),
            "ResumeThread": ([w.HANDLE], w.DWORD),
            "WaitForSingleObject": ([w.HANDLE, w.DWORD], w.DWORD),
            "GetExitCodeProcess": ([w.HANDLE, ctypes.POINTER(w.DWORD)], w.BOOL),
            "CloseHandle": ([w.HANDLE], w.BOOL),
            "CreateProcessW": ([w.LPCWSTR, w.LPWSTR, ctypes.c_void_p,
                               ctypes.c_void_p, w.BOOL, w.DWORD,
                               ctypes.c_void_p, w.LPCWSTR,
                               ctypes.POINTER(Startup), ctypes.POINTER(ProcessInfo)], w.BOOL),
        }
        for name, (arguments, result) in signatures.items():
            function = getattr(self.k, name)
            function.argtypes, function.restype = arguments, result

    def start(self, command, data):
        import msvcrt
        self.job = self.k.CreateJobObjectW(None, None)
        limits = self.Extended()
        limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.job or not self.k.SetInformationJobObject(
                self.job, 9, ctypes.byref(limits), ctypes.sizeof(limits)):
            raise OSError("supervision_unavailable")
        read_fd, self.input_fd = os.pipe()
        try:
            startup, info = self.Startup(), self.ProcessInfo()
            startup.cb, startup.flags = ctypes.sizeof(startup), 0x100
            startup.stdin = msvcrt.get_osfhandle(read_fd)
            startup.stdout = msvcrt.get_osfhandle(sys.stdout.fileno())
            startup.stderr = msvcrt.get_osfhandle(sys.stderr.fileno())
            for handle in (startup.stdin, startup.stdout, startup.stderr):
                os.set_handle_inheritable(handle, True)
            line = ctypes.create_unicode_buffer(subprocess.list2cmdline(command))
            if not self.k.CreateProcessW(command[0], line, None, None, True,
                                        0x4 | 0x08000000, None, None,
                                        ctypes.byref(startup), ctypes.byref(info)):
                raise OSError("worker_unavailable")
            self.process, self.thread = info.process, info.thread
            if not self.k.AssignProcessToJobObject(self.job, self.process):
                # It has never run, so cannot have created descendants.
                self.k.TerminateProcess(self.process, 1)
                raise OSError("supervision_unavailable")
            if self.k.ResumeThread(self.thread) == 0xFFFFFFFF:
                raise OSError("worker_unavailable")
            self.k.CloseHandle(self.thread)
            self.thread = None
        finally:
            os.close(read_fd)

        write_fd, self.input_fd = self.input_fd, None

        def write(value):
            view = memoryview(value)
            while view:
                view = view[os.write(write_fd, view):]

        threading.Thread(target=feed, args=(write, lambda: os.close(write_fd), data),
                         daemon=True).start()
        return info.pid

    def poll(self):
        state = self.k.WaitForSingleObject(self.process, 0)
        if state == 0x102:  # WAIT_TIMEOUT
            return None
        if state != 0:
            raise OSError("worker_failed")
        value = self.w.DWORD()
        if not self.k.GetExitCodeProcess(self.process, ctypes.byref(value)):
            raise OSError("worker_failed")
        return value.value

    def cleanup(self, deadline):
        if not self.job:
            return self.process is None
        self.k.TerminateJobObject(self.job, 1)
        while time.monotonic() < deadline:
            value = self.Accounting()
            if not self.k.QueryInformationJobObject(
                    self.job, 1, ctypes.byref(value), ctypes.sizeof(value), None):
                return False
            if value.active == 0:
                # Assignment can fail while the worker is still suspended.
                # Confirm that process ended too, even when the job was empty.
                if not self.process or self.k.WaitForSingleObject(self.process, 0) == 0:
                    return True
            time.sleep(0.01)
        return False

    def close(self):
        if self.input_fd is not None:
            os.close(self.input_fd)
        for handle in (self.thread, self.process, self.job):
            if handle:
                self.k.CloseHandle(handle)


def main():
    """Read one bounded private request, supervise it, and certify cleanup."""
    tree, status, code = None, None, "supervision_unavailable"
    cancelled = threading.Event()
    cleanup_deadline = time.monotonic() + 1
    try:
        if sys.version_info < (3, 11):
            raise ValueError("runtime")
        raw = bytearray()
        while b'\n' not in raw and len(raw) <= 65536:
            chunk = os.read(0, min(4096, 65537 - len(raw)))
            if not chunk:
                break
            raw.extend(chunk)
        line, separator, pending = bytes(raw).partition(b'\n')
        if not separator or len(line) > 65535:
            raise ValueError("request")
        request = json.loads(line)
        command, payload = request["command"], request["input"]
        total_ms, cleanup_ms = request["timeout_ms"], request["cleanup_ms"]
        if (not isinstance(command, list) or not command or len(command) > 8
                or not all(isinstance(part, str) and part for part in command)
                or not isinstance(payload, str) or len(payload.encode()) > 60000
                or not isinstance(total_ms, int) or not 100 <= total_ms <= 600000
                or not isinstance(cleanup_ms, int) or not 50 <= cleanup_ms < total_ms):
            raise ValueError("request")
        end = time.monotonic() + total_ms / 1000
        cleanup_deadline = end
        work_end = end - cleanup_ms / 1000

        def controls():
            # EOF also signals owner disappearance, so workers do not survive
            # an ordinary controller exit that closes its control pipe.
            # Unbuffered OS reads avoid a daemon holding Python stdin's buffered
            # lock during interpreter shutdown. Any data or EOF requests stop.
            if not pending:
                os.read(0, 16)
            cancelled.set()

        threading.Thread(target=controls, daemon=True).start()
        if hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, lambda *_: cancelled.set())
        signal.signal(signal.SIGINT, lambda *_: cancelled.set())
        if sys.platform == "win32":
            tree = WindowsTree()
        elif sys.platform.startswith("linux"):
            tree = LinuxTree()
        else:
            raise OSError("supervision_unavailable")
        pid = tree.start(command, payload.encode("utf-8"))
        emit({"kind": "started", "worker_pid": pid})
        while True:
            status = tree.poll()
            if status is not None:
                code = "worker_exit"
                break
            if cancelled.is_set():
                code = "cancelled"
                break
            if time.monotonic() >= work_end:
                code = "process_timeout"
                break
            cancelled.wait(0.01)
    except (OSError, ValueError, KeyError, TypeError, OverflowError):
        code = "supervision_unavailable"
    finally:
        clean = tree is None
        try:
            if tree is not None:
                clean = tree.cleanup(cleanup_deadline)
        except Exception:
            clean = False
        finally:
            if tree is not None:
                try:
                    tree.close()
                except OSError:
                    clean = False
        emit({"kind": "supervisor", "code": code, "worker_status": status,
              "cleanup": "confirmed" if clean else "unconfirmed"})


if __name__ == "__main__":
    main()
