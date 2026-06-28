#!/usr/bin/env python3
"""Render MoneyPrinterTurbo config from environment variables.

Usage
-----
- Called by docker entrypoint or local startup tooling.
- Patches only a minimal DeepSeek-related subset to avoid touching unrelated configs.

Supported variables
-----------------
- MPT_LLM_PROVIDER
- MPT_DEEPSEEK_API_KEY
- MPT_DEEPSEEK_BASE_URL
- MPT_DEEPSEEK_MODEL_NAME

Fallbacks:
- DEEPSEEK_API_KEY
- DEEPSEEK_BASE_URL
- DEEPSEEK_MODEL_NAME

When a target variable is empty, this script keeps existing config value.
"""

import json
import os
import re
import shutil
from pathlib import Path


DEFAULT_CONFIG_PATH = "/MoneyPrinterTurbo/config.toml"
DEFAULT_EXAMPLE_PATH = "/MoneyPrinterTurbo/config.example.toml"


def read_config_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_config_exists(config_path: Path, example_path: Path) -> None:
    if config_path.exists():
        return

    if not example_path.exists():
        raise SystemExit(f"missing config template: {example_path}")

    shutil.copyfile(example_path, config_path)
    print(f"init config.toml from template: {config_path}")


def load_dotenv_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"\'')
        values[key] = value
    return values


def get_env_value(candidates: list[str], file_values: dict[str, str]) -> str:
    for name in candidates:
        if name in os.environ and os.environ[name].strip():
            return os.environ[name].strip()
        if name in file_values and file_values[name].strip():
            return file_values[name].strip()
    return ""


def patch_line(text: str, key: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf"^(?P<prefix>\s*{re.escape(key)}\s*=)\s*.*$", re.M)
    if not pattern.search(text):
        return text, False

    replacement = rf"\g<prefix> {json.dumps(value)}"
    return pattern.sub(replacement, text, count=1), True


def main() -> None:
    config_path = Path(os.getenv("MPT_CONFIG_PATH", DEFAULT_CONFIG_PATH))
    example_path = Path(os.getenv("MPT_CONFIG_EXAMPLE_PATH", DEFAULT_EXAMPLE_PATH))
    env_path = Path(os.getenv("MPT_ENV_FILE", "/MoneyPrinterTurbo/.env"))

    env_values = load_dotenv_file(env_path)
    ensure_config_exists(config_path, example_path)

    config_text = read_config_text(config_path)
    original = config_text

    updates = {
        "llm_provider": get_env_value(
            ["MPT_LLM_PROVIDER", "LLM_PROVIDER"], env_values
        ),
        "deepseek_api_key": get_env_value(
            ["MPT_DEEPSEEK_API_KEY", "DEEPSEEK_API_KEY"], env_values
        ),
        "deepseek_base_url": get_env_value(
            ["MPT_DEEPSEEK_BASE_URL", "DEEPSEEK_BASE_URL", "MPT_DEEPSEEK_BASE"],
            env_values,
        ),
        "deepseek_model_name": get_env_value(
            ["MPT_DEEPSEEK_MODEL_NAME", "DEEPSEEK_MODEL_NAME", "MPT_DEEPSEEK_MODEL"],
            env_values,
        ),
    }

    applied = []
    for key, value in updates.items():
        if not value:
            continue
        new_text, changed = patch_line(config_text, key, value)
        if changed:
            config_text = new_text
            applied.append(key)

    if config_text != original:
        config_path.write_text(config_text, encoding="utf-8")

    if applied:
        print("rendered config.toml with:", ", ".join(applied))


if __name__ == "__main__":
    main()
