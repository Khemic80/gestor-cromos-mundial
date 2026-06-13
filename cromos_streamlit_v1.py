import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Gestor de Cromos - Mundial 2026",
    page_icon="🏆",
    layout="wide"
)

# ============================================================
# INICIALIZACIÓN DE ESTADO - SIN RERUN AUTOMÁTICO
# ============================================================
if 'datos' not in st.session_state:
    st.session_state.datos = {}
if 'cromos_por_equipo' not in st.session_state:
    st.session_state.cromos_por_equipo = {}
if 'lista_equipos' not in st.session_state:
    st.session_state.lista_equipos = []
if 'equipo_actual' not in st.session_state:
    st.session_state.equipo_actual = None
if 'excel_cargado' not in st.session_state:
    st.session_state.excel_cargado = False
if 'excel_nombre' not in st.session_state:
    st.session_state.excel_nombre = None
if 'json_nombre' not in st.session_state:
    st.session_state.json_nombre = None

# ============================================================
# ICONOS
# ============================================================
ICONOS = {
    "FIFA World Cup History": "🏆",
    "Extra Sticker": "⭐",
    "Coca Cola - Edición España": "🥤",
    "default": "⚽"
}

PAISES_ICONOS = {
    "Corea del Sur": "🇰🇷", "Korea Republic": "🇰🇷", "Algeria": "🇩🇿",
    "Bosnia": "🇧🇦", "España": "🇪🇸", "Paraguay": "🇵🇾", "Qatar": "🇶🇦",
    "Argentina": "🇦🇷", "New Zealand": "🇳🇿", "Uzbekistan": "🇺🇿",
    "Australia": "🇦🇺", "Morocco": "🇲🇦", "Croatia": "🇭🇷", "México": "🇲🇽",
    "South Africa": "🇿🇦", "Jordan": "🇯🇴", "Czechia": "🇨🇿", "Canadá": "🇨🇦",
    "Switzerland": "🇨🇭", "Brazil": "🇧🇷", "Japan": "🇯🇵", "Haiti": "🇭🇹",
    "Scotland": "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "USA": "🇺🇸", "Austria": "🇦🇹", "Türkiye": "🇹🇷",
    "Germany": "🇩🇪", "Curaçao": "🇨🇼", "Côte d'Ivoire": "🇨🇮", "Ecuador": "🇪🇨",
    "Netherlands": "🇳🇱", "Sweden": "🇸🇪", "Tunisia": "🇹🇳", "Belgium": "🇧🇪",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Egypt": "🇪🇬", "Portugal": "🇵🇹", "IR Iran": "🇮🇷",
    "Cabo Verde": "🇨🇻", "Saudi Arabia": "🇸🇦", "Uruguay": "🇺🇾", "France": "🇫🇷",
    "Senegal": "🇸🇳", "Iraq": "🇮🇶", "Norway": "🇳🇴", "Congo DR": "🇨🇩",
    "Colombia": "🇨🇴", "Ghana": "🇬🇭", "Panamá": "🇵🇦"
}

def obtener_icono(nombre):
    if nombre in ICONOS:
        return ICONOS[nombre]
    if nombre in PAISES_ICONOS:
        return PAISES_ICONOS[nombre]
    for key, icono in PAISES_ICONOS.items():
        if key.lower() in nombre.lower() or nombre.lower() in key.lower():
            return icono
    return "⚽"

# ============================================================
# FUNCIONES
# ============================================================

