#!/usr/bin/env python
"""Teste rápido de importação e inicialização."""
import sys

print("Testando importações e inicialização do backend...")

try:
    print("✓ Importando módulos básicos...", end=" ")
    from app.main import app
    from app.core.database import Base, engine
    print("OK")
    
    print("✓ Importando todos os models...", end=" ")
    import app.models.usuarios
    import app.models.veiculos
    import app.models.condutores
    import app.models.manutencao
    import app.models.multas
    import app.models.chat
    print("OK")
    
    print("✓ Verificando app FastAPI...", end=" ")
    assert app is not None
    print("OK")
    
    print("\n✅ BACKEND PRONTO PARA INICIAR!")
    sys.exit(0)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
