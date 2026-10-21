import sqlite3
import os
from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, flash, g
)
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'solecito-cafe-2025'
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'solecito.db')


# ============================================================
# 🖼️ IMAGEN SORPRESA Y LOGO (editables)
# ============================================================
LOGO_URL = 'https://cdn.phototourl.com/member/2026-10-19-d76a41e0-1774-4d18-a7c0-4055e1bee849.jpg'
IMAGEN_SORPRESA = 'https://cdn.phototourl.com/member/2026-10-19-ff2961e1-530a-4c44-8f23-72771e7f138e.jpg'
MUSICA_SORPRESA = 'starman.mp3.mp3' 

# ============================================================
# REDES SOCIALES (editable)
# ============================================================
REDES = [
    {'nombre': 'Instagram', 'icono': '📸', 'url': 'https://www.instagram.com/solecitocafe.mx?mdxt=YXlmanhnN3ZyajAz'},
    {'nombre': 'Facebook',  'icono': '👍🏻', 'url': 'https://www.facebook.com/share/14tBt6tBA3W/'},
    {'nombre': 'TikTok',    'icono': '⏯️', 'url': 'https://www.tiktok.com/@solecitocafe.mx?_r=1&_t=ZS-9AfrXzRp3zA'},
    {'nombre': 'WhatsApp',  'icono': '📍', 'url': 'https://maps.app.goo.gl/q35vTxaoBsiAGjWB6'},
]


