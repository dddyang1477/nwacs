import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))

archive_dirs = [
    'archive/old-core-scripts',
    'archive/old-core-subsystems',
    'archive/old-v8-scripts',
    'archive/old-v8-docs',
    'archive/old-v8-fix-scripts',
    'archive/old-docs',
    'archive/old-configs',
    'archive/old-learning',
    'archive/old-generators',
    'scripts',
]

for d in archive_dirs:
    path = os.path.join(BASE, d)
    os.makedirs(path, exist_ok=True)
    print(f'Created: {d}')

print('\nAll directories created.')
