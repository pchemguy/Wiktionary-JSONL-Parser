# Windows shell policy

Identify the host executing shell commands. Apply this policy on Windows; other hosts retain their own shell.

These are general policies. If the target project specifically targets PowerShell or defines explicit project-specific shell policies, those requirements override the corresponding general rules below.

## Command rules

- **PowerShell and pwsh are unavailable.** Do not probe for, install or invoke them.
- **CMD is the default shell:** write Windows command lines in CMD syntax and use a `cmd` wrapper only when necessary or explicitly instructed.
- Do not generate PowerShell/pwsh invocations, cmdlets or PowerShell-specific syntax.
- **Run one command per shell call.** Do not chain commands with `&&`, `||`, `&` or multiple command lines. Use separate calls; for a necessary sequence, invoke a temporary `.cmd` script with explicit failure handling.
- **Do not pass pipes, redirection or other shell operations directly in a command line supplied to an agent shell tool.** Put the complete call in a temporary `.cmd` file and invoke only that file. This includes grouping, conditionals, loops and variable assignment; keep complex quoting inside that file too.
- **Do not embed script text in a command line supplied to an agent shell tool, including one-liners or quoted source.** This includes interpreter evaluation arguments and shell command strings. Use either form:
    - Write the source to a temporary script file and invoke that file with its interpreter.
    - Treat the entire call as complex: put it, including any embedded script text, in a temporary `.cmd` file and invoke only that file through the shell tool.
- Git Bash may also be available. **Always invoke Bash commands with `bash -c`**, because the shim executes commands through CMD.

## Probe and recover

run_command or a similar shell tool may invoke PowerShell internally, outside the agent's control. Probe the tool before deciding whether recovery is needed.

1. Run `echo CMDPROBE%SystemDrive%` through the actual shell tool. Inspect output, error and exit status.
    - **Success:** require exit status 0 and `CMDPROBE` followed by the expanded system drive. Skip recovery and proceed to step 3.
    - **PowerShell-related error:** proceed to step 2.
    - **Other failure**, including literal `%SystemDrive%` output: report the blocker and stop the turn.
2. Recover only after a PowerShell-related probe error:
    - Save the exact shim below as `PowerShell.cmd` in the shell tool's **current working directory (CWD)** or an existing writable directory on its effective **PATH**. Use an available filesystem tool.
    - If placed inside a Git repository, add its repository-relative path to `.gitignore`.
    - Retry the same probe through the same shell tool. If setup or retry fails, report the blocker and stop the turn.
    - On success, report the shim location and that commands now execute through CMD.
3. Before using quoted program/script paths, verify a harmless quoted-path command, such as an available program's --help. Continue after the required checks succeed; repeat them when the host or shell tool setup changes.

Preserve unrelated adapters/executables and leave global PATH, registry and client configuration unchanged. Keep the shim and temporary scripts out of version control. Use only harmless commands as probes.

## Antigravity wrapper and shim

Antigravity's reported harness may use:

```text
PowerShell -Command "%CLI%"
PowerShell -Command %CLI%
```

The harness backslash-escapes embedded double quotes as `\"`. The CMD shim decodes that wrapper:

```bat
@echo off

set "CLI=%*"
REM Remove `-Command `
set "CLI=%CLI:~9%"

REM Remove outer quotes, if present
set "QUOTED=\%CLI:~0,1%\%CLI:~-1%"
set "QUOTED={%QUOTED:\"=%}"
if "%QUOTED%"=="{}" (
    set "CLI=%CLI:~1,-1%"
)

set "CLI=%CLI:\"="%"

call %CLI%
```

The shim removes the fixed `-Command ` prefix, strips an optional pair of outer double quotes, restores `\"` to `"`, and invokes the decoded command through CMD with `call`. It targets the two illustrated launcher forms; do not assume another client uses the same argument layout or escaping, or that its launcher can resolve a `.cmd` adapter.