# ============================================================
# BASE DE DATOS Y MENÚ REAL
# ============================================================
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, precio REAL NOT NULL, categoria TEXT NOT NULL, descripcion TEXT DEFAULT \'\', imagen TEXT DEFAULT \'\')')
        
    c.execute('CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT NOT NULL, telefono TEXT DEFAULT \'\', direccion TEXT DEFAULT \'\', notas TEXT DEFAULT \'\', total REAL NOT NULL, detalle TEXT NOT NULL, fecha TEXT NOT NULL)')

    c.execute('SELECT COUNT(*) FROM productos')
    if c.fetchone()[0] == 0:
        # AQUÍ ESTÁN LAS IMÁGENES EXACTAS DE TU CÓDIGO ORIGINAL
        ejemplos = [
            ('Tradicional', 65.0, 'Latte', 'Jarabe casero', 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&q=80'),
            ('Vainilla / Vainilla Light', 75.0, 'Latte', 'Jarabe casero', 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80'),
            ('Mazapán', 75.0, 'Latte', '', 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&q=80'),
            ('Nutella', 75.0, 'Latte', '', 'https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=600&q=80'),
            ('Moka Mexicano', 75.0, 'Latte', 'Chocolate Abuelita', 'https://cdn.phototourl.com/member/2026-10-19-bddc185b-cde3-424b-b1cd-3c476625a615.jpg'),
            ('Spanish', 75.0, 'Latte', 'Lechera', 'https://cdn.phototourl.com/member/2026-10-19-b5088241-0674-4852-9df3-3c4d2601e16e.jpg'),
            ('Canelita', 75.0, 'Latte', 'Miel, Canela', 'https://cdn.phototourl.com/member/2026-10-19-5ddf6133-7c16-4705-b55a-3de867062a14.jpg'),
            ('Dorado', 80.0, 'Latte', 'Miel, Canela, Vainilla', 'https://cdn.phototourl.com/member/2026-10-19-e82936a2-81f2-4f79-8509-c00030d7b261.jpg'),
            ('Tiramisú Latte', 75.0, 'Latte', 'Latte tradicional con Cold Foam de Tiramisú', 'https://cdn.phototourl.com/member/2026-10-19-954c38e7-3cd3-4f63-b23d-dbdee40ca71e.jpg'),
            ('Frutal', 80.0, 'Latte', 'Fresa / Mango / Arándano / Frutos rojos', 'https://cdn.phototourl.com/member/2026-10-19-e32054d0-3da8-48c8-a1bb-c95fcd7d34d7.jpg'),

            ('Tradicional', 70.0, 'Matcha', 'Con Cold Foam de Vainilla', 'https://cdn.phototourl.com/member/2026-10-19-9a1cea84-70aa-459d-a336-d0cb38bcd321.jpg'),  
            ('Tiramisú', 80.0, 'Matcha', 'Matcha tradicional con Cold Foam de Tiramisú', 'https://cdn.phototourl.com/member/2026-10-19-35930a22-3ac1-4f42-b139-1ed4e3fe1c5d.jpg'),
            ('Frutal (Fresita)', 85.0, 'Matcha', 'Fresa / Mango / Arándano / Frutos rojos', 'https://cdn.phototourl.com/member/2026-10-20-5b24f9fd-55b8-4c9c-95c7-05fd16e8ecd8.jpg'),
            ('Pink Tres Leches', 90.0, 'Matcha', 'Fresa, leche condensada y evaporada', 'https://cdn.phototourl.com/member/2026-10-20-8cabfc43-e7b1-4232-9443-b69d9a142155.jpg'),

            ('Ixli', 65.0, 'Tisana', 'Kiwi, Manzana, Fresa, Arándano', 'https://cdn.phototourl.com/member/2026-10-20-ac3b1966-dab7-4c1e-b886-ced7824f8a84.jpg'),
            ('Jacotepec', 65.0, 'Tisana', 'Mora Azul, Manzana, Fresa, Arándano', 'https://cdn.phototourl.com/member/2026-10-19-af2d4659-1bee-49db-883c-8ff94c128156.jpg'),

            ('Doppio', 40.0, 'Espresso', 'Espresso Doble', 'https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=600&q=80'),
            ('Americano', 50.0, 'Espresso', 'Espresso con agua', 'https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?w=600&q=80'),

            ('Golden Milk Latte', 65.0, 'Golden', 'Leche dorada (cúrcuma)', 'https://cdn.phototourl.com/member/2026-10-19-b5e6deb5-ff60-41f6-a71b-6c11ff9a0b32.jpg'),
            ('Golden Te', 55.0, 'Golden', 'Té dorado', 'https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=600&q=80'),
            ('Affogato Lotus', 85.0, 'Golden', 'Helado con espresso y Lotus', 'https://cdn.phototourl.com/member/2026-10-20-6b8a8297-35ec-4ea8-9144-db94c59e871d.jpg'),

            ('Croissant', 35.0, 'Desayunos', 'Sencillo / Cheesy', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80'),
            ('Bagel', 35.0, 'Desayunos', 'Sencillo / Cheesy', 'https://images.unsplash.com/photo-1555507036-ab1f4038808a?w=600&q=80'),
            ('Sandwich de Desayuno', 65.0, 'Desayunos', 'Croissant, Tocino, Huevo y Queso', 'https://cdn.phototourl.com/member/2026-10-19-097ae370-a35f-4bcd-a00f-249eb1d00cba.jpg'),
        ]
        
        c.executemany(
            'INSERT INTO productos (nombre, precio, categoria, descripcion, imagen) VALUES (?, ?, ?, ?, ?)',
            ejemplos
        )
    
    conn.commit()
    conn.close()


# ============================================================
# HELPERS
# ============================================================
def get_carrito():
    return session.get('carrito', {})

def guardar_carrito(c):
    session['carrito'] = c
    session.modified = True

def total_carrito(c):
    return sum(i['precio'] * i['cantidad'] for i in c.values())

def count_carrito(c):
    return sum(i['cantidad'] for i in c.values())


# ============================================================
# CSS
# ============================================================
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --crema: #FBF1DC;
    --crema-2: #F5E6C8;
    --beige: #EBD4A8;
    --dorado: #E5A93B;
    --dorado-suave: #F5C36A;
    --dorado-osc: #C98420;
    --cafe: #8B6F47;
    --cafe-oscuro: #5C4426;
    --marron: #3E2C1E;
    --texto: #3E2C1E;
    --texto-suave: #7A6548;
    --blanco: #FFFFFF;
    --sombra: 0 4px 20px rgba(92, 68, 38, 0.10);
    --sombra-hover: 0 12px 32px rgba(92, 68, 38, 0.18);
}

body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    background: var(--crema);
    color: var(--texto);
    line-height: 1.65;
    background-image:
        radial-gradient(circle at 12% 8%, rgba(235, 212, 168, 0.55) 0%, transparent 42%),
        radial-gradient(circle at 88% 92%, rgba(245, 195, 106, 0.25) 0%, transparent 45%);
    background-attachment: fixed;
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 1.5rem; }

h1, h2, h3 {
    font-family: Georgia, 'Times New Roman', serif;
    font-weight: 700;
    color: var(--cafe-oscuro);
    line-height: 1.25;
    letter-spacing: 0.01em;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
@keyframes revelarLento {
    0%   { opacity: 0; filter: brightness(0.2) blur(10px); transform: scale(1.06); }
    60%  { opacity: 0.85; filter: brightness(0.75) blur(3px); transform: scale(1.02); }
    100% { opacity: 1; filter: brightness(1) blur(0); transform: scale(1); }
}

/* ---------- HEADER ---------- */
header {
    background: var(--marron);
    padding: 0.75rem 0;
    position: sticky; top: 0; z-index: 100;
    box-shadow: 0 3px 14px rgba(62, 44, 30, 0.25);
    border-bottom: 3px solid var(--dorado);
}
.nav { display: flex; justify-content: space-between; align-items: center; gap: 1rem; flex-wrap: wrap; }
.logo { display: flex; align-items: center; gap: 0.8rem; text-decoration: none; color: var(--crema); }
.logo-img { width: 58px; height: 58px; border-radius: 50%; object-fit: cover; border: 2px solid var(--dorado); filter: drop-shadow(0 3px 8px rgba(0,0,0,0.3)); flex-shrink: 0; background: #fff; }
.logo-nombre { display: flex; flex-direction: column; line-height: 1.1; }
.logo-nombre span:first-child { font-family: Georgia, serif; font-size: 1.3rem; font-weight: 700; letter-spacing: 0.15em; color: var(--crema); }
.logo-nombre span:last-child { font-family: Georgia, serif; font-style: italic; font-size: 0.8rem; letter-spacing: 0.3em; color: var(--dorado-suave); margin-top: 3px; }

nav { display: flex; gap: 0.3rem; align-items: center; flex-wrap: wrap; }
nav a { color: var(--crema); text-decoration: none; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.95rem; font-weight: 500; transition: background 0.2s; }
nav a:hover { background: rgba(245, 195, 106, 0.15); color: var(--dorado-suave); }
nav a.cart-btn { background: var(--dorado); color: var(--marron); font-weight: 700; box-shadow: 0 3px 10px rgba(229, 169, 59, 0.4); }
nav a.cart-btn:hover { background: var(--dorado-suave); transform: translateY(-1px); color: var(--marron); }
.cart-count { background: var(--marron); color: var(--dorado-suave); border-radius: 10px; padding: 0.1rem 0.5rem; font-size: 0.8rem; margin-left: 0.3rem; font-weight: 700; }

/* ---------- MAIN ---------- */
main { min-height: 70vh; padding: 3rem 0; }

/* ---------- BOTÓN FLOTANTE INICIO ---------- */
.btn-inicio-flotante {
    position: fixed;
    bottom: 1.2rem;
    left: 1.2rem;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--marron);
    color: var(--crema);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    text-decoration: none;
    box-shadow: 0 4px 14px rgba(62, 44, 30, 0.35);
    border: 2px solid var(--dorado);
    z-index: 900;
    transition: all 0.25s;
}
.btn-inicio-flotante:hover {
    background: var(--dorado);
    color: var(--marron);
    transform: translateY(-3px) scale(1.08);
}

/* ---------- TARJETAS DE CATEGORÍA ---------- */
.categorias-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
}
.categoria-card {
    position: relative;
    border-radius: 20px;
    overflow: hidden;
    text-decoration: none;
    color: var(--crema);
    min-height: 220px;
    display: flex;
    align-items: flex-end;
    padding: 1.6rem;
    background-size: cover;
    background-position: center;
    box-shadow: var(--sombra);
    transition: transform 0.3s, box-shadow 0.3s;
    isolation: isolate;
}
.categoria-card::before {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(30,20,12,0.85), rgba(30,20,12,0.15));
    z-index: -1;
    transition: background 0.3s;
}
.categoria-card:hover { transform: translateY(-6px); box-shadow: var(--sombra-hover); }
.categoria-card:hover::before { background: linear-gradient(to top, rgba(30,20,12,0.9), rgba(92,68,38,0.45)); }
.categoria-card .cat-nombre {
    font-family: Georgia, serif;
    font-size: 1.7rem;
    font-weight: 700;
    text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    line-height: 1.1;
}
.categoria-card .cat-extra {
    display: block;
    font-family: Georgia, serif;
    font-style: italic;
    font-size: 0.85rem;
    color: var(--dorado-suave);
    margin-top: 0.3rem;
    text-shadow: 0 1px 6px rgba(0,0,0,0.7);
}
.categoria-card .cat-contador {
    position: absolute;
    top: 1rem; right: 1rem;
    background: rgba(251, 241, 220, 0.9);
    color: var(--marron);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
}

/* ---------- BOTÓN VOLVER ---------- */
.btn-volver-categorias {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--blanco);
    color: var(--cafe-oscuro);
    border: 2px solid var(--beige);
    padding: 0.55rem 1.2rem;
    border-radius: 22px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.9rem;
    transition: all 0.2s;
    margin-bottom: 1.5rem;
}
.btn-volver-categorias:hover { border-color: var(--dorado); background: var(--crema-2); transform: translateX(-2px); }

