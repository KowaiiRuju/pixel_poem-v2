#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convenience entrypoint / alias for 'Top 10 (up to 2026).py'
"""
import sys
import importlib.util
from pathlib import Path

target_file = Path(__file__).resolve().parent / "Top 10 (up to 2026).py"

spec = importlib.util.spec_from_file_location("top_10_up_to_2026", str(target_file))
module = importlib.util.module_from_spec(spec)
sys.modules["top_10_up_to_2026"] = module
spec.loader.exec_module(module)

if __name__ == "__main__":
    module.main()
