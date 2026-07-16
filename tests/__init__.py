__init__.py para o pacote tests
"""

import sys
import os

# Adicionar raiz do projeto ao path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))