/* ---------- FILTROS ---------- */
.filtros { display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content: center; margin-bottom: 2rem; }
.chip { padding: 0.5rem 1.2rem; border-radius: 20px; background: var(--blanco); color: var(--texto); text-decoration: none; font-weight: 500; font-size: 0.9rem; border: 2px solid var(--beige); transition: all 0.2s; }
.chip:hover { border-color: var(--dorado); transform: translateY(-1px); }
.chip.activo { background: var(--dorado); color: var(--marron); border-color: var(--dorado); font-weight: 700; }

/* ---------- LISTA DE PRODUCTOS ---------- */
.producto-item { display: flex; align-items: center; gap: 1.5rem; padding: 1rem; background: var(--blanco); border-radius: 12px; margin-bottom: 1rem; box-shadow: var(--sombra); transition: transform 0.2s, box-shadow 0.2s; cursor: pointer; border: 2px solid transparent; }
.producto-item:hover { transform: translateY(-3px); box-shadow: var(--sombra-hover); border-color: var(--dorado-suave); }
.prod-img { width: 80px; height: 80px; object-fit: cover; border-radius: 8px; flex-shrink: 0; background: var(--crema-2); }
.prod-info { flex: 1; }
.prod-info h3 { font-size: 1.2rem; margin-bottom: 0.2rem; }
.prod-info p { font-size: 0.85rem; color: var(--texto-suave); font-style: italic; }
.prod-precio { font-size: 1.3rem; font-weight: 700; color: var(--marron); font-family: Georgia, serif; }
.prod-add { background: var(--dorado-suave); border: none; width: 40px; height: 40px; border-radius: 50%; font-size: 1.3rem; cursor: pointer; color: var(--marron); transition: all 0.25s; font-weight: 700; }
.prod-add:hover { background: var(--dorado); transform: rotate(90deg) scale(1.05); }

/* ---------- MODAL ---------- */
.modal-overlay { display: none; position: fixed; inset: 0; background: rgba(62, 44, 30, 0.55); backdrop-filter: blur(6px); z-index: 1000; justify-content: center; align-items: center; padding: 1rem; }
.modal-overlay.activo { display: flex; animation: fadeIn 0.25s; }
.modal { background: var(--blanco); border-radius: 22px; max-width: 500px; width: 100%; max-height: 90vh; overflow-y: auto; animation: scaleIn 0.3s; box-shadow: 0 20px 50px rgba(0,0,0,0.28); position: relative; }
.modal-img { width: 100%; height: 190px; object-fit: cover; display: block; background: var(--crema-2); }
.modal-close { position: absolute; top: 0.8rem; right: 0.8rem; background: rgba(251, 241, 220, 0.96); border: none; width: 34px; height: 34px; border-radius: 50%; cursor: pointer; font-size: 1rem; color: var(--marron); transition: all 0.2s; z-index: 2; }
.modal-close:hover { background: var(--marron); color: var(--crema); transform: rotate(90deg); }
.modal-body { padding: 1.5rem; }
.modal-body h2 { font-size: 1.6rem; margin-bottom: 0.2rem; }
.modal-cat { font-size: 0.75rem; text-transform: uppercase; color: var(--dorado-osc); margin-bottom: 0.5rem; font-weight: 700; letter-spacing: 0.08em; }
.modal-desc { color: var(--texto-suave); font-size: 0.9rem; margin-bottom: 1rem; font-style: italic; }

.form-grupo { margin-bottom: 1.2rem; }
.form-grupo label { display: block; font-weight: 600; font-size: 0.85rem; margin-bottom: 0.5rem; color: var(--marron); }
.opciones-tamano { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; }
.opcion-tamano { padding: 0.8rem 0.4rem; border: 2px solid var(--beige); background: var(--crema-2); border-radius: 12px; cursor: pointer; text-align: center; transition: all 0.2s; font-family: inherit; color: var(--texto); }
.opcion-tamano:hover { border-color: var(--dorado); }
.opcion-tamano.activo { background: var(--dorado); border-color: var(--dorado); color: var(--marron); }
.opcion-tamano .t-nombre { display: block; font-weight: 700; font-size: 0.9rem; }
.opcion-tamano .t-extra { display: block; font-size: 0.7rem; color: var(--texto-suave); margin-top: 0.1rem; }
.opcion-tamano.activo .t-extra { color: rgba(62, 44, 30, 0.75); }

.contador { display: inline-flex; align-items: center; background: var(--crema-2); border: 2px solid var(--beige); border-radius: 25px; overflow: hidden; }
.contador button { background: transparent; border: none; width: 42px; height: 42px; font-size: 1.2rem; cursor: pointer; color: var(--marron); transition: background 0.2s; }
.contador button:hover { background: var(--dorado-suave); }
.contador input { width: 55px; text-align: center; border: none; background: transparent; font-size: 1rem; font-weight: 700; color: var(--marron); outline: none; }

textarea, input[type=text], input[type=tel] { width: 100%; padding: 0.8rem 1rem; border: 2px solid var(--beige); border-radius: 12px; font-size: 0.9rem; font-family: inherit; background: var(--crema-2); color: var(--texto); outline: none; transition: border-color 0.2s; resize: vertical; }
textarea:focus, input:focus { border-color: var(--dorado); background: var(--blanco); }

.modal-total { background: var(--crema-2); border-radius: 12px; padding: 1rem 1.2rem; margin: 1.2rem 0; display: flex; justify-content: space-between; align-items: center; }
.modal-total span { font-size: 0.85rem; color: var(--texto-suave); }
.modal-total strong { font-size: 1.5rem; color: var(--marron); font-weight: 800; font-family: Georgia, serif; }

.btn { display: inline-flex; align-items: center; gap: 0.4rem; background: var(--marron); color: var(--crema); padding: 0.85rem 2rem; border: none; border-radius: 25px; text-decoration: none; cursor: pointer; font-size: 0.95rem; font-weight: 600; font-family: inherit; transition: all 0.2s; box-shadow: 0 4px 12px rgba(62, 44, 30, 0.2); }
.btn:hover { background: var(--cafe-oscuro); transform: translateY(-2px); box-shadow: 0 8px 20px rgba(62, 44, 30, 0.3); }
.btn-block { width: 100%; justify-content: center; }

