@echo off

set "REPO=H:\GitHub\Wiktionary-JSONL-Parser"
set "PYTHONPATH=%REPO%\src;%PYTHONPATH%"

python -m wiktionary_jsonl_parser.cli "%~dpn0.jsonl"
