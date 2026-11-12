#!/usr/bin/env python3
"""Gera texturas, modelos, JSONs de dados e traducoes do mod Starfall. Uso: python3 tools/generate_assets.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen"))
import blocks_tex, items_tex, rigs, data   # noqa: E402

if __name__ == "__main__":
    blocks_tex.run()
    items_tex.run()
    rigs.run()
    data.run()
    print("OK: assets gerados.")
