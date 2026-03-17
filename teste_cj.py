import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from cj.services import buscar_produtos_cj

print("🔍 Buscando produtos de bijuterias no CJ...")
produtos = buscar_produtos_cj(keyword="jewelry necklace", page_size=5)

if produtos:
    print(f"✅ {len(produtos)} produtos encontrados!")
    for p in produtos:
        print(f"  - {p.get('productNameEn')} | ${p.get('sellPrice')}")
else:
    print("❌ Nenhum produto encontrado ou erro na conexão.")