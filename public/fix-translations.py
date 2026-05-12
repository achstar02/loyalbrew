#!/usr/bin/env python3
"""
Fix corrupted Chinese (zh) translations in app.js
Replaces ?? placeholders with correct Chinese translations
"""

import re

def main():
    # Read the file
    with open('app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chinese translations dictionary (key: english -> chinese)
    # This is a sample - need to fill in all keys
    zh_translations = {
        'mCatHotDrinks': '热饮',
        'mCatColdDrinks': '冷饮', 
        'mCatFood': '食物',
        'mCatDesserts': '甜点',
        'mCatSnacks': '小吃',
        'mCatPromotions': '促销',
    }
    
    print(f"Loaded {len(zh_translations)} Chinese translations")

if __name__ == '__main__':
    main()