#!/usr/bin/env python3
"""
Script CLI para ejecutar el servicio de scraping
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.scraping_service import main

if __name__ == "__main__":
    exit(main())

