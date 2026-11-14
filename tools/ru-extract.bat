@echo off
setlocal DisableDelayedExpansion

if not defined WIKTIONARY_JSONL_PARSER_ROOT set "WIKTIONARY_JSONL_PARSER_ROOT=%~dp0.."
if defined PYTHONPATH (
    set "PYTHONPATH=%WIKTIONARY_JSONL_PARSER_ROOT%\src;%PYTHONPATH%"
) else (
    set "PYTHONPATH=%WIKTIONARY_JSONL_PARSER_ROOT%\src"
)

if "%~1"=="" (
    python -m wiktionary_jsonl_parser.cli "%~dpn0.jsonl"
) else (
    python -m wiktionary_jsonl_parser.cli %*
)
exit /b %ERRORLEVEL%