def cargar_excel(file):
    """Carga el Excel y crea la estructura de cromos"""
    try:
        df = pd.read_excel(file)
        
        if len(df.columns) < 3:
            st.error("❌ El Excel debe tener 3 columnas")
            return False
        
        col_equipo = df.columns[0]
        col_codigo = df.columns[1]
        col_nombre = df.columns[2]
        
        cromos_por_equipo = {}
        
        for _, row in df.iterrows():
            equipo = str(row[col_equipo]).strip() if pd.notna(row[col_equipo]) else ""
            codigo = str(row[col_codigo]).strip() if pd.notna(row[col_codigo]) else ""
            nombre = str(row[col_nombre]).strip() if pd.notna(row[col_nombre]) else ""
            
            if not equipo or equipo == 'nan' or len(equipo) < 2:
                continue
            if not codigo or codigo == 'nan':
                continue
            if not nombre or nombre == 'nan':
                continue
            
            cromo = f"{codigo} - {nombre}"
            
            if equipo not in cromos_por_equipo:
                cromos_por_equipo[equipo] = []
            if cromo not in cromos_por_equipo[equipo]:
                cromos_por_equipo[equipo].append(cromo)
        
        for equipo in cromos_por_equipo:
            cromos_por_equipo[equipo] = sorted(cromos_por_equipo[equipo])
        
        st.session_state.cromos_por_equipo = cromos_por_equipo
        st.session_state.lista_equipos = sorted(cromos_por_equipo.keys())
        st.session_state.excel_cargado = True
        st.session_state.excel_nombre = file.name
        
        # Inicializar datos vacíos para cada equipo
        for equipo in st.session_state.lista_equipos:
            if equipo not in st.session_state.datos:
                st.session_state.datos[equipo] = {"faltas": [], "repes": []}
        
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def cargar_json(file):
    """Carga el archivo JSON y fusiona"""
    try:
        datos_json = json.load(file)
        
        # Verificar que los equipos existan en el Excel
        for equipo in list(datos_json.keys()):
            if equipo not in st.session_state.cromos_por_equipo:
                del datos_json[equipo]
        
        # Asegurar que todos los equipos del Excel tengan entrada
        for equipo in st.session_state.lista_equipos:
            if equipo not in datos_json:
                datos_json[equipo] = {"faltas": [], "repes": []}
        
        st.session_state.datos = datos_json
        st.session_state.json_nombre = file.name
        return True
    except Exception as e:
        st.error(f"Error al cargar JSON: {str(e)}")
        return False

# ============================================================
# INTERFAZ
# ============================================================

st.title("🏆 GESTOR DE CROMOS - MUNDIAL 2026 🏆")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📁 1. Cargar Excel")
    
    uploaded_excel = st.file_uploader(
        "Archivo Excel (3 columnas: Equipo, Código, Nombre)",
        type=['xlsx', 'xls'],
        key="excel_upload"
    )
    
    if uploaded_excel is not None and uploaded_excel.name != st.session_state.excel_nombre:
        with st.spinner("Cargando Excel..."):
            if cargar_excel(uploaded_excel):
                st.success(f"✅ {len(st.session_state.lista_equipos)} equipos")
                st.rerun()
    
    if st.session_state.excel_cargado:
        st.info(f"📊 Excel: {len(st.session_state.lista_equipos)} equipos")
    
    st.markdown("---")
    st.header("💾 2. Cargar JSON")
    
    uploaded_json = st.file_uploader(
        "Archivo mi_coleccion_cromos.json",
        type=['json'],
        key="json_upload"
    )
    
    if uploaded_json is not None and uploaded_json.name != st.session_state.json_nombre:
        if st.session_state.excel_cargado:
            with st.spinner("Cargando progreso..."):
                if cargar_json(uploaded_json):
                    st.success(f"✅ Progreso cargado")
                    st.rerun()
        else:
            st.warning("Primero carga el Excel")
    
    # Mostrar estadísticas si hay datos
    if st.session_state.datos and st.session_state.excel_cargado:
        total_faltas = sum(len(d.get("faltas", [])) for d in st.session_state.datos.values())
        total_repes = sum(len(d.get("repes", [])) for d in st.session_state.datos.values())
        st.info(f"📊 {total_faltas} faltas | {total_repes} repes")
    
    st.markdown("---")
    st.header("📊 3. Exportar")
    
    # Botón para guardar JSON
    if st.session_state.datos:
        json_str = json.dumps(st.session_state.datos, indent=4, ensure_ascii=False)
        st.download_button(
            label="💾 Guardar JSON",
            data=json_str,
            file_name=f"mi_coleccion_cromos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Botón para exportar CSV de faltas y repes
    if st.button("📥 Exportar faltas y repes (CSV)", use_container_width=True):
        if st.session_state.datos:
            datos_exp = []
            for equipo, contenido in st.session_state.datos.items():
                for cromo in contenido.get("faltas", []):
                    datos_exp.append({"Equipo": equipo, "Cromo": cromo, "Estado": "FALTA ❌"})
                for cromo in contenido.get("repes", []):
                    datos_exp.append({"Equipo": equipo, "Cromo": cromo, "Estado": "REPETIDO 🔄"})
            
            if datos_exp:
                df_exp = pd.DataFrame(datos_exp)
                csv = df_exp.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Descargar CSV",
                    csv,
                    f"faltas_repes_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv",
                    use_container_width=True
                )