/* ---------- CARRITO ---------- */
.carrito-layout { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
@media (min-width: 900px) { .carrito-layout { grid-template-columns: 1.6fr 1fr; } }
.carrito-card, .form-final { background: var(--blanco); border-radius: 18px; padding: 1.5rem; box-shadow: var(--sombra); border: 1px solid rgba(235, 212, 168, 0.6); }
.carrito-item { display: grid; grid-template-columns: 70px 1fr auto; gap: 1rem; align-items: center; padding: 1rem 0; border-bottom: 1px dashed var(--beige); }
.carrito-item:last-child { border-bottom: none; }
.carrito-item-img { width: 70px; height: 70px; object-fit: cover; border-radius: 12px; background: var(--crema-2); }
.carrito-item-info h4 { font-size: 1rem; margin-bottom: 0.2rem; color: var(--marron); }
.carrito-item-info small { color: var(--texto-suave); font-size: 0.8rem; display: block; font-style: italic; }
.carrito-item-precio { font-weight: 700; font-size: 1.15rem; color: var(--marron); text-align: right; font-family: Georgia, serif; }
.carrito-item-acciones { display: flex; gap: 0.5rem; align-items: center; margin-top: 0.4rem; }
.mini-contador { display: inline-flex; align-items: center; background: var(--crema-2); border-radius: 20px; border: 2px solid var(--beige); }
.mini-contador a { background: transparent; border: none; width: 28px; height: 28px; cursor: pointer; color: var(--marron); text-decoration: none; display: flex; align-items: center; justify-content: center; border-radius: 50%; transition: background 0.2s; }
.mini-contador a:hover { background: var(--dorado-suave); }
.mini-contador span { padding: 0 0.5rem; font-weight: 700; font-size: 0.9rem; }
.btn-eliminar { background: transparent; border: none; color: var(--beige); cursor: pointer; font-size: 1rem; padding: 0.3rem; border-radius: 50%; transition: color 0.2s; text-decoration: none; }
.btn-eliminar:hover { color: #A54B3D; }

.total-box { background: linear-gradient(135deg, var(--crema-2), var(--beige)); border-radius: 12px; padding: 1.2rem 1.4rem; margin-top: 1.5rem; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(229, 169, 59, 0.3); }
.total-box span { font-size: 0.9rem; color: var(--texto-suave); font-weight: 600; }
.total-box strong { font-size: 1.7rem; color: var(--marron); font-weight: 800; font-family: Georgia, serif; }

/* ---------- ÉXITO ---------- */
.exito { max-width: 550px; margin: 3rem auto; text-align: center; background: var(--blanco); padding: 3rem 2rem; border-radius: 22px; box-shadow: var(--sombra); animation: scaleIn 0.5s; border: 1px solid rgba(235, 212, 168, 0.6); }
.exito .emoji-grande { font-size: 4rem; display: block; margin-bottom: 1rem; }
.exito h1 { font-size: 1.9rem; margin-bottom: 0.8rem; }
.exito p { color: var(--texto-suave); margin-bottom: 1.5rem; }
.exito .num-pedido { display: inline-block; background: var(--dorado-suave); color: var(--marron); padding: 0.4rem 1rem; border-radius: 12px; font-weight: 700; font-size: 0.85rem; margin-bottom: 1.2rem; }
.exito-acciones { display: flex; gap: 0.8rem; justify-content: center; flex-wrap: wrap; margin-top: 1.5rem; }

/* ---------- FOOTER ---------- */
footer { background: linear-gradient(180deg, var(--marron), #2A1E14); color: var(--crema); padding: 3rem 0 1.8rem; text-align: center; border-top: 3px solid var(--dorado); }
.footer-logo-wrap { display: inline-flex; flex-direction: column; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem; }
.footer-logo-img { width: 80px; height: 80px; border-radius: 50%; object-fit: cover; border: 2px solid var(--dorado); filter: drop-shadow(0 4px 10px rgba(229, 169, 59, 0.4)); background: #fff; }
footer .footer-logo-texto { font-family: Georgia, serif; font-size: 1.2rem; font-weight: 700; letter-spacing: 0.2em; color: var(--crema); }
footer p { opacity: 0.85; font-size: 0.9rem; margin-top: 0.3rem; color: var(--crema); font-style: italic; font-family: Georgia, serif; }

.footer-redes { display: flex; gap: 0.8rem; justify-content: center; margin: 1.2rem 0 0.5rem; flex-wrap: wrap; }
.footer-redes a {
    display: inline-flex; align-items: center; justify-content: center;
    width: 42px; height: 42px; border-radius: 50%;
    background: rgba(245, 195, 106, 0.12);
    border: 1.5px solid rgba(229, 169, 59, 0.5);
    color: var(--dorado-suave); text-decoration: none; font-size: 1.1rem;
    transition: all 0.25s;
}
.footer-redes a:hover {
    background: var(--dorado); color: var(--marron);
    transform: translateY(-3px) scale(1.08);
    box-shadow: 0 6px 16px rgba(229, 169, 59, 0.35);
}

.footer-agradecimientos { margin-top: 1.6rem; }
.btn-agradecimientos {
    display: inline-block;
    padding: 0.4rem 0.95rem;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(251, 241, 220, 0.55);
    background: transparent;
    border: 1px solid rgba(235, 212, 168, 0.25);
    border-radius: 20px;
    text-decoration: none;
    font-family: inherit;
    transition: all 0.25s;
}
.btn-agradecimientos:hover {
    color: var(--dorado-suave);
    border-color: var(--dorado);
    background: rgba(245, 195, 106, 0.08);
}

footer .copy { opacity: 0.5; font-size: 0.78rem; margin-top: 1rem; padding-top: 1.5rem; border-top: 1px solid rgba(235, 212, 168, 0.15); }

/* ---------- FLASH ---------- */
.flash { padding: 0.9rem 1.2rem; border-radius: 12px; margin-bottom: 1rem; font-size: 0.9rem; animation: fadeIn 0.3s; }
.flash.success { background: #E5F5E9; color: #2A6B44; }
.flash.warning { background: #FFF3CD; color: #8B6914; }

/* ---------- PANTALLA AGRADECIMIENTOS ---------- */
.fullscreen-gracias { position: fixed; inset: 0; overflow: hidden; z-index: 500; background: #0A0805; }
.fullscreen-gracias .imagen-fondo {
    position: absolute; inset: 0;
    background-size: contain; /* Imagen completa */
    background-position: center;
    background-repeat: no-repeat;
    background-color: #0A0805;
    opacity: 0;
    filter: brightness(1) blur(0);
    transform: scale(1);
    animation: revelarLento 3.5s ease-out 0.3s forwards;
}

/* Botón de música personalizado */
.btn-musica {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    background: rgba(251, 241, 220, 0.95);
    border: 2px solid var(--dorado);
    border-radius: 30px;
    padding: 0.8rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    cursor: pointer;
    z-index: 1000;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: all 0.3s;
    font-family: 'Segoe UI', sans-serif;
    color: var(--marron);
    font-weight: 600;
    font-size: 0.95rem;
}
.btn-musica:hover {
    background: #FFFFFF;
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(229, 169, 59, 0.5);
}
.btn-musica .icono {
    font-size: 1.3rem;
    animation: pulso 1.5s infinite ease-in-out;
}
@keyframes pulso {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

/* ---------- PORTADA ---------- */
.portada-hero {
    position: relative;
    text-align: center;
    padding: 5rem 1.5rem 4rem;
    border-radius: 26px;
    background:
        linear-gradient(135deg, rgba(62,44,30,0.72), rgba(92,68,38,0.55)),
        url('https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1600&q=80') center/cover;
    color: var(--crema);
    box-shadow: var(--sombra-hover);
    overflow: hidden;
    animation: fadeIn 0.9s ease;
}
.portada-hero h1 {
    color: var(--crema);
    font-size: 3.2rem;
    margin-bottom: 0.8rem;
    text-shadow: 0 3px 14px rgba(0,0,0,0.45);
}
.portada-hero .lema {
    font-family: Georgia, serif;
    font-style: italic;
    font-size: 1.2rem;
    color: var(--dorado-suave);
    margin-bottom: 2.2rem;
    text-shadow: 0 2px 8px rgba(0,0,0,0.5);
}
.portada-hero .btn { font-size: 1.05rem; padding: 1rem 2.6rem; }
.portada-hero .btn:hover { background: var(--dorado); color: var(--marron); }

.portada-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-top: 3rem;
}
.portada-card {
    background: var(--blanco);
    border-radius: 18px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: var(--sombra);
    border: 1px solid rgba(235, 212, 168, 0.6);
    transition: transform 0.25s, box-shadow 0.25s;
}
.portada-card:hover { transform: translateY(-6px); box-shadow: var(--sombra-hover); }
.portada-card .icono { font-size: 2.4rem; display: block; margin-bottom: 0.8rem; }
.portada-card h3 { font-size: 1.15rem; margin-bottom: 0.4rem; }
.portada-card p { color: var(--texto-suave); font-size: 0.9rem; }

.portada-info {
    margin-top: 3rem;
    text-align: center;
    background: var(--blanco);
    border-radius: 18px;
    padding: 2rem 1.5rem;
    box-shadow: var(--sombra);
    border: 1px solid rgba(235, 212, 168, 0.6);
}
.portada-info h2 { font-size: 1.6rem; margin-bottom: 0.6rem; }
.portada-info p { color: var(--texto-suave); font-size: 0.95rem; }
.portada-info .horario { font-family: Georgia, serif; font-style: italic; color: var(--cafe); margin-top: 0.6rem; }
"""


# ============================================================
# LAYOUT BASE
# ============================================================
def base(contenido):
    redes_html = "".join(
        f'<a href="{r["url"]}" target="_blank" rel="noopener" title="{r["nombre"]}">{r["icono"]}</a>'
        for r in REDES
    )

    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Solecito Café </title>
<link rel="icon" type="image/jpeg" href=\"""" + LOGO_URL + """\">
<style>{{ css|safe }}</style>
</head>
<body>

<header>
    <div class="container nav">
        <a href="{{ url_for('portada') }}" class="logo">
            <img src=\"""" + LOGO_URL + """\" alt="Logo" class="logo-img">
            <div class="logo-nombre">
                <span>SOLECITO</span>
                <span>café</span>
            </div>
        </a>
        <nav>
            <a href="{{ url_for('portada') }}">Inicio</a>
            <a href="{{ url_for('index') }}">Menú</a>
            <a href="{{ url_for('ver_carrito') }}" class="cart-btn">
                🛒 Carrito {% if carrito_count > 0 %}<span class="cart-count">{{ carrito_count }}</span>{% endif %}
            </a>
        </nav>
    </div>
</header>

{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="container" style="padding-top: 1rem;">
        {% for categoria, msg in messages %}
            <div class="flash {{ categoria }}">{{ msg }}</div>
        {% endfor %}
        </div>
    {% endif %}
{% endwith %}

<main class="container">
    """ + contenido + """
</main>

<footer>
    <div class="container">
        <div class="footer-logo-wrap">
            <img src=\"""" + LOGO_URL + """\" alt="Logo" class="footer-logo-img">
            <span class="footer-logo-texto">SOLECITO café</span>
        </div>
        <p>Café que cura el corazón ♥</p>

        <div class="footer-redes">
            """ + redes_html + """
        </div>

        <div class="footer-agradecimientos">
            <a href="{{ url_for('agradecimientos') }}" class="btn-agradecimientos">Agradecimientos</a>
        </div>

        <div class="copy">© 2025 Solecito Café · Independencia No. 44B, Ixtlahuacán del Río, 45260</div>
    </div>
</footer>

<a href="{{ url_for('portada') }}" class="btn-inicio-flotante" title="Inicio">🏠</a>

<script>
let productoActual = null;

function abrirModal(id, nombre, precio, descripcion, imagen, categoria) {
    productoActual = { id, nombre, precio, descripcion, imagen, categoria };
    document.getElementById('modal-img').src = imagen;
    document.getElementById('modal-cat').textContent = categoria;
    document.getElementById('modal-nombre').textContent = nombre;
    document.getElementById('modal-desc').textContent = descripcion || 'Preparado con los mejores ingredientes';
    document.getElementById('modal-cantidad').value = 1;
    document.getElementById('modal-notas').value = '';
    document.getElementById('modal-prod-id').value = id;

    document.querySelectorAll('.opcion-tamano').forEach((b, i) => {
        b.classList.toggle('activo', i === 0);
    });
    document.getElementById('modal-tamano').value = 'Chico';
    document.getElementById('modal-mult').value = '1.00';
    actualizarTotalModal();
    document.getElementById('modal-overlay').classList.add('activo');
    document.body.style.overflow = 'hidden';
}

function cerrarModal() {
    document.getElementById('modal-overlay').classList.remove('activo');
    document.body.style.overflow = '';
}

function seleccionarTamano(btn, nombre, multiplicador) {
    document.querySelectorAll('.opcion-tamano').forEach(b => b.classList.remove('activo'));
    btn.classList.add('activo');
    document.getElementById('modal-tamano').value = nombre;
    document.getElementById('modal-mult').value = multiplicador;
    actualizarTotalModal();
}

function cambiarCantidad(delta) {
    const input = document.getElementById('modal-cantidad');
    let v = parseInt(input.value) + delta;
    if (v < 1) v = 1;
    if (v > 20) v = 20;
    input.value = v;
    actualizarTotalModal();
}

function actualizarTotalModal() {
    if (!productoActual) return;
    const cant = parseInt(document.getElementById('modal-cantidad').value) || 1;
    const mult = parseFloat(document.getElementById('modal-mult').value) || 1;
    const total = productoActual.precio * mult * cant;
    document.getElementById('modal-total').textContent = '$' + total.toFixed(2);
}

document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.getElementById('modal-overlay');
    if (overlay) {
        overlay.addEventListener('click', e => {
            if (e.target === overlay) cerrarModal();
        });
    }
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') cerrarModal();
    });
});
</script>
</body>
</html>
"""


# ============================================================
# PORTADA (primera página)
# ============================================================
PORTADA_HTML = base("""
<div class="portada-hero">
    <h1>Solecito Café </h1>
    <p class="lema">Café que cura el corazón ♥</p>
    <a href="{{ url_for('index') }}" class="btn">☕ Ver el menú</a>
</div>

<div class="portada-cards">
    <div class="portada-card">
        <span class="icono">☕</span>
        <h3>Café de especialidad</h3>
        <p>Lattes, matchas y espressos preparados con cariño.</p>
    </div>
    <div class="portada-card">
        <span class="icono">🍵</span>
        <h3>Tisanas artesanales</h3>
        <p>Mezclas frutales y especiadas de la casa.</p>
    </div>
    <div class="portada-card">
        <span class="icono">🥐</span>
        <h3>Desayunos frescos</h3>
        <p>Croissants, bagels y sandwiches recién hechos.</p>
    </div>
</div>

<div class="portada-info">
    <h2>Visítanos</h2>
    <p>Independencia No. 44B, Ixtlahuacán del Río, 45260</p>
    <p class="horario">Lunes a domingo · 8:00 am – 9:00 pm</p>
</div>
""")


# ============================================================
# MENÚ (por categorías)
# ============================================================
INDEX_HTML = base("""
{% if categoria_actual %}
    <a href="{{ url_for('index') }}" class="btn-volver-categorias">← Todas las categorías</a>
{% endif %}

<div style="text-align: center; margin-bottom: 2rem;">
    {% if categoria_actual %}
        <h1 style="font-size: 2.8rem; margin-bottom: 0.5rem;">{{ categoria_actual }}</h1>
        {% if categoria_actual == 'Latte' %}<p style="color: var(--texto-suave); font-style: italic; font-family: Georgia, serif;">Frío / Caliente / Frappé</p>{% endif %}
        {% if categoria_actual == 'Matcha' %}<p style="color: var(--texto-suave); font-style: italic; font-family: Georgia, serif;">Frío / Caliente</p>{% endif %}
    {% else %}
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">Nuestro Menú</h1>
        <p style="color: var(--texto-suave); font-style: italic; font-family: Georgia, serif;">— Elige una categoría —</p>
    {% endif %}
</div>

{% if not categoria_actual %}
    <div class="categorias-grid">
        {% for cat, prods in categorias_dict.items() %}
            <a href="{{ url_for('index', categoria=cat) }}" class="categoria-card" style="background-image: url('{{ prods[0].imagen }}');">
                <span class="cat-contador">{{ prods|length }} opciones</span>
                <div>
                    <span class="cat-nombre">{{ cat }}</span>
                    {% if cat == 'Latte' %}<span class="cat-extra">Frío / Caliente / Frappé</span>{% endif %}
                    {% if cat == 'Matcha' %}<span class="cat-extra">Frío / Caliente</span>{% endif %}
                </div>
            </a>
        {% endfor %}
    </div>
{% else %}
    {% for cat, prods in categorias_dict.items() %}
        {% if cat == categoria_actual %}
            {% for p in prods %}
                <div class="producto-item" onclick="abrirModal({{ p.id }}, '{{ p.nombre|e }}', {{ p.precio }}, '{{ p.descripcion|e }}', '{{ p.imagen }}', '{{ p.categoria }}')">
                    <img class="prod-img" src="{{ p.imagen }}" alt="{{ p.nombre }}">
                    <div class="prod-info">
                        <h3>{{ p.nombre }}</h3>
                        {% if p.descripcion %}<p>{{ p.descripcion }}</p>{% endif %}
                    </div>
                    <div class="prod-precio">${{ "%.2f"|format(p.precio) }}</div>
                    <button class="prod-add">+</button>
                </div>
            {% endfor %}
        {% endif %}
    {% endfor %}
{% endif %}

<div class="modal-overlay" id="modal-overlay">
    <div class="modal" onclick="event.stopPropagation()">
        <form method="POST" action="{{ url_for('agregar_al_carrito') }}">
            <input type="hidden" name="producto_id" id="modal-prod-id">
            <input type="hidden" name="tamano" id="modal-tamano" value="Chico">
            <input type="hidden" name="multiplicador" id="modal-mult" value="1.00">

            <button type="button" class="modal-close" onclick="cerrarModal()">✕</button>
            <img class="modal-img" id="modal-img" src="" alt="Producto">

            <div class="modal-body">
                <div class="modal-cat" id="modal-cat">Categoría</div>
                <h2 id="modal-nombre">Producto</h2>
                <p class="modal-desc" id="modal-desc">Descripción</p>

                <div class="form-grupo">
                    <label>Tamaño</label>
                    <div class="opciones-tamano">
                        <button type="button" class="opcion-tamano activo" onclick="seleccionarTamano(this, 'Chico', 1.00)">
                            <span class="t-nombre">Chico</span>
                            <span class="t-extra">Base</span>
                        </button>
                        <button type="button" class="opcion-tamano" onclick="seleccionarTamano(this, 'Mediano', 1.25)">
                            <span class="t-nombre">Mediano</span>
                            <span class="t-extra">+25%</span>
                        </button>
                        <button type="button" class="opcion-tamano" onclick="seleccionarTamano(this, 'Grande', 1.50)">
                            <span class="t-nombre">Grande</span>
                            <span class="t-extra">+50%</span>
                        </button>
                    </div>
                </div>

                <div class="form-grupo">
                    <label>Cantidad</label>
                    <div class="contador">
                        <button type="button" onclick="cambiarCantidad(-1)">−</button>
                        <input type="number" name="cantidad" id="modal-cantidad" value="1" min="1" max="20" readonly>
                        <button type="button" onclick="cambiarCantidad(1)">+</button>
                    </div>
                </div>

                <div class="form-grupo">
                    <label>Notas especiales</label>
                    <textarea name="notas" id="modal-notas" rows="2" placeholder="Sin azúcar, leche deslactosada…"></textarea>
                </div>

                <div class="modal-total">
                    <span>Total</span>
                    <strong id="modal-total">$0.00</strong>
                </div>

                <button type="submit" class="btn btn-block"> Agregar al pedido</button>
            </div>
        </form>
    </div>
</div>
""")


CARRITO_HTML = base("""
<div style="margin-bottom: 1.5rem;">
    <a href="{{ url_for('index') }}" style="color: var(--cafe); text-decoration: none; font-weight: 600;">← Volver al menú</a>
</div>

<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem;">Tu Pedido</h1>
</div>

{% if carrito %}
<div class="carrito-layout">
    <div class="carrito-card">
        <h3 style="margin-bottom: 1rem; color: var(--marron);">Productos ({{ carrito_count }})</h3>
        {% for pid, item in carrito.items() %}
            <div class="carrito-item">
                <img class="carrito-item-img" src="{{ item.imagen }}" alt="{{ item.nombre }}">
                <div class="carrito-item-info">
                    <h4>{{ item.nombre }}</h4>
                    <small>
                        {{ item.tamano }}{% if item.notas %} · {{ item.notas }}{% endif %}
                    </small>
                    <div class="carrito-item-acciones">
                        <div class="mini-contador">
                            <a href="{{ url_for('disminuir', pid=pid) }}">−</a>
                            <span>{{ item.cantidad }}</span>
                            <a href="{{ url_for('aumentar', pid=pid) }}">+</a>
                        </div>
                        <a href="{{ url_for('eliminar_del_carrito', pid=pid) }}" class="btn-eliminar" title="Eliminar">✕</a>
                    </div>
                </div>
                <div class="carrito-item-precio">${{ "%.2f"|format(item.precio * item.cantidad) }}</div>
            </div>
        {% endfor %}

        <div class="total-box">
            <span>Total del pedido</span>
            <strong>${{ "%.2f"|format(total) }}</strong>
        </div>
    </div>

    <div class="form-final">
        <h2 style="margin-bottom: 0.5rem;">Datos del pedido</h2>
        <p style="color: var(--texto-suave); margin-bottom: 1.2rem; font-size: 0.9rem; font-style: italic;">Completa tu información</p>

        <form method="POST" action="{{ url_for('checkout') }}">
            <div class="form-grupo">
                <label>Nombre *</label>
                <input type="text" name="cliente" placeholder="María González" required>
            </div>
            <div class="form-grupo">
                <label>Teléfono</label>
                <input type="tel" name="telefono" placeholder="55 1234 5678">
            </div>
            <div class="form-grupo">
                <label>Dirección o Mesa</label>
                <input type="text" name="direccion" placeholder="Calle... o Mesa #4">
            </div>
            <div class="form-grupo">
                <label>Notas del pedido</label>
                <textarea name="notas" rows="2" placeholder="Entregar antes de las 5pm…"></textarea>
            </div>

            <button type="submit" class="btn btn-block">Confirmar pedido</button>
            <a href="{{ url_for('vaciar_carrito') }}" style="display: block; text-align: center; margin-top: 1rem; color: #A54B3D; text-decoration: none; font-size: 0.9rem;">🗑️ Vaciar carrito</a>
        </form>
    </div>
</div>

{% else %}
<div style="text-align: center; padding: 4rem 2rem; background: white; border-radius: 22px; max-width: 500px; margin: 0 auto;">
    <span style="font-size: 4rem; display: block; margin-bottom: 1rem;">☕</span>
    <h3 style="margin-bottom: 0.5rem;">Tu carrito está vacío</h3>
    <p style="color: var(--texto-suave); margin-bottom: 1.5rem; font-style: italic;">Agrega productos del menú para comenzar</p>
    <a href="{{ url_for('index') }}" class="btn">Ir al menú</a>
</div>
{% endif %}
""")


EXITO_HTML = base("""
<div class="exito">
    <span class="emoji-grande">🎉</span>
    <div class="num-pedido">Pedido #{{ pedido_id }}</div>
    <h1>¡Gracias, {{ cliente }}!</h1>
    <p>Tu pedido ha sido registrado con éxito.<br>En breve comenzaremos a prepararlo.</p>

    <div style="background: var(--crema-2); border-radius: 12px; padding: 1.2rem; margin: 1.2rem 0; text-align: left;">
        <p style="margin: 0; font-size: 0.8rem; color: var(--texto-suave);">Total</p>
        <p style="font-size: 1.6rem; font-weight: 700; color: var(--marron); margin: 0.2rem 0 0; font-family: Georgia, serif;">${{ "%.2f"|format(total) }}</p>
        {% if telefono %}<p style="margin-top: 0.8rem; font-size: 0.85rem;"><strong>Teléfono:</strong> {{ telefono }}</p>{% endif %}
        {% if direccion %}<p style="font-size: 0.85rem;"><strong>Dirección/Mesa:</strong> {{ direccion }}</p>{% endif %}
        {% if notas %}<p style="font-size: 0.85rem;"><strong>Notas:</strong> {{ notas }}</p>{% endif %}
    </div>

    <div class="exito-acciones">
        <a href="{{ url_for('index') }}" class="btn">Seguir pidiendo</a>
    </div>
</div>
""")


# ============================================================
# PÁGINA AGRADECIMIENTOS (sin texto, solo imagen + música)
# ============================================================
def agradecimientos_html(imagen_url, musica_url):
    import urllib.parse
    audio_src = url_for('static', filename=urllib.parse.quote(musica_url))
    
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>♥</title>
<style>{{ css|safe }}</style>
</head>
<body>

<audio id="audio-fondo" loop preload="auto" autoplay>
    <source src=\"""" + audio_src + """\" type="audio/mpeg">
</audio>

<div class="btn-musica" id="btn-musica" onclick="toggleMusica()">
    <span class="icono" id="icono">🎵</span>
    <span id="texto-btn">Reproducir música</span>
</div>

<a href="{{ url_for('portada') }}" class="btn-inicio-flotante" title="Inicio">🏠</a>

<div class="fullscreen-gracias">
    <div class="imagen-fondo" style="background-image: url('""" + imagen_url + """');"></div>
</div>

<script>
function toggleMusica() {
    const audio = document.getElementById('audio-fondo');
    const icono = document.getElementById('icono');
    const texto = document.getElementById('texto-btn');
    const btn = document.getElementById('btn-musica');
    
    if (!audio) return;

    if (audio.paused) {
        if (audio.currentTime === 0) {
            audio.currentTime = 54;
        }
        audio.play().then(() => {
            icono.textContent = '🔊';
            texto.textContent = 'Pausar música';
            btn.style.background = 'rgba(245, 195, 106, 0.95)';
        }).catch(err => {
            console.error("Error al reproducir:", err);
        });
    } else {
        audio.pause();
        icono.textContent = '🎵';
        texto.textContent = 'Reproducir música';
        btn.style.background = 'rgba(251, 241, 220, 0.95)';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const audio = document.getElementById('audio-fondo');
    const icono = document.getElementById('icono');
    const texto = document.getElementById('texto-btn');
    const btn = document.getElementById('btn-musica');
    
    if (audio) {
        audio.volume = 0.35;
        audio.currentTime = 54; // Preparado en el segundo 54
        
        const playPromise = audio.play();
        
        if (playPromise !== undefined) {
            playPromise.then(() => {
                icono.textContent = '🔊';
                texto.textContent = 'Pausar música';
                btn.style.background = 'rgba(245, 195, 106, 0.95)';
            }).catch(() => {
                console.log("Autoplay bloqueado por el navegador. Se requiere clic del usuario.");
                icono.textContent = '🎵';
                texto.textContent = 'Reproducir música';
                btn.style.background = 'rgba(251, 241, 220, 0.95)';
            });
        }
    }
});
</script>
</body>
</html>
"""


# ============================================================
# HELPER DE RENDER
# ============================================================
def render(page_html, **ctx):
    carrito = get_carrito()
    ctx['css'] = CSS
    ctx['carrito_count'] = count_carrito(carrito)
    return render_template_string(page_html, **ctx)


# ============================================================
# RUTAS
# ============================================================
@app.route('/')
def portada():
    return render(PORTADA_HTML)


@app.route('/menu')
def index():
    db = get_db()
    categoria = request.args.get('categoria')
    
    if categoria:
        productos = db.execute('SELECT * FROM productos WHERE categoria = ?', (categoria,)).fetchall()
    else:
        productos = db.execute('SELECT * FROM productos').fetchall()
        
    categorias = [r['categoria'] for r in db.execute('SELECT DISTINCT categoria FROM productos').fetchall()]
    
    categorias_dict = {}
    for cat in categorias:
        categorias_dict[cat] = [p for p in productos if p['categoria'] == cat]

    return render(INDEX_HTML, productos=productos, categorias=categorias, categoria_actual=categoria, categorias_dict=categorias_dict)


@app.route('/agregar', methods=['POST'])
def agregar_al_carrito():
    db = get_db()
    pid = request.form.get('producto_id')
    tamano = request.form.get('tamano', 'Chico')
    multiplicador = float(request.form.get('multiplicador', 1.0))
    cantidad = int(request.form.get('cantidad', 1))
    notas = request.form.get('notas', '').strip()

    prod = db.execute('SELECT * FROM productos WHERE id = ?', (pid,)).fetchone()
    if not prod:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('index'))

    precio_final = round(prod['precio'] * multiplicador, 2)
    key = f"{pid}-{tamano}-{notas}"

    carrito = get_carrito()
    if key in carrito:
        carrito[key]['cantidad'] += cantidad
    else:
        carrito[key] = {
            'id': prod['id'],
            'nombre': prod['nombre'],
            'precio': precio_final,
            'cantidad': cantidad,
            'tamano': tamano,
            'notas': notas,
            'imagen': prod['imagen'],
        }
    guardar_carrito(carrito)
    flash(f'"{prod["nombre"]}" agregado al pedido', 'success')
    return redirect(request.referrer or url_for('index'))


@app.route('/carrito')
def ver_carrito():
    carrito = get_carrito()
    return render(CARRITO_HTML, carrito=carrito, total=total_carrito(carrito))


@app.route('/carrito/aumentar/<pid>')
def aumentar(pid):
    carrito = get_carrito()
    if pid in carrito:
        carrito[pid]['cantidad'] += 1
        guardar_carrito(carrito)
    return redirect(url_for('ver_carrito'))


@app.route('/carrito/disminuir/<pid>')
def disminuir(pid):
    carrito = get_carrito()
    if pid in carrito:
        carrito[pid]['cantidad'] -= 1
        if carrito[pid]['cantidad'] <= 0:
            del carrito[pid]
        guardar_carrito(carrito)
    return redirect(url_for('ver_carrito'))


@app.route('/carrito/eliminar/<pid>')
def eliminar_del_carrito(pid):
    carrito = get_carrito()
    carrito.pop(pid, None)
    guardar_carrito(carrito)
    return redirect(url_for('ver_carrito'))


@app.route('/carrito/vaciar')
def vaciar_carrito():
    session.pop('carrito', None)
    flash('Carrito vaciado', 'warning')
    return redirect(url_for('ver_carrito'))


@app.route('/checkout', methods=['POST'])
def checkout():
    carrito = get_carrito()
    if not carrito:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('index'))

    cliente = request.form.get('cliente', '').strip() or 'Anónimo'
    telefono = request.form.get('telefono', '').strip()
    direccion = request.form.get('direccion', '').strip()
    notas = request.form.get('notas', '').strip()
    total = total_carrito(carrito)

    detalle = " | ".join(
        f"{i['cantidad']}x {i['nombre']} ({i['tamano']})"
        for i in carrito.values()
    )

    db = get_db()
    cur = db.execute(
        '''INSERT INTO pedidos (cliente, telefono, direccion, notas, total, detalle, fecha)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (cliente, telefono, direccion, notas, total, detalle,
         datetime.now().strftime('%Y-%m-%d %H:%M'))
    )
    db.commit()
    pedido_id = cur.lastrowid

    session.pop('carrito', None)
    return render(EXITO_HTML, pedido_id=pedido_id, cliente=cliente,
                  telefono=telefono, direccion=direccion,
                  notas=notas, total=total)


@app.route('/agradecimientos')
def agradecimientos():
    return render_template_string(
        agradecimientos_html(IMAGEN_SORPRESA, MUSICA_SORPRESA),
        css=CSS
    )


# ============================================================
# MAIN
# ============================================================
init_db()

if __name__ == '__main__':
    print('=' * 55)
    print('    SOLECITO CAFÉ — Servidor Flask')
    print('  🌐  http://127.0.0.1:5000')
    print('=' * 55)
    app.run(debug=True)
