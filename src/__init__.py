"""
src package initialization for IDS Forge
"""
import os
import sys

# Ensure src package directory is accessible on sys.path
package_dir = os.path.dirname(os.path.abspath(__file__))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)