# ============================================================
# CONTENIDO PRINCIPAL
# ============================================================

if not st.session_state.excel_cargado:
    st.info("📋 **Instrucciones:**")
    st.markdown("""
    1. En el panel izquierdo, carga tu archivo **Excel** con el listado completo de cromos
    2. Luego carga tu archivo **JSON** con el progreso guardado
    3. Selecciona un equipo para ver y editar tus cromos
    
    **Formato del Excel:** 3 columnas: Equipo | Código | Nombre
    """)
    
    with st.expander("📝 Ver ejemplo"):
        ejemplo = pd.DataFrame({
            "Equipo": ["España", "España", "Argentina", "FIFA World Cup History"],
            "Código": ["ESP 1", "ESP 2", "ARG 1", "FWC 1"],
            "Nombre": ["Escudo", "Unai Simón", "Escudo", "Logo Mundial"]
        })
        st.dataframe(ejemplo, use_container_width=True)

else:
    # Estadísticas principales
    total_cromos_excel = sum(len(c) for c in st.session_state.cromos_por_equipo.values())
    total_faltas = sum(len(d.get("faltas", [])) for d in st.session_state.datos.values())
    total_repes = sum(len(d.get("repes", [])) for d in st.session_state.datos.values())
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 Equipos", len(st.session_state.lista_equipos))
    col2.metric("🎴 Cromos", total_cromos_excel)
    col3.metric("❌ Faltas", total_faltas)
    col4.metric("🔄 Repes", total_repes)
    
    st.markdown("---")
    
    # Selección de equipo
    col_equipos, col_cromos = st.columns([1, 2])
    
    with col_equipos:
        st.subheader("📋 Equipos")
        
        busqueda = st.text_input("🔍 Buscar", placeholder="Nombre...")
        
        equipos_filtrados = st.session_state.lista_equipos
        if busqueda:
            equipos_filtrados = [e for e in equipos_filtrados if busqueda.lower() in e.lower()]
        
        for equipo in equipos_filtrados:
            faltas_eq = len(st.session_state.datos.get(equipo, {}).get("faltas", []))
            total_eq = len(st.session_state.cromos_por_equipo.get(equipo, []))
            porcentaje = int(((total_eq - faltas_eq) / total_eq) * 100) if total_eq > 0 else 0
            
            icono = obtener_icono(equipo)
            
            if st.button(
                f"{icono} {equipo}",
                key=f"btn_{equipo}",
                use_container_width=True,
                type="secondary" if st.session_state.equipo_actual != equipo else "primary"
            ):
                st.session_state.equipo_actual = equipo
                st.rerun()
    
    with col_cromos:
        if st.session_state.equipo_actual:
            equipo = st.session_state.equipo_actual
            
            if equipo not in st.session_state.cromos_por_equipo:
                st.error(f"Equipo no encontrado")
            else:
                cromos = st.session_state.cromos_por_equipo[equipo]
                
                if equipo not in st.session_state.datos:
                    st.session_state.datos[equipo] = {"faltas": [], "repes": []}
                
                icono = obtener_icono(equipo)
                st.subheader(f"{icono} {equipo}")
                
                faltas = set(st.session_state.datos[equipo].get("faltas", []))
                repes = set(st.session_state.datos[equipo].get("repes", []))
                
                total_eq = len(cromos)
                conseguidos = total_eq - len(faltas)
                porcentaje = int((conseguidos / total_eq) * 100) if total_eq > 0 else 0
                
                st.progress(porcentaje / 100)
                st.caption(f"📊 {conseguidos}/{total_eq} ({porcentaje}%) | 🔄 Repes: {len(repes)}")
                
                st.markdown("---")
                
                # Botones rápidos
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Todo conseguido", use_container_width=True):
                        st.session_state.datos[equipo]["faltas"] = []
                        st.session_state.datos[equipo]["repes"] = []
                        st.rerun()
                with col_b:
                    if st.button("❌ Todo faltas", use_container_width=True):
                        st.session_state.datos[equipo]["faltas"] = cromos.copy()
                        st.session_state.datos[equipo]["repes"] = []
                        st.rerun()
                
                st.markdown("---")
                st.subheader("🎴 Cromos")
                
                # Mostrar cromos en grid de 2 columnas
                for idx in range(0, len(cromos), 2):
                    col1, col2 = st.columns(2)
                    
                    # Primer cromo
                    cromo1 = cromos[idx]
                    conseguido1 = cromo1 not in faltas
                    repetido1 = cromo1 in repes
                    
                    with col1:
                        with st.container(border=True):
                            st.markdown(f"**{cromo1[:50]}**")
                            nuevo_cons1 = st.checkbox("✅", value=conseguido1, key=f"c1_{equipo}_{idx}")
                            nuevo_rep1 = st.checkbox("🔄", value=repetido1, key=f"r1_{equipo}_{idx}", disabled=not nuevo_cons1)
                            
                            if nuevo_cons1 != conseguido1:
                                if nuevo_cons1:
                                    faltas.discard(cromo1)
                                else:
                                    faltas.add(cromo1)
                                    repes.discard(cromo1)
                                st.session_state.datos[equipo]["faltas"] = list(faltas)
                                st.session_state.datos[equipo]["repes"] = list(repes)
                                st.rerun()
                            
                            if nuevo_rep1 != repetido1 and nuevo_cons1:
                                if nuevo_rep1:
                                    repes.add(cromo1)
                                else:
                                    repes.discard(cromo1)
                                st.session_state.datos[equipo]["repes"] = list(repes)
                                st.rerun()
                    
                    # Segundo cromo (si existe)
                    if idx + 1 < len(cromos):
                        cromo2 = cromos[idx + 1]
                        conseguido2 = cromo2 not in faltas
                        repetido2 = cromo2 in repes
                        
                        with col2:
                            with st.container(border=True):
                                st.markdown(f"**{cromo2[:50]}**")
                                nuevo_cons2 = st.checkbox("✅", value=conseguido2, key=f"c2_{equipo}_{idx}")
                                nuevo_rep2 = st.checkbox("🔄", value=repetido2, key=f"r2_{equipo}_{idx}", disabled=not nuevo_cons2)
                                
                                if nuevo_cons2 != conseguido2:
                                    if nuevo_cons2:
                                        faltas.discard(cromo2)
                                    else:
                                        faltas.add(cromo2)
                                        repes.discard(cromo2)
                                    st.session_state.datos[equipo]["faltas"] = list(faltas)
                                    st.session_state.datos[equipo]["repes"] = list(repes)
                                    st.rerun()
                                
                                if nuevo_rep2 != repetido2 and nuevo_cons2:
                                    if nuevo_rep2:
                                        repes.add(cromo2)
                                    else:
                                        repes.discard(cromo2)
                                    st.session_state.datos[equipo]["repes"] = list(repes)
                                    st.rerun()
        else:
            st.info("👈 Selecciona un equipo")

# Footer
st.markdown("---")
st.caption("🏆 Gestor de Cromos - Mundial 2026")