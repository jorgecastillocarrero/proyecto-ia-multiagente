# -*- coding: utf-8 -*-
from fpdf import FPDF

class PDFAgentes(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.set_x(10)
        self.cell(0, 10, 'Proyecto IA Multi-Agente - Arquitectura y Guia', align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

    def titulo_seccion(self, texto):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 102, 204)
        self.ln(5)
        self.set_x(10)
        self.cell(0, 10, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def subtitulo(self, texto):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(51, 51, 51)
        self.ln(3)
        self.set_x(10)
        self.cell(0, 8, texto, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def parrafo(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(10)
        self.multi_cell(0, 6, texto)
        self.ln(3)

    def item_lista(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)
        self.set_x(10)
        self.multi_cell(0, 6, f"  - {texto}")

    def tabla_simple(self, headers, datos, col_widths=None):
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(0, 102, 204)
        self.set_text_color(255, 255, 255)

        if col_widths is None:
            col_widths = [190 // len(headers)] * len(headers)

        self.set_x(10)
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, fill=True, align='C')
        self.ln()

        self.set_font('Helvetica', '', 9)
        self.set_text_color(0, 0, 0)
        fill = False
        for fila in datos:
            self.set_x(10)
            self.set_fill_color(240, 240, 240) if fill else self.set_fill_color(255, 255, 255)
            for i, celda in enumerate(fila):
                self.cell(col_widths[i], 7, str(celda)[:40], border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(5)

    def codigo(self, texto):
        self.set_font('Courier', '', 8)
        self.set_fill_color(245, 245, 245)
        self.set_text_color(50, 50, 50)
        lines = texto.split('\n')
        for line in lines:
            self.set_x(10)
            self.cell(0, 5, line[:95], fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

def crear_pdf():
    pdf = PDFAgentes()

    # ========== PORTADA ==========
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(0, 102, 204)
    pdf.ln(50)
    pdf.cell(0, 20, 'PROYECTO IA MULTI-AGENTE', align='C')
    pdf.ln(15)
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(51, 51, 51)
    pdf.cell(0, 15, 'Arquitectura para ERP Retail', align='C')
    pdf.ln(30)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'Guia de Diseno e Implementacion', align='C')
    pdf.ln(10)
    pdf.cell(0, 10, 'Stack: Laravel + Python + LLM Local', align='C')
    pdf.ln(50)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 10, 'Documento generado con asistencia de Claude AI', align='C')

    # ========== INDICE ==========
    pdf.add_page()
    pdf.titulo_seccion('INDICE')
    pdf.set_font('Helvetica', '', 11)
    indice = [
        "1. Vision General de la Arquitectura",
        "2. Agente Asistente",
        "3. Agente de Alertas",
        "4. Agente de Automatizaciones",
        "5. Agente Predictivo",
        "6. Integracion con ERP Laravel",
        "7. Stack Tecnologico Recomendado",
        "8. Roadmap de Implementacion",
        "9. Tipos de Agentes IA (Guia General)",
        "10. Matriz de Recomendaciones",
        "11. Cuadro: Usuarios, Frontend y Backend",
        "12. Cuadro: Eventos, Acciones y Bases de Datos",
        "13. Cuadro: Agentes IA y Tipos de Busqueda",
        "14. Ejemplos Practicos de Alertas",
        "15. Frontends Especificos por Departamento",
        "16. Compatibilidad Movil (PWA)",
        "17. Flujos de Trabajo y Comunicacion",
        "18. Analisis Flujo RRHH - Sistema de Seleccion"
    ]
    for item in indice:
        pdf.cell(0, 8, item)
        pdf.ln()

    # ========== SECCION 1: VISION GENERAL ==========
    pdf.add_page()
    pdf.titulo_seccion('1. VISION GENERAL DE LA ARQUITECTURA')

    pdf.parrafo('El sistema multi-agente propuesto se estructura en capas para garantizar escalabilidad, '
                'mantenibilidad y separacion de responsabilidades. La arquitectura conecta el ERP existente '
                'en Laravel con una capa de agentes inteligentes desarrollada en Python.')

    pdf.subtitulo('Capas del Sistema')
    capas = [
        ("Presentacion", "ERP Laravel, Dashboard Agentes, API Externa"),
        ("Gateway/Orquestador", "Agent Router (FastAPI), Auth, Rate Limiting"),
        ("Agentes", "Asistente, Alertas, Automatizaciones, Predictivo"),
        ("Servicios Compartidos", "LLM Local (Ollama), Vector Store, Message Queue"),
        ("Datos", "ERP Database + AI Database")
    ]
    pdf.tabla_simple(['Capa', 'Componentes'], capas, [50, 140])

    pdf.subtitulo('Principios de Diseno')
    principios = [
        "Modelo local para control total de datos y privacidad",
        "Comunicacion asincrona via colas de mensajes",
        "Separacion entre ERP (PHP) y Agentes (Python)",
        "Base de datos dedicada para IA (embeddings, historial, modelos)"
    ]
    for p in principios:
        pdf.item_lista(p)

    # ========== SECCION 2: AGENTE ASISTENTE ==========
    pdf.add_page()
    pdf.titulo_seccion('2. AGENTE ASISTENTE')

    pdf.parrafo('El Agente Asistente es la interfaz conversacional principal del sistema. '
                'Permite a los usuarios consultar datos del ERP usando lenguaje natural.')

    pdf.subtitulo('Componentes')
    componentes = [
        "Procesador de Consultas: Interpreta lenguaje natural y clasifica intenciones",
        "Tools (Herramientas): consultar_producto, generar_reporte, buscar_cliente, ver_inventario, estado_pedido, historial_ventas",
        "RAG (Retrieval): Documentacion ERP, manuales, FAQs"
    ]
    for c in componentes:
        pdf.item_lista(c)

    pdf.subtitulo('Casos de Uso')
    casos = [
        ("Consulta stock", "Cuantas unidades tenemos del producto X?"),
        ("Reportes", "Genera un reporte de ventas del mes"),
        ("Estado pedido", "Cual es el estado del pedido #1234?"),
        ("Deudas", "Quienes son los clientes con mayor deuda?")
    ]
    pdf.tabla_simple(['Tipo', 'Ejemplo de Consulta'], casos, [50, 140])

    # ========== SECCION 3: AGENTE ALERTAS ==========
    pdf.add_page()
    pdf.titulo_seccion('3. AGENTE DE ALERTAS')

    pdf.parrafo('El Agente de Alertas realiza monitoreo proactivo del sistema y genera '
                'notificaciones inteligentes basadas en reglas configurables.')

    pdf.subtitulo('Arquitectura')
    componentes = [
        "Scheduler (Cron Jobs): Stock cada 15min, pagos cada hora, anomalias diario",
        "Motor de Reglas: Condiciones configurables con umbrales",
        "Analizador LLM: Prioriza, agrupa y sugiere acciones",
        "Canales de Salida: Email, SMS, Telegram, Dashboard"
    ]
    for c in componentes:
        pdf.item_lista(c)

    pdf.subtitulo('Tipos de Alertas')
    alertas = [
        ("Stock critico", "< 10% umbral", "Alta"),
        ("Pago vencido", "> 30 dias", "Media-Alta"),
        ("Anomalia ventas", "Desviacion > 2 sigma", "Media"),
        ("Pedido retrasado", "> fecha estimada", "Media")
    ]
    pdf.tabla_simple(['Categoria', 'Trigger', 'Prioridad'], alertas, [55, 75, 55])

    # ========== SECCION 4: AGENTE AUTOMATIZACIONES ==========
    pdf.add_page()
    pdf.titulo_seccion('4. AGENTE DE AUTOMATIZACIONES')

    pdf.parrafo('El Agente de Automatizaciones ejecuta acciones automaticas basadas en eventos '
                'o solicitudes, implementando workflows configurables.')

    pdf.subtitulo('Componentes')
    componentes = [
        "Event Listeners: Escucha nuevos pedidos, cambios inventario, triggers usuario",
        "Workflow Engine: EVENTO -> CONDICION -> ACCION -> NOTIFICACION",
        "Approval Flow: Acciones criticas requieren aprobacion humana"
    ]
    for c in componentes:
        pdf.item_lista(c)

    pdf.subtitulo('Acciones Disponibles')
    acciones = [
        ("crear_orden_compra()", "Reposicion automatica de inventario"),
        ("enviar_email()", "Comunicaciones automaticas"),
        ("actualizar_precios()", "Ajustes dinamicos de precios"),
        ("generar_factura()", "Creacion automatica de documentos"),
        ("notificar_proveedor()", "Comunicacion cadena suministro"),
        ("programar_recordatorio()", "Follow-ups automaticos")
    ]
    pdf.tabla_simple(['Funcion', 'Descripcion'], acciones, [70, 120])

    pdf.subtitulo('Ejemplo de Workflow')
    workflow = """WORKFLOW: Reposicion Automatica
TRIGGER: stock(producto) < punto_reorden
IF: proveedor.activo = true
THEN:
  1. calcular_cantidad_optima()
  2. crear_orden_compra()
  3. enviar_email(proveedor)
  4. notificar(compras, "Nueva OC generada")"""
    pdf.codigo(workflow)

    # ========== SECCION 5: AGENTE PREDICTIVO ==========
    pdf.add_page()
    pdf.titulo_seccion('5. AGENTE PREDICTIVO')

    pdf.parrafo('El Agente Predictivo genera predicciones de demanda, ventas y tendencias '
                'utilizando modelos de Machine Learning combinados con interpretacion LLM.')

    pdf.subtitulo('Pipeline de Datos')
    pipeline = [
        "ETL desde ERP: Extraccion automatica de datos historicos",
        "Limpieza y normalizacion: Preparacion de datos para ML",
        "Feature engineering: Creacion de variables predictivas"
    ]
    for p in pipeline:
        pdf.item_lista(p)

    pdf.subtitulo('Modelos ML')
    modelos = [
        ("Prediccion Demanda", "Prophet/LSTM", "Unidades/semana", "Semanal"),
        ("Segmentacion Clientes", "Clustering", "Grupos + estrategias", "Mensual"),
        ("Deteccion Anomalias", "Isolation Forest", "Alertas fraude", "Tiempo real"),
        ("Recomendacion", "Collaborative Filter", "Cross-sell", "Por transaccion")
    ]
    pdf.tabla_simple(['Modelo', 'Algoritmo', 'Output', 'Frecuencia'], modelos, [45, 45, 50, 45])

    pdf.subtitulo('Capa LLM (Interpretacion)')
    interp = [
        "Explicacion de predicciones en lenguaje natural",
        "Generacion de insights y recomendaciones",
        "Respuesta a preguntas sobre tendencias"
    ]
    for i in interp:
        pdf.item_lista(i)

    # ========== SECCION 6: INTEGRACION LARAVEL ==========
    pdf.add_page()
    pdf.titulo_seccion('6. INTEGRACION CON ERP LARAVEL')

    pdf.parrafo('La integracion entre el ERP Laravel existente y la capa de agentes Python '
                'se realiza mediante multiples canales de comunicacion.')

    pdf.subtitulo('Canales de Comunicacion')
    canales = [
        ("HTTP/REST", "Controllers Laravel <-> FastAPI Gateway"),
        ("Message Queue", "Laravel Events -> RabbitMQ/Redis -> Python Consumer"),
        ("Database", "Read-Only Replica para acceso desde Python")
    ]
    pdf.tabla_simple(['Canal', 'Componentes'], canales, [50, 140])

    pdf.subtitulo('Ejemplo: Servicio Laravel')
    codigo_laravel = """// app/Services/AgentService.php
class AgentService {
    public function askAssistant(string $query): array {
        return Http::post(config('agents.gateway_url')
            . '/assistant', [
            'query' => $query,
            'user_id' => auth()->id(),
            'context' => $this->getERPContext()
        ])->json();
    }
}"""
    pdf.codigo(codigo_laravel)

    pdf.subtitulo('Ejemplo: API Gateway Python')
    codigo_python = """# gateway/main.py
from fastapi import FastAPI
app = FastAPI()

@app.post("/assistant")
async def assistant_endpoint(request: AssistantRequest):
    agent = AssistantAgent(llm=ollama_client)
    return await agent.process(request.query, request.context)"""
    pdf.codigo(codigo_python)

    # ========== SECCION 7: STACK TECNOLOGICO ==========
    pdf.add_page()
    pdf.titulo_seccion('7. STACK TECNOLOGICO RECOMENDADO')

    pdf.subtitulo('Modelos Locales Recomendados')
    modelos_llm = [
        ("Mistral 7B", "16 GB", "Tareas generales", "RECOMENDADO"),
        ("Llama 3 8B", "16 GB", "Razonamiento", "Alternativa"),
        ("Mixtral 8x7B", "48 GB", "Alto rendimiento", "Si hay recursos"),
        ("Phi-3", "8 GB", "Recursos limitados", "Ligero")
    ]
    pdf.tabla_simple(['Modelo', 'RAM Min', 'Caso de Uso', 'Nota'], modelos_llm, [40, 30, 60, 55])

    pdf.subtitulo('Stack Completo')
    pdf.parrafo('CAPA EXISTENTE (mantener):')
    exist = ["Laravel 10/11 (PHP 8.2+)", "MySQL/PostgreSQL", "Redis (cache + queues)"]
    for e in exist:
        pdf.item_lista(e)

    pdf.parrafo('CAPA DE AGENTES (nuevo):')
    agentes = ["Python 3.11+", "FastAPI (API Gateway)", "LangChain / LlamaIndex",
               "Ollama (servidor LLM)", "ChromaDB / Qdrant (vector store)"]
    for a in agentes:
        pdf.item_lista(a)

    pdf.parrafo('CAPA ML/PREDICTIVA:')
    ml = ["scikit-learn", "Prophet (series temporales)", "PyTorch (deep learning)", "MLflow (tracking)"]
    for m in ml:
        pdf.item_lista(m)

    pdf.parrafo('INFRAESTRUCTURA:')
    infra = ["Docker + Docker Compose", "RabbitMQ (mensajeria)", "Celery (tareas programadas)", "Nginx (reverse proxy)"]
    for i in infra:
        pdf.item_lista(i)

    pdf.subtitulo('Hardware Minimo Recomendado')
    hw = [
        ("CPU", "8+ cores"),
        ("RAM", "32 GB (64 GB ideal)"),
        ("GPU", "NVIDIA 8+ GB VRAM (RTX 3060+) - opcional"),
        ("Almacenamiento", "500 GB SSD")
    ]
    pdf.tabla_simple(['Componente', 'Especificacion'], hw, [60, 130])

    # ========== SECCION 8: ROADMAP ==========
    pdf.add_page()
    pdf.titulo_seccion('8. ROADMAP DE IMPLEMENTACION')

    pdf.subtitulo('Fase 1: Fundamentos')
    fase1 = [
        "Configurar Ollama + Mistral 7B en servidor",
        "Crear API Gateway con FastAPI",
        "Integrar llamadas basicas desde Laravel",
        "Implementar Agente Asistente (MVP)"
    ]
    for f in fase1:
        pdf.item_lista(f)

    pdf.subtitulo('Fase 2: Monitoreo')
    fase2 = [
        "Sistema de alertas con reglas basicas",
        "Configurar cola de mensajes (Redis/RabbitMQ)",
        "Implementar dashboard de alertas"
    ]
    for f in fase2:
        pdf.item_lista(f)

    pdf.subtitulo('Fase 3: Automatizacion')
    fase3 = [
        "Desarrollar motor de workflows",
        "Implementar acciones automaticas criticas",
        "Crear sistema de aprobaciones"
    ]
    for f in fase3:
        pdf.item_lista(f)

    pdf.subtitulo('Fase 4: Predictivo')
    fase4 = [
        "Construir pipeline de datos",
        "Entrenar modelos de prediccion de demanda",
        "Integrar con decisiones de compra"
    ]
    for f in fase4:
        pdf.item_lista(f)

    # ========== SECCION 9: TIPOS DE AGENTES ==========
    pdf.add_page()
    pdf.titulo_seccion('9. TIPOS DE AGENTES IA (GUIA GENERAL)')

    pdf.subtitulo('9.1 Por Funcion Principal')
    tipos_funcion = [
        ("Asistente Conversacional", "Soporte, consultas"),
        ("Alertas/Monitoreo", "Stock, anomalias, SLAs"),
        ("Automatizacion", "RPA, workflows"),
        ("Predictivo", "Demanda, churn, ventas"),
        ("Analisis", "BI conversacional"),
        ("Busqueda/RAG", "Knowledge base"),
        ("Clasificacion", "Tickets, emails"),
        ("Generacion", "Contenido, documentos"),
        ("Validacion/QA", "Tests, compliance"),
        ("Recomendacion", "Cross-sell, next action")
    ]
    pdf.tabla_simple(['Tipo', 'Uso'], tipos_funcion, [70, 115])

    pdf.subtitulo('9.2 Por Nivel de Autonomia')
    autonomia = [
        ("Reactivo", "Solo responde a inputs", "Chatbot basico"),
        ("Proactivo", "Inicia acciones por triggers", "Alertas"),
        ("Semi-autonomo", "Propone, humano aprueba", "Ordenes compra"),
        ("Autonomo", "Decide y ejecuta solo", "Trading, escalado")
    ]
    pdf.tabla_simple(['Nivel', 'Caracteristica', 'Ejemplo'], autonomia, [45, 75, 65])

    pdf.add_page()
    pdf.subtitulo('9.3 Por Arquitectura Tecnica')
    arquitectura = [
        ("Single Agent", "Un agente, una tarea", "Baja"),
        ("Multi-Agent", "Varios colaborando", "Media-Alta"),
        ("Hierarchical", "Supervisor + workers", "Alta"),
        ("Swarm", "Distribuido sin control central", "Muy Alta")
    ]
    pdf.tabla_simple(['Tipo', 'Descripcion', 'Complejidad'], arquitectura, [50, 85, 50])

    pdf.subtitulo('9.4 Por Area de Negocio')
    areas = [
        ("Ventas", "Lead scoring, propuestas, CRM assistant"),
        ("Marketing", "Contenido, segmentacion, campanas"),
        ("Operaciones", "Inventario, logistica, scheduling"),
        ("Finanzas", "Conciliacion, fraude, forecasting"),
        ("RRHH", "Screening CV, onboarding, consultas"),
        ("IT", "Helpdesk, monitoreo, incidents"),
        ("Legal", "Contratos, auditoria, regulaciones"),
        ("Atencion Cliente", "Soporte L1, escalamiento"),
        ("Produccion", "Mantenimiento predictivo, calidad"),
        ("Compras", "Proveedores, negociacion, ordenes")
    ]
    pdf.tabla_simple(['Area', 'Tipos de Agentes'], areas, [50, 135])

    pdf.subtitulo('9.5 Por Capacidad Tecnica')
    capacidades = [
        ("Tool-Using", "Usa APIs, bases de datos, calculadoras"),
        ("Coding", "Genera y ejecuta codigo"),
        ("Browsing", "Navega web, extrae informacion"),
        ("Memory", "Mantiene contexto largo plazo"),
        ("Planning", "Descompone tareas complejas"),
        ("Reflection", "Auto-evalua y mejora respuestas"),
        ("Multimodal", "Procesa texto, imagen, audio, video")
    ]
    pdf.tabla_simple(['Capacidad', 'Descripcion'], capacidades, [50, 135])

    # ========== SECCION 10: MATRIZ RECOMENDACIONES ==========
    pdf.add_page()
    pdf.titulo_seccion('10. MATRIZ DE RECOMENDACIONES')

    pdf.subtitulo('Evaluacion por Tipo de Agente')
    matriz = [
        ("Asistente/Chat", "Medio", "Baja", "Rapido", "Medio"),
        ("Alertas", "Alto", "Baja", "Rapido", "Alto"),
        ("Automatizacion", "Muy Alto", "Media", "Medio", "Muy Alto"),
        ("Predictivo", "Muy Alto", "Alta", "Largo", "Muy Alto"),
        ("Generacion", "Medio", "Baja", "Rapido", "Medio"),
        ("Analisis/BI", "Alto", "Media", "Medio", "Alto"),
        ("Recomendacion", "Alto", "Media", "Medio", "Alto")
    ]
    pdf.tabla_simple(['Tipo', 'Impacto', 'Dificultad', 'Tiempo', 'ROI'], matriz, [45, 35, 35, 35, 35])

    pdf.subtitulo('Recomendacion por Madurez de IA')

    pdf.parrafo('NIVEL 1 - Inicio:')
    n1 = ["Chatbot FAQ", "Alertas simples", "Busqueda documentos", "Clasificacion basica"]
    for n in n1:
        pdf.item_lista(n)

    pdf.parrafo('NIVEL 2 - Crecimiento:')
    n2 = ["Automatizacion workflows", "Analisis predictivo", "Recomendaciones", "Generacion contenido"]
    for n in n2:
        pdf.item_lista(n)

    pdf.parrafo('NIVEL 3 - Avanzado:')
    n3 = ["Agentes autonomos", "Sistemas multi-agente", "Agentes de decision", "Optimizacion continua"]
    for n in n3:
        pdf.item_lista(n)

    # ========== SECCION 11: CUADRO USUARIOS ==========
    pdf.add_page()
    pdf.titulo_seccion('11. CUADRO: USUARIOS, FRONTEND Y BACKEND')

    pdf.subtitulo('Por Tipo de Usuario')
    usuarios = [
        ("Pescadero", "Operario", "Blade + Vue.js", "Laravel", "MySQL"),
        ("Logistica", "Operario", "Blade + Vue.js", "Laravel", "MySQL"),
        ("Administrativo", "Operario", "Blade + Vue.js", "Laravel", "MySQL"),
        ("Gerente", "Direccion", "Vue.js completo", "Laravel+FastAPI", "PostgreSQL"),
        ("Director", "Direccion", "Vue.js completo", "Laravel+FastAPI", "PostgreSQL")
    ]
    pdf.tabla_simple(['Usuario', 'Rol', 'Frontend', 'Backend', 'BD'], usuarios, [35, 30, 40, 45, 35])

    pdf.subtitulo('Funciones por Usuario')
    funciones = [
        ("Pescadero", "CRUD + Alertas + Chat IA"),
        ("Logistica", "CRUD + Alertas + Chat IA"),
        ("Administrativo", "CRUD + Alertas + Chat IA"),
        ("Gerente", "Dashboards + KPIs + Alertas + Chat IA + Predicciones"),
        ("Director", "Dashboards + KPIs + Alertas + Chat IA + Predicciones")
    ]
    pdf.tabla_simple(['Usuario', 'Funciones Disponibles'], funciones, [45, 145])

    pdf.subtitulo('Frontend: Que se Mantiene y Que se Anade')
    pdf.parrafo('FRONTEND ACTUAL (se mantiene):')
    actual = ["Formularios CRUD", "Tablas con filtros", "Calendario", "Reportes basicos"]
    for a in actual:
        pdf.item_lista(a)

    pdf.parrafo('WIDGETS NUEVOS (se anaden con Vue.js):')
    nuevo = ["Widget Alertas (campanita con notificaciones)", "Widget Chat IA (burbuja de conversacion)"]
    for n in nuevo:
        pdf.item_lista(n)

    # ========== SECCION 12: CUADRO EVENTOS ==========
    pdf.add_page()
    pdf.titulo_seccion('12. CUADRO: EVENTOS, ACCIONES Y BASES DE DATOS')

    pdf.subtitulo('Por Tipo de Evento/Accion')
    eventos = [
        ("Registrar venta", "Pescadero", "Blade", "Laravel", "MySQL", "MySQL"),
        ("Ver stock", "Todos", "Blade", "Laravel", "MySQL", "-"),
        ("Crear pedido", "Logistica", "Blade", "Laravel", "MySQL", "MySQL"),
        ("Facturar", "Administrativo", "Blade", "Laravel", "MySQL", "MySQL"),
        ("Ver dashboard", "Gerencia", "Vue.js", "FastAPI", "PostgreSQL", "-"),
        ("Chat con IA", "Todos", "Vue.js", "FastAPI+Ollama", "PostgreSQL", "-"),
        ("Recibir alerta", "Todos", "Vue.js", "Laravel Echo", "Redis", "-"),
        ("Config workflow", "Gerencia", "Vue.js", "FastAPI", "PostgreSQL", "PostgreSQL"),
        ("Ver predicciones", "Gerencia", "Vue.js", "FastAPI+ML", "PostgreSQL", "-")
    ]
    pdf.tabla_simple(['Evento', 'Usuario', 'Frontend', 'Backend', 'BD Lee', 'BD Escribe'], eventos, [32, 28, 25, 35, 32, 32])

    pdf.subtitulo('Por Tipo de Alerta')
    alertas_tipo = [
        ("Stock bajo", "Agente IA", "Pescadero+Logistica+Gerencia", "Push+Banner"),
        ("Pago vencido", "Agente IA", "Administrativo+Gerencia", "Push+Email"),
        ("Pedido retrasado", "Agente IA", "Logistica+Gerencia", "Push"),
        ("Anomalia ventas", "Agente IA", "Gerencia", "Push+Dashboard"),
        ("Error datos", "Agente IA", "Responsable del dato", "Push+Banner"),
        ("Tarea asignada", "Gerencia", "Trabajador asignado", "Push+Banner")
    ]
    pdf.tabla_simple(['Alerta', 'Quien Crea', 'Destinatarios', 'Canal'], alertas_tipo, [40, 35, 65, 45])

    # ========== SECCION 13: CUADRO AGENTES ==========
    pdf.add_page()
    pdf.titulo_seccion('13. CUADRO: AGENTES IA Y TIPOS DE BUSQUEDA')

    pdf.subtitulo('Por Agente IA')
    agentes_bd = [
        ("Asistente", "Responde preguntas", "FastAPI+Ollama", "PostgreSQL", "ChromaDB"),
        ("Alertas", "Detecta anomalias", "FastAPI+Celery", "PostgreSQL", "Redis"),
        ("Automatizacion", "Ejecuta workflows", "FastAPI+Celery", "PostgreSQL", "MySQL"),
        ("Documentos", "Busca en docs", "FastAPI+Ollama", "ChromaDB", "-"),
        ("Predictivo", "Genera pronosticos", "FastAPI+ML", "PostgreSQL", "-")
    ]
    pdf.tabla_simple(['Agente', 'Funcion', 'Backend', 'BD Principal', 'BD Secund.'], agentes_bd, [35, 40, 40, 40, 30])

    pdf.subtitulo('Por Tipo de Busqueda')
    busquedas = [
        ("SQL directo", "Asistente, Alertas, Predictivo", "SQLAlchemy", "PostgreSQL", "< 100ms"),
        ("Tiempo real", "Alertas", "Laravel Echo", "Redis", "< 50ms"),
        ("Semantica RAG", "Documentos, Asistente", "LangChain", "ChromaDB", "< 300ms"),
        ("Series tiempo", "Predictivo", "Prophet/LSTM", "PostgreSQL", "< 500ms"),
        ("Trigger/Evento", "Automatizacion", "Laravel Events", "MySQL->PostgreSQL", "< 200ms")
    ]
    pdf.tabla_simple(['Tipo Busqueda', 'Agentes', 'Tecnologia', 'BD', 'Velocidad'], busquedas, [35, 50, 35, 45, 25])

    pdf.subtitulo('Resumen de Bases de Datos')
    bds = [
        ("MySQL", "Datos operativos ERP", "Automatizacion (escribir)"),
        ("PostgreSQL", "Analitica, historicos, metricas", "Todos (leer)"),
        ("ChromaDB", "Embeddings de documentos", "Documentos, Asistente"),
        ("Redis", "Cache, umbrales, sesiones", "Alertas, Asistente")
    ]
    pdf.tabla_simple(['Base de Datos', 'Que Guarda', 'Agentes que la Usan'], bds, [40, 75, 75])

    # ========== SECCION 14: EJEMPLOS ALERTAS ==========
    pdf.add_page()
    pdf.titulo_seccion('14. EJEMPLOS PRACTICOS DE ALERTAS')

    pdf.subtitulo('Ejemplo 1: Alerta de Error (Precio = 0)')
    pdf.parrafo('El agente de verificacion detecta automaticamente errores en los datos '
                'y crea alertas que persisten hasta que el error se corrija.')

    ejemplo1 = [
        ("1", "Agente IA", "Detecta producto con precio = 0.00"),
        ("2", "Agente IA", "Crea alerta asignada a responsable"),
        ("3", "Maria (Admin)", "Ve alerta en su panel"),
        ("4", "Maria (Admin)", "Corrige precio en ERP: 7.50 euros"),
        ("5", "Agente IA", "Verifica precio > 0, cierra alerta")
    ]
    pdf.tabla_simple(['Paso', 'Quien', 'Accion'], ejemplo1, [20, 45, 125])

    pdf.parrafo('Caracteristicas de este tipo de alerta:')
    caract1 = [
        "Creacion: Automatica por el Agente IA",
        "Asignacion: Al responsable del dato (ej: administrativo de productos)",
        "Persistencia: No desaparece hasta que el dato se corrija",
        "Cierre: Automatico cuando la condicion se cumple (precio > 0)"
    ]
    for c in caract1:
        pdf.item_lista(c)

    pdf.add_page()
    pdf.subtitulo('Ejemplo 2: Alerta de Progreso (Llamadas CV)')
    pdf.parrafo('Gerencia asigna tareas con seguimiento de progreso. '
                'El sistema actualiza automaticamente el estado X/Y.')

    ejemplo2 = [
        ("1", "Gerencia", "Selecciona 20 CVs en dashboard"),
        ("2", "Gerencia", "Asigna tarea a Laura (RRHH)"),
        ("3", "Laura", "Ve alerta: 0/20 llamadas pendientes"),
        ("4", "Laura", "Llama candidato, confirma cita, registra fecha"),
        ("5", "Sistema", "Actualiza automaticamente: 1/20"),
        ("6", "Laura", "Completa todas las llamadas"),
        ("7", "Sistema", "20/20 completadas, cierra alerta")
    ]
    pdf.tabla_simple(['Paso', 'Quien', 'Accion'], ejemplo2, [20, 35, 135])

    pdf.parrafo('Caracteristicas de este tipo de alerta:')
    caract2 = [
        "Creacion: Manual por Gerencia desde dashboard",
        "Asignacion: A trabajador especifico (ej: RRHH)",
        "Progreso: Muestra X/Y tareas completadas",
        "Actualizacion: Automatica cuando trabajador registra accion",
        "Cierre: Automatico cuando progreso = 100%"
    ]
    for c in caract2:
        pdf.item_lista(c)

    pdf.subtitulo('Comparativa de Tipos de Alerta')
    comparativa = [
        ("Error (Precio=0)", "Agente IA", "Error/Anomalia", "No", "Auto (dato OK)"),
        ("Progreso (CVs)", "Gerencia", "Seguimiento", "Si (X/Y)", "Auto (100%)"),
        ("Vencimiento", "Agente IA", "Tiempo limite", "No", "Auto (pagado)"),
        ("Manual", "Usuario", "Recordatorio", "No", "Manual")
    ]
    pdf.tabla_simple(['Tipo', 'Quien Crea', 'Categoria', 'Progreso', 'Cierre'], comparativa, [40, 30, 40, 30, 45])

    # ========== SECCION 15: FRONTENDS ESPECIFICOS ==========
    pdf.add_page()
    pdf.titulo_seccion('15. FRONTENDS ESPECIFICOS POR DEPARTAMENTO')

    pdf.parrafo('Se crearan 11 frontends especificos con Vue.js, cada uno optimizado para las '
                'necesidades de su departamento. El ERP base (Blade + jQuery) se mantiene para '
                'funcionalidades que no tengan frontend especifico.')

    pdf.subtitulo('15.1 Lista de Frontends a Desarrollar')
    frontends = [
        ("1. RRHH", "/rrhh/*", "CVs, entrevistas, nominas, alertas personal"),
        ("2. Administrativo", "/admin/*", "Facturas, pagos, cobros, alertas contables"),
        ("3. Tiendas", "/tiendas/*", "Ventas, stock, pedidos rapidos, alertas producto"),
        ("4. Logistica", "/logistica/*", "Rutas, entregas, tracking, alertas envios"),
        ("5. Compras", "/compras/*", "Proveedores, ordenes, precios, alertas stock"),
        ("6. Comercial", "/comercial/*", "Clientes, ofertas, visitas, alertas ventas"),
        ("7. Calidad", "/calidad/*", "Controles, incidencias, trazabilidad"),
        ("8. Almacen", "/almacen/*", "Entradas, salidas, inventario, ubicaciones"),
        ("9. Contabilidad", "/contabilidad/*", "Asientos, balances, impuestos, cierres"),
        ("10. Produccion", "/produccion/*", "Elaborados, recetas, costes, mermas"),
        ("11. Gerencia", "/gerencia/*", "Dashboards, KPIs, predicciones, vision global")
    ]
    pdf.tabla_simple(['Frontend', 'Ruta', 'Funciones Especificas'], frontends, [40, 35, 115])

    pdf.add_page()
    pdf.subtitulo('15.2 Caracteristicas Comunes de Todos los Frontends')
    comunes = [
        "Desarrollados con Vue.js 3 + Inertia.js",
        "Diseno responsive con Tailwind CSS",
        "Widget de alertas integrado (campanita)",
        "Widget de chat IA integrado",
        "Conexion a API Laravel compartida",
        "Autenticacion y permisos por rol"
    ]
    for c in comunes:
        pdf.item_lista(c)

    pdf.subtitulo('15.3 Funciones Especificas por Frontend')

    pdf.parrafo('RRHH:')
    rrhh = ["Gestion de candidatos y CVs", "Seguimiento de entrevistas (X/Y completadas)",
            "Control de nominas", "Alertas de personal (ausencias, vencimientos)"]
    for r in rrhh:
        pdf.item_lista(r)

    pdf.parrafo('ADMINISTRATIVO:')
    admin = ["Facturacion y cobros", "Control de pagos a proveedores",
             "Alertas de vencimientos", "Conciliacion bancaria"]
    for a in admin:
        pdf.item_lista(a)

    pdf.parrafo('TIENDAS:')
    tiendas = ["Punto de venta optimizado", "Consulta de stock en tiempo real",
               "Pedidos rapidos al almacen", "Alertas de productos (precio 0, stock bajo)"]
    for t in tiendas:
        pdf.item_lista(t)

    pdf.parrafo('LOGISTICA:')
    logistica = ["Gestion de rutas de reparto", "Tracking de entregas",
                 "Confirmacion de recepciones", "Alertas de pedidos retrasados"]
    for l in logistica:
        pdf.item_lista(l)

    pdf.add_page()
    pdf.parrafo('COMPRAS:')
    compras = ["Gestion de proveedores", "Ordenes de compra automaticas",
               "Comparativa de precios", "Alertas de stock minimo"]
    for c in compras:
        pdf.item_lista(c)

    pdf.parrafo('COMERCIAL:')
    comercial = ["Cartera de clientes", "Seguimiento de ofertas",
                 "Registro de visitas", "Alertas de oportunidades"]
    for c in comercial:
        pdf.item_lista(c)

    pdf.parrafo('CALIDAD:')
    calidad = ["Controles de calidad", "Registro de incidencias",
               "Trazabilidad de productos", "Alertas de no conformidades"]
    for c in calidad:
        pdf.item_lista(c)

    pdf.parrafo('ALMACEN:')
    almacen = ["Entradas y salidas de mercancia", "Control de ubicaciones",
               "Inventarios y recuentos", "Alertas de caducidades"]
    for a in almacen:
        pdf.item_lista(a)

    pdf.parrafo('CONTABILIDAD:')
    contabilidad = ["Asientos contables", "Balances y cuentas",
                    "Gestion de impuestos", "Cierres mensuales/anuales"]
    for c in contabilidad:
        pdf.item_lista(c)

    pdf.parrafo('PRODUCCION:')
    produccion = ["Gestion de elaborados", "Recetas y escandallos",
                  "Control de costes", "Alertas de mermas"]
    for p in produccion:
        pdf.item_lista(p)

    pdf.parrafo('GERENCIA:')
    gerencia = ["Dashboards con KPIs en tiempo real", "Graficos y predicciones IA",
                "Vision global de todos los departamentos", "Asignacion de tareas con seguimiento",
                "Chat IA avanzado con acceso a todos los datos"]
    for g in gerencia:
        pdf.item_lista(g)

    pdf.add_page()
    pdf.subtitulo('15.4 Orden de Desarrollo Sugerido')
    orden = [
        ("Fase 1", "Gerencia", "Toma decisiones, necesita KPIs primero"),
        ("Fase 2", "Tiendas", "Mayor volumen de usuarios"),
        ("Fase 3", "Administrativo", "Gestiona alertas de pagos/cobros"),
        ("Fase 4", "RRHH", "Gestion de personal y entrevistas"),
        ("Fase 5", "Logistica", "Control de entregas y rutas"),
        ("Fase 6", "Compras", "Ordenes automaticas y proveedores"),
        ("Fase 7", "Almacen", "Control de stock y ubicaciones"),
        ("Fase 8", "Comercial", "Seguimiento de clientes"),
        ("Fase 9", "Contabilidad", "Gestion contable"),
        ("Fase 10", "Calidad", "Controles e incidencias"),
        ("Fase 11", "Produccion", "Elaborados y costes")
    ]
    pdf.tabla_simple(['Fase', 'Frontend', 'Justificacion'], orden, [25, 40, 125])

    pdf.subtitulo('15.5 Arquitectura Tecnica')
    pdf.parrafo('Todos los frontends comparten:')
    arquitectura = [
        "Backend unico: Laravel 11 con API REST",
        "Base de datos: MySQL (operativo) + PostgreSQL (analitica)",
        "Agentes IA: FastAPI + Ollama (compartidos)",
        "Alertas: Laravel Echo + WebSockets (compartido)",
        "Autenticacion: Laravel Sanctum con permisos por rol"
    ]
    for a in arquitectura:
        pdf.item_lista(a)

    pdf.subtitulo('15.6 ERP Base (Se Mantiene)')
    pdf.parrafo('El ERP actual con Blade + jQuery se mantiene para:')
    erp_base = [
        "Funcionalidades sin frontend especifico asignado",
        "Usuarios con multiples roles",
        "Acceso de emergencia si falla un frontend especifico",
        "Migracion gradual (hasta que todos los frontends esten listos)"
    ]
    for e in erp_base:
        pdf.item_lista(e)

    # ========== SECCION 16: COMPATIBILIDAD MOVIL ==========
    pdf.add_page()
    pdf.titulo_seccion('16. COMPATIBILIDAD MOVIL (PWA)')

    pdf.parrafo('Todos los frontends Vue.js seran compatibles con dispositivos moviles '
                'mediante PWA (Progressive Web App), permitiendo acceso desde smartphones '
                'y tablets sin necesidad de publicar en App Store o Google Play.')

    pdf.subtitulo('16.1 Opciones de Acceso Movil')
    opciones_movil = [
        ("Web Responsive", "Vue.js + Tailwind", "Navegador movil", "Inmediato"),
        ("PWA", "Service Worker + Manifest", "Instalable como app", "Recomendado"),
        ("App Hibrida", "Ionic + Vue o Capacitor", "App nativa", "Opcional"),
        ("App Nativa", "Flutter / React Native", "Stores (iOS/Android)", "Futuro")
    ]
    pdf.tabla_simple(['Opcion', 'Tecnologia', 'Resultado', 'Estado'], opciones_movil, [40, 55, 50, 40])

    pdf.subtitulo('16.2 PWA - Recomendado')
    pdf.parrafo('PWA (Progressive Web App) es la opcion recomendada porque:')
    pwa_ventajas = [
        "Se instala desde el navegador (sin App Store)",
        "Funciona offline (con datos en cache)",
        "Recibe notificaciones push (alertas)",
        "Acceso rapido desde icono en pantalla",
        "Actualizaciones automaticas (sin reinstalar)",
        "Un solo desarrollo para web y movil",
        "Sin costes de publicacion en stores"
    ]
    for p in pwa_ventajas:
        pdf.item_lista(p)

    pdf.subtitulo('16.3 Funciones por Dispositivo')
    funciones_movil = [
        ("Tiendas", "Movil/Tablet", "Ventas rapidas, consulta stock, alertas"),
        ("Logistica", "Movil", "Rutas, entregas, confirmaciones, GPS"),
        ("Comercial", "Movil/Tablet", "Visitas clientes, pedidos, fotos"),
        ("Almacen", "Tablet", "Entradas/salidas, escaneo, ubicaciones"),
        ("RRHH", "Escritorio", "Gestion CVs, entrevistas (menos movil)"),
        ("Gerencia", "Tablet/Escritorio", "Dashboards, KPIs, decisiones"),
        ("Administrativo", "Escritorio", "Facturacion, contabilidad")
    ]
    pdf.tabla_simple(['Frontend', 'Dispositivo Principal', 'Funciones Movil'], funciones_movil, [40, 50, 100])

    pdf.add_page()
    pdf.subtitulo('16.4 Caracteristicas PWA por Frontend')

    pdf.parrafo('TIENDAS (Alta prioridad movil):')
    tiendas_movil = [
        "Punto de venta tactil optimizado",
        "Escaneo de codigos de barras con camara",
        "Consulta de precios y stock en tiempo real",
        "Alertas push de productos",
        "Funciona offline (sincroniza al conectar)"
    ]
    for t in tiendas_movil:
        pdf.item_lista(t)

    pdf.parrafo('LOGISTICA (Alta prioridad movil):')
    logistica_movil = [
        "Lista de entregas del dia",
        "Navegacion GPS integrada",
        "Confirmacion de entrega con firma",
        "Foto de entrega como comprobante",
        "Alertas de pedidos urgentes"
    ]
    for l in logistica_movil:
        pdf.item_lista(l)

    pdf.parrafo('COMERCIAL (Media prioridad movil):')
    comercial_movil = [
        "Ficha de cliente con historial",
        "Registro de visitas con geolocalizacion",
        "Creacion de pedidos en campo",
        "Catalogo de productos con fotos",
        "Alertas de oportunidades"
    ]
    for c in comercial_movil:
        pdf.item_lista(c)

    pdf.parrafo('ALMACEN (Tablet recomendado):')
    almacen_movil = [
        "Escaneo de codigos para entradas/salidas",
        "Consulta de ubicaciones",
        "Inventario con contador tactil",
        "Alertas de caducidades proximas"
    ]
    for a in almacen_movil:
        pdf.item_lista(a)

    pdf.add_page()
    pdf.subtitulo('16.5 Notificaciones Push')
    pdf.parrafo('Las alertas del sistema llegaran como notificaciones push al movil:')
    push = [
        "Stock bajo: Notificacion a tienda y almacen",
        "Pedido urgente: Notificacion a logistica",
        "Pago vencido: Notificacion a administrativo",
        "Tarea asignada: Notificacion al responsable",
        "Error detectado: Notificacion al encargado del dato"
    ]
    for p in push:
        pdf.item_lista(p)

    pdf.subtitulo('16.6 Requisitos Tecnicos PWA')
    requisitos = [
        ("HTTPS", "Obligatorio para PWA", "Ya disponible"),
        ("Service Worker", "Cache y offline", "Configurar"),
        ("Web Manifest", "Icono y nombre app", "Configurar"),
        ("Push API", "Notificaciones", "Laravel + Firebase/Pusher"),
        ("Responsive", "Adaptacion pantalla", "Tailwind CSS")
    ]
    pdf.tabla_simple(['Requisito', 'Funcion', 'Estado'], requisitos, [45, 75, 65])

    pdf.subtitulo('16.7 Orden de Implementacion Movil')
    orden_movil = [
        ("Fase 1", "Todos los frontends responsive", "Base para movil"),
        ("Fase 2", "PWA en Tiendas y Logistica", "Mayor uso movil"),
        ("Fase 3", "PWA en Comercial y Almacen", "Uso en campo"),
        ("Fase 4", "Notificaciones push", "Alertas en tiempo real"),
        ("Fase 5", "Funciones offline", "Sincronizacion diferida")
    ]
    pdf.tabla_simple(['Fase', 'Accion', 'Objetivo'], orden_movil, [25, 80, 85])

    # ========== SECCION 17: FLUJOS DE TRABAJO ==========
    pdf.add_page()
    pdf.titulo_seccion('17. FLUJOS DE TRABAJO Y COMUNICACION')

    pdf.parrafo('Esta seccion detalla los flujos de comunicacion entre todos los componentes '
                'del sistema: usuarios, frontends, backends, agentes IA y bases de datos.')

    pdf.subtitulo('17.1 Flujo de Arquitectura General')
    pdf.parrafo('Diagrama de capas del sistema completo:')

    flujo_arq = [
        ("Capa 1", "USUARIOS", "Gerencia, Operarios, Tiendas, etc."),
        ("Capa 2", "FRONTENDS", "Vue.js (11 apps) + ERP Base (Blade)"),
        ("Capa 3", "API GATEWAY", "Laravel (REST) + FastAPI (IA)"),
        ("Capa 4", "SERVICIOS", "Agentes IA, ML, Notificaciones"),
        ("Capa 5", "DATOS", "MySQL + PostgreSQL + ChromaDB + Redis")
    ]
    pdf.tabla_simple(['Capa', 'Componente', 'Descripcion'], flujo_arq, [25, 45, 120])

    pdf.parrafo('Flujo de comunicacion entre capas:')
    flujo_capas = [
        ("Usuario", "->", "Frontend", "Acciones del usuario"),
        ("Frontend", "->", "Laravel API", "Peticiones HTTP/REST"),
        ("Laravel API", "->", "MySQL", "Operaciones CRUD"),
        ("Laravel API", "->", "FastAPI", "Consultas a agentes IA"),
        ("FastAPI", "->", "PostgreSQL", "Consultas analiticas"),
        ("FastAPI", "->", "Ollama", "Procesamiento LLM"),
        ("Agentes IA", "->", "Redis", "Cache y estado alertas"),
        ("Laravel Echo", "->", "Frontend", "Notificaciones push")
    ]
    pdf.tabla_simple(['Origen', '', 'Destino', 'Proposito'], flujo_capas, [40, 15, 45, 90])

    pdf.add_page()
    pdf.subtitulo('17.2 Flujo de Frontend por Tipo de Usuario')

    pdf.parrafo('Flujo para OPERARIOS (Tiendas, Logistica, Almacen):')
    flujo_operario = [
        ("1", "Usuario abre app (PWA o web)"),
        ("2", "Frontend Vue.js carga datos desde Laravel API"),
        ("3", "Usuario realiza accion (venta, entrada, etc.)"),
        ("4", "Frontend envia POST a Laravel API"),
        ("5", "Laravel guarda en MySQL"),
        ("6", "Laravel dispara evento (si aplica)"),
        ("7", "Evento sincroniza a PostgreSQL (ETL)"),
        ("8", "Si hay alerta, Laravel Echo notifica en tiempo real")
    ]
    pdf.tabla_simple(['Paso', 'Accion'], flujo_operario, [20, 170])

    pdf.parrafo('Flujo para GERENCIA (Dashboard, KPIs, Chat IA):')
    flujo_gerencia = [
        ("1", "Gerente abre dashboard Vue.js"),
        ("2", "Frontend solicita KPIs a FastAPI"),
        ("3", "FastAPI consulta PostgreSQL (datos agregados)"),
        ("4", "Graficos ApexCharts renderizan datos"),
        ("5", "Gerente usa chat IA: pregunta algo"),
        ("6", "Frontend envia pregunta a FastAPI"),
        ("7", "FastAPI consulta PostgreSQL + ChromaDB + Ollama"),
        ("8", "Respuesta IA se muestra en chat")
    ]
    pdf.tabla_simple(['Paso', 'Accion'], flujo_gerencia, [20, 170])

    pdf.add_page()
    pdf.subtitulo('17.3 Flujo de Comunicacion de Agentes IA')

    pdf.parrafo('Como se comunican los agentes entre si y con los usuarios:')

    flujo_agentes = [
        ("Asistente", "Recibe pregunta", "FastAPI", "PostgreSQL + ChromaDB"),
        ("Alertas", "Detecta anomalia", "Celery (cron)", "PostgreSQL + Redis"),
        ("Automatizacion", "Ejecuta workflow", "Celery (evento)", "PostgreSQL + MySQL"),
        ("Predictivo", "Genera pronostico", "FastAPI (manual)", "PostgreSQL"),
        ("Documentos", "Busca en docs", "FastAPI", "ChromaDB")
    ]
    pdf.tabla_simple(['Agente', 'Trigger', 'Backend', 'BD que Usa'], flujo_agentes, [40, 45, 45, 60])

    pdf.parrafo('Flujo de una ALERTA (desde deteccion hasta usuario):')
    flujo_alerta = [
        ("1", "Agente Alertas", "Celery ejecuta job cada 15 min"),
        ("2", "Agente Alertas", "Consulta PostgreSQL: SELECT productos WHERE precio = 0"),
        ("3", "Agente Alertas", "Encuentra anomalia: Lubina precio 0.00"),
        ("4", "Agente Alertas", "Crea registro en tabla 'alertas' (PostgreSQL)"),
        ("5", "Agente Alertas", "Publica evento en Redis (canal alertas)"),
        ("6", "Laravel Echo", "Escucha Redis, detecta nueva alerta"),
        ("7", "Laravel Echo", "Envia push via WebSocket al frontend del responsable"),
        ("8", "Frontend Vue", "Muestra notificacion en campanita del usuario")
    ]
    pdf.tabla_simple(['Paso', 'Componente', 'Accion'], flujo_alerta, [20, 45, 125])

    pdf.add_page()
    pdf.subtitulo('17.4 Flujo de Base de Datos (Sincronizacion)')

    pdf.parrafo('Como se mantienen sincronizadas MySQL y PostgreSQL:')

    flujo_sync = [
        ("1", "Operario", "Registra venta en ERP"),
        ("2", "Laravel", "INSERT en MySQL (tabla ventas)"),
        ("3", "Laravel", "Dispara evento VentaCreada"),
        ("4", "Listener", "Escucha evento, transforma datos"),
        ("5", "Listener", "INSERT en PostgreSQL (fact_ventas)"),
        ("6", "PostgreSQL", "Dato disponible para agentes IA"),
        ("7", "Agente", "Consulta PostgreSQL para analisis")
    ]
    pdf.tabla_simple(['Paso', 'Componente', 'Accion'], flujo_sync, [20, 40, 130])

    pdf.parrafo('Estrategia de sincronizacion por tipo de dato:')
    sync_tipo = [
        ("Ventas", "Tiempo real", "Evento Laravel", "< 1 segundo"),
        ("Stock", "Tiempo real", "Evento Laravel", "< 1 segundo"),
        ("Clientes", "Cada 15 min", "Job ETL", "15 minutos"),
        ("Productos", "Cada 15 min", "Job ETL", "15 minutos"),
        ("Historicos", "Cada noche", "Job nocturno", "1 vez/dia")
    ]
    pdf.tabla_simple(['Dato', 'Frecuencia', 'Metodo', 'Latencia'], sync_tipo, [40, 40, 50, 55])

    pdf.add_page()
    pdf.subtitulo('17.5 Flujo de Comunicacion Eficiente')

    pdf.parrafo('Reglas para evitar cuellos de botella:')
    reglas = [
        "MySQL solo para CRUD operativo (escrituras frecuentes)",
        "PostgreSQL solo para LECTURAS analiticas (nunca escribir desde ERP)",
        "Redis como intermediario de mensajes (no consultas directas)",
        "ChromaDB solo para busquedas semanticas (documentos)",
        "Agentes NUNCA escriben en MySQL directamente",
        "Alertas se cachean en Redis para no reconsultar"
    ]
    for r in reglas:
        pdf.item_lista(r)

    pdf.parrafo('Flujo de escritura vs lectura:')
    flujo_rw = [
        ("Operario escribe", "Frontend -> Laravel -> MySQL", "Rapido, transaccional"),
        ("Sync a analitica", "MySQL -> Evento -> PostgreSQL", "Asincrono, no bloquea"),
        ("Gerencia lee", "Frontend -> FastAPI -> PostgreSQL", "Optimizado para lectura"),
        ("Agente consulta", "Agente -> PostgreSQL", "Indices y vistas materializadas"),
        ("Agente alerta", "Agente -> Redis -> Laravel Echo", "Tiempo real, sin BD")
    ]
    pdf.tabla_simple(['Accion', 'Flujo', 'Caracteristica'], flujo_rw, [45, 80, 65])

    pdf.add_page()
    pdf.subtitulo('17.6 Flujo Completo: Ejemplo Practico')

    pdf.parrafo('Escenario: Pescadero vende producto con precio 0, se detecta y corrige.')

    ejemplo_completo = [
        ("1", "Pescadero", "Registra venta de Lubina en tienda"),
        ("2", "Laravel", "Guarda venta en MySQL"),
        ("3", "Evento", "VentaCreada -> sincroniza a PostgreSQL"),
        ("4", "Agente Alertas", "Job cada 15 min: detecta precio = 0"),
        ("5", "Agente Alertas", "Crea alerta en PostgreSQL"),
        ("6", "Redis", "Publica mensaje: nueva alerta"),
        ("7", "Laravel Echo", "Detecta mensaje, busca responsable"),
        ("8", "WebSocket", "Envia push a Maria (admin productos)"),
        ("9", "Maria", "Ve notificacion en su pantalla"),
        ("10", "Maria", "Abre producto, corrige precio a 7.50"),
        ("11", "Laravel", "UPDATE en MySQL (precio = 7.50)"),
        ("12", "Evento", "ProductoActualizado -> sincroniza PostgreSQL"),
        ("13", "Agente Alertas", "Siguiente job: verifica condicion"),
        ("14", "Agente Alertas", "Precio > 0 = TRUE, cierra alerta"),
        ("15", "Maria", "Ve que la alerta desaparecio automaticamente")
    ]
    pdf.tabla_simple(['Paso', 'Quien/Que', 'Accion'], ejemplo_completo, [20, 40, 130])

    pdf.add_page()
    pdf.subtitulo('17.7 Diagrama de Conexiones entre Componentes')

    pdf.parrafo('Resumen de todas las conexiones del sistema:')
    conexiones = [
        ("Frontend Vue", "Laravel API", "HTTP/REST", "Peticiones usuario"),
        ("Frontend Vue", "Laravel Echo", "WebSocket", "Alertas tiempo real"),
        ("Laravel API", "MySQL", "TCP/SQL", "CRUD operativo"),
        ("Laravel API", "FastAPI", "HTTP/REST", "Consultas IA"),
        ("Laravel API", "Redis", "TCP", "Cache y colas"),
        ("FastAPI", "PostgreSQL", "TCP/SQL", "Consultas analiticas"),
        ("FastAPI", "Ollama", "HTTP", "Procesamiento LLM"),
        ("FastAPI", "ChromaDB", "HTTP", "Busqueda semantica"),
        ("Celery", "Redis", "TCP", "Cola de tareas"),
        ("Celery", "PostgreSQL", "TCP/SQL", "Jobs de agentes"),
        ("Laravel Echo", "Redis", "Pub/Sub", "Mensajes tiempo real")
    ]
    pdf.tabla_simple(['Origen', 'Destino', 'Protocolo', 'Uso'], conexiones, [40, 40, 40, 70])

    pdf.subtitulo('17.8 Resumen de Puertos y Servicios')
    puertos = [
        ("Laravel API", "8000", "HTTP", "API principal"),
        ("FastAPI", "8001", "HTTP", "Gateway IA"),
        ("MySQL", "3306", "TCP", "BD operativa"),
        ("PostgreSQL", "5432", "TCP", "BD analitica"),
        ("Redis", "6379", "TCP", "Cache/mensajes"),
        ("Ollama", "11434", "HTTP", "LLM local"),
        ("ChromaDB", "8002", "HTTP", "Vector store"),
        ("WebSocket", "6001", "WS", "Notificaciones")
    ]
    pdf.tabla_simple(['Servicio', 'Puerto', 'Protocolo', 'Funcion'], puertos, [45, 30, 35, 80])

    # ========== SECCION 18: ANALISIS FLUJO RRHH ==========
    pdf.add_page()
    pdf.titulo_seccion('18. ANALISIS FLUJO RRHH - SISTEMA DE SELECCION')

    pdf.parrafo('Esta seccion mapea el flujo de trabajo de seleccion de personal (RRHH) '
                'al sistema multi-agente, detallando que componentes intervienen en cada paso.')

    pdf.subtitulo('18.1 Vision General del Proceso')
    pdf.parrafo('El proceso de seleccion de personal se divide en 6 fases principales, '
                'cada una con diferentes niveles de automatizacion e intervencion humana.')

    fases_rrhh = [
        ("1. Entrada CVs", "Automatico", "Alta", "Agente Documentos + Automatizacion"),
        ("2. Primera Criba", "Automatico", "Alta", "Agente Alertas + Asistente"),
        ("3. Segunda Criba", "Semi-auto", "Media", "Frontend RRHH + Asistente"),
        ("4. Llamadas", "Manual", "Baja", "Frontend RRHH + Alertas"),
        ("5. Entrevistas", "Manual", "Baja", "Frontend RRHH"),
        ("6. Reactivacion", "Automatico", "Alta", "Agente Alertas")
    ]
    pdf.tabla_simple(['Fase', 'Tipo', 'Automatizacion', 'Componentes IA'], fases_rrhh, [40, 30, 35, 85])

    pdf.add_page()
    pdf.subtitulo('18.2 Fase 1: Entrada de CVs')
    pdf.parrafo('Los CVs llegan por multiples canales y se procesan automaticamente.')

    entrada_cvs = [
        ("Email (cv@empresa.com)", "Agente Automatizacion", "Detecta adjuntos PDF/DOC"),
        ("Portal web", "Laravel API", "Formulario de candidatos"),
        ("LinkedIn", "Agente Automatizacion", "Scraping autorizado"),
        ("Agencias", "Email/API", "Integracion con ETTs")
    ]
    pdf.tabla_simple(['Canal Entrada', 'Componente', 'Accion'], entrada_cvs, [50, 50, 90])

    pdf.parrafo('Stack tecnologico de esta fase:')
    stack_fase1 = [
        ("Frontend", "-", "No hay interaccion de usuario"),
        ("Backend", "Laravel + FastAPI", "Recepcion y procesamiento"),
        ("Agente", "Documentos + Automatizacion", "Extraccion de texto del CV"),
        ("BD Escribe", "PostgreSQL", "Tabla candidatos + embeddings"),
        ("BD Lee", "ChromaDB", "Indexacion semantica del CV")
    ]
    pdf.tabla_simple(['Componente', 'Tecnologia', 'Funcion'], stack_fase1, [40, 60, 90])

    pdf.parrafo('Flujo detallado:')
    flujo_fase1 = [
        ("1", "CV llega por email/web/API"),
        ("2", "Agente Automatizacion detecta nuevo documento"),
        ("3", "Agente Documentos extrae texto (OCR si es imagen)"),
        ("4", "LLM (Ollama) parsea: nombre, email, experiencia, skills"),
        ("5", "Datos estructurados se guardan en PostgreSQL"),
        ("6", "Embedding del CV se guarda en ChromaDB"),
        ("7", "Candidato queda listo para la primera criba")
    ]
    pdf.tabla_simple(['Paso', 'Accion'], flujo_fase1, [20, 170])

    pdf.add_page()
    pdf.subtitulo('18.3 Fase 2: Primera Criba (Automatica)')
    pdf.parrafo('El sistema filtra automaticamente CVs que no cumplen requisitos minimos.')

    criterios_criba1 = [
        ("Experiencia minima", "3 anios en el sector", "Automatico", "Descarta < 3 anios"),
        ("Ubicacion", "Provincia de Malaga", "Automatico", "Descarta fuera de zona"),
        ("Idiomas", "Espanol nativo", "Automatico", "Verifica idioma CV"),
        ("Palabras clave", "Pescaderia, alimentacion", "Automatico", "Busqueda semantica"),
        ("Disponibilidad", "Inmediata/1 mes", "Semi-auto", "Si indica en CV")
    ]
    pdf.tabla_simple(['Criterio', 'Valor Requerido', 'Tipo', 'Accion'], criterios_criba1, [40, 45, 35, 70])

    pdf.parrafo('Stack tecnologico de esta fase:')
    stack_fase2 = [
        ("Frontend", "-", "Proceso automatico en background"),
        ("Backend", "FastAPI + Celery", "Jobs programados"),
        ("Agente", "Alertas + Asistente", "Evaluacion y clasificacion"),
        ("BD Lee", "PostgreSQL + ChromaDB", "Datos candidato + similitud"),
        ("BD Escribe", "PostgreSQL", "Estado: aprobado/descartado")
    ]
    pdf.tabla_simple(['Componente', 'Tecnologia', 'Funcion'], stack_fase2, [40, 60, 90])

    pdf.parrafo('Resultado de la primera criba:')
    resultado_criba1 = [
        ("Aprobado", "Verde", "Pasa a segunda criba"),
        ("Descartado", "Rojo", "Se archiva con motivo"),
        ("Revision", "Amarillo", "RRHH decide manualmente")
    ]
    pdf.tabla_simple(['Estado', 'Color', 'Siguiente Paso'], resultado_criba1, [50, 40, 100])

    pdf.add_page()
    pdf.subtitulo('18.4 Fase 3: Segunda Criba (RRHH)')
    pdf.parrafo('El responsable de RRHH revisa los candidatos preseleccionados con ayuda de IA.')

    pdf.parrafo('Stack tecnologico de esta fase:')
    stack_fase3 = [
        ("Frontend", "Vue.js (RRHH)", "Dashboard de candidatos"),
        ("Backend", "Laravel + FastAPI", "API + consultas IA"),
        ("Agente", "Asistente", "Responde preguntas sobre CVs"),
        ("BD Lee", "PostgreSQL + ChromaDB", "Datos + busqueda semantica"),
        ("BD Escribe", "PostgreSQL", "Notas y decisiones RRHH")
    ]
    pdf.tabla_simple(['Componente', 'Tecnologia', 'Funcion'], stack_fase3, [40, 60, 90])

    pdf.parrafo('Funciones del frontend RRHH en esta fase:')
    funciones_fase3 = [
        "Lista de candidatos aprobados en primera criba",
        "Vista detallada de cada CV con datos parseados",
        "Chat IA: 'Comparame estos 3 candidatos'",
        "Chat IA: 'Quien tiene mas experiencia en X?'",
        "Boton: Aprobar para llamada / Descartar",
        "Campo de notas internas por candidato"
    ]
    for f in funciones_fase3:
        pdf.item_lista(f)

    pdf.parrafo('Interaccion con Agente Asistente:')
    chat_ejemplos = [
        ("RRHH pregunta", "Quien tiene experiencia en pescaderia?"),
        ("Asistente", "Busca en ChromaDB por similitud semantica"),
        ("Asistente", "Responde: Juan (5 anios), Maria (3 anios)..."),
        ("RRHH pregunta", "Compara a Juan y Maria"),
        ("Asistente", "Genera tabla comparativa de skills y experiencia")
    ]
    pdf.tabla_simple(['Actor', 'Accion/Respuesta'], chat_ejemplos, [45, 145])

    pdf.add_page()
    pdf.subtitulo('18.5 Fase 4: Llamadas a Candidatos')
    pdf.parrafo('RRHH contacta a los candidatos seleccionados para agendar entrevistas.')

    pdf.parrafo('Stack tecnologico de esta fase:')
    stack_fase4 = [
        ("Frontend", "Vue.js (RRHH)", "Gestor de llamadas"),
        ("Backend", "Laravel", "CRUD de contactos"),
        ("Agente", "Alertas", "Seguimiento progreso X/Y"),
        ("BD Lee", "PostgreSQL", "Datos de contacto"),
        ("BD Escribe", "PostgreSQL", "Resultado llamada + cita")
    ]
    pdf.tabla_simple(['Componente', 'Tecnologia', 'Funcion'], stack_fase4, [40, 60, 90])

    pdf.parrafo('Flujo de trabajo con alertas de progreso:')
    flujo_llamadas = [
        ("1", "Gerencia/RRHH", "Selecciona 20 candidatos para llamar"),
        ("2", "Sistema", "Crea alerta de progreso: 0/20 llamadas"),
        ("3", "RRHH", "Ve alerta en su panel con lista de pendientes"),
        ("4", "RRHH", "Llama a candidato, registra resultado"),
        ("5", "Sistema", "Actualiza automaticamente: 1/20"),
        ("6", "RRHH", "Candidato confirma, agenda fecha entrevista"),
        ("7", "Sistema", "Guarda cita en calendario"),
        ("8", "Sistema", "20/20 completado, cierra alerta")
    ]
    pdf.tabla_simple(['Paso', 'Quien', 'Accion'], flujo_llamadas, [20, 40, 130])

    pdf.parrafo('Resultados posibles de cada llamada:')
    resultados_llamada = [
        ("Cita confirmada", "Se agenda entrevista", "Pasa a Fase 5"),
        ("No contesta", "Se reintenta 2 veces", "Queda pendiente"),
        ("Rechaza oferta", "Se descarta", "Se archiva"),
        ("Pide mas info", "Se envia email", "Queda pendiente")
    ]
    pdf.tabla_simple(['Resultado', 'Accion', 'Siguiente'], resultados_llamada, [45, 55, 90])

    pdf.add_page()
    pdf.subtitulo('18.6 Fase 5: Entrevistas')
    pdf.parrafo('Se realizan las entrevistas presenciales o por videollamada.')

    pdf.parrafo('Stack tecnologico de esta fase:')
    stack_fase5 = [
        ("Frontend", "Vue.js (RRHH)", "Agenda y evaluacion"),
        ("Backend", "Laravel", "Calendario + notas"),
        ("Agente", "-", "Sin IA en entrevista"),
        ("BD Lee", "PostgreSQL", "Historial candidato"),
        ("BD Escribe", "PostgreSQL", "Evaluacion entrevista")
    ]
    pdf.tabla_simple(['Componente', 'Tecnologia', 'Funcion'], stack_fase5, [40, 60, 90])

    pdf.parrafo('Funciones del frontend RRHH en esta fase:')
    funciones_fase5 = [
        "Calendario con citas programadas",
        "Ficha del candidato con todo su historial",
        "Formulario de evaluacion post-entrevista",
        "Puntuacion por competencias (1-5)",
        "Decision: Contratar / Segunda entrevista / Descartar",
        "Generacion de oferta laboral (si aplica)"
    ]
    for f in funciones_fase5:
        pdf.item_lista(f)

    pdf.parrafo('Estados post-entrevista:')
    estados_entrevista = [
        ("Contratado", "Pasa a onboarding", "Proceso finalizado"),
        ("Segunda entrevista", "Se agenda nueva cita", "Vuelve a Fase 5"),
        ("En espera", "Pool de reserva", "Posible reactivacion"),
        ("Descartado", "No apto para el puesto", "Se archiva")
    ]
    pdf.tabla_simple(['Estado', 'Accion', 'Nota'], estados_entrevista, [50, 60, 80])

    pdf.add_page()
    pdf.subtitulo('18.7 Fase 6: Reactivacion de Candidatos')
    pdf.parrafo('El sistema puede reactivar automaticamente candidatos del pool de reserva.')

    pdf.parrafo('Stack tecnologico de esta fase:')
    stack_fase6 = [
        ("Frontend", "-", "Proceso automatico"),
        ("Backend", "FastAPI + Celery", "Jobs programados"),
        ("Agente", "Alertas", "Detecta vacantes + matching"),
        ("BD Lee", "PostgreSQL + ChromaDB", "Pool + similitud"),
        ("BD Escribe", "PostgreSQL", "Reactivacion candidato")
    ]
    pdf.tabla_simple(['Componente', 'Tecnologia', 'Funcion'], stack_fase6, [40, 60, 90])

    pdf.parrafo('Triggers de reactivacion:')
    triggers_react = [
        ("Nueva vacante", "Se abre puesto similar", "Busca en pool"),
        ("Tiempo transcurrido", "Candidato en espera > 3 meses", "Pregunta si sigue interesado"),
        ("Cambio requisitos", "Se flexibilizan criterios", "Reevalua descartados"),
        ("Solicitud RRHH", "Manual desde dashboard", "Recupera candidato especifico")
    ]
    pdf.tabla_simple(['Trigger', 'Condicion', 'Accion'], triggers_react, [50, 60, 80])

    pdf.parrafo('Flujo de reactivacion automatica:')
    flujo_react = [
        ("1", "Agente Alertas", "Detecta nueva vacante en el sistema"),
        ("2", "Agente Alertas", "Busca candidatos en pool con skills similares"),
        ("3", "ChromaDB", "Devuelve top 10 por similitud semantica"),
        ("4", "Agente Alertas", "Crea alerta para RRHH: 10 candidatos potenciales"),
        ("5", "RRHH", "Revisa lista y decide quien recontactar"),
        ("6", "Sistema", "Candidatos seleccionados vuelven a Fase 4")
    ]
    pdf.tabla_simple(['Paso', 'Componente', 'Accion'], flujo_react, [20, 45, 125])

    pdf.add_page()
    pdf.subtitulo('18.8 Integracion MySQL (ERP) y PostgreSQL (IA)')

    pdf.parrafo('El flujo RRHH conecta datos existentes del ERP (MySQL) con el nuevo sistema de seleccion (PostgreSQL):')

    datos_mysql = [
        ("trabajadores", "Empleados actuales", "Verificar si candidato ya trabaja"),
        ("trabajadores_antiguos", "Ex-empleados", "Verificar si candidato ya trabajo antes"),
        ("registro_horario", "Fichajes", "Consultar horarios al contratar"),
        ("nominas", "Datos salariales", "Preparar oferta economica"),
        ("vacantes", "Puestos abiertos", "Disparar busqueda de candidatos"),
        ("departamentos", "Estructura empresa", "Asignar departamento al contratar")
    ]
    pdf.tabla_simple(['Tabla MySQL', 'Contenido', 'Uso en RRHH'], datos_mysql, [50, 50, 90])

    pdf.parrafo('Datos nuevos en PostgreSQL (sistema de seleccion):')
    datos_pg = [
        ("candidatos", "Datos parseados del CV", "Nombre, email, skills, experiencia"),
        ("cvs_documentos", "PDF original + embeddings", "Busqueda semantica"),
        ("proceso_seleccion", "Estado de cada candidato", "Fase actual, fechas, notas"),
        ("llamadas", "Registro de contactos", "Resultado, fecha cita"),
        ("entrevistas", "Evaluaciones", "Puntuacion, decision"),
        ("alertas_rrhh", "Notificaciones", "Progreso, tareas pendientes")
    ]
    pdf.tabla_simple(['Tabla PostgreSQL', 'Contenido', 'Detalle'], datos_pg, [50, 55, 85])

    pdf.add_page()
    pdf.parrafo('Momentos de integracion MySQL <-> PostgreSQL:')
    integracion = [
        ("Entrada CV", "Lee MySQL", "Verifica si email ya es empleado/ex-empleado"),
        ("Primera Criba", "Lee MySQL", "Descarta si ya trabajo y salio mal"),
        ("Segunda Criba", "Lee MySQL", "Muestra historial si fue empleado antes"),
        ("Entrevista OK", "Lee MySQL", "Consulta salarios del puesto para oferta"),
        ("Contratacion", "Escribe MySQL", "INSERT en trabajadores + nominas"),
        ("Nueva vacante", "Lee MySQL", "Trigger desde tabla vacantes del ERP")
    ]
    pdf.tabla_simple(['Momento', 'Accion', 'Detalle'], integracion, [40, 40, 110])

    pdf.subtitulo('18.9 Resumen: Stack Completo por Fase')

    pdf.parrafo('Tabla resumen incluyendo ambas bases de datos:')

    resumen_rrhh = [
        ("1. Entrada CVs", "-", "Laravel+FastAPI", "Docs+Auto", "MySQL+PG", "PG"),
        ("2. Primera Criba", "-", "FastAPI+Celery", "Alertas+Asist", "MySQL+PG", "PG"),
        ("3. Segunda Criba", "Vue RRHH", "Laravel+FastAPI", "Asistente", "MySQL+PG", "PG"),
        ("4. Llamadas", "Vue RRHH", "Laravel", "Alertas", "PG", "PG"),
        ("5. Entrevistas", "Vue RRHH", "Laravel", "-", "MySQL+PG", "PG+MySQL"),
        ("6. Reactivacion", "-", "FastAPI+Celery", "Alertas", "MySQL+PG", "PG")
    ]
    pdf.tabla_simple(['Fase', 'Frontend', 'Backend', 'Agentes', 'BD Lee', 'BD Escr'], resumen_rrhh, [35, 28, 40, 37, 32, 28])

    pdf.parrafo('Leyenda:')
    leyenda = [
        "MySQL = Base de datos ERP (trabajadores, nominas, vacantes)",
        "PG = PostgreSQL (candidatos, proceso seleccion, alertas)",
        "Chroma = ChromaDB (embeddings de CVs)",
        "Docs = Agente Documentos",
        "Auto = Agente Automatizacion",
        "Asist = Agente Asistente"
    ]
    for l in leyenda:
        pdf.item_lista(l)

    pdf.parrafo('Flujo de sincronizacion al CONTRATAR:')
    sync_contratar = [
        ("1", "RRHH marca 'Contratar' en frontend", "PostgreSQL", "estado = contratado"),
        ("2", "Laravel detecta cambio de estado", "-", "Evento ContratacionAprobada"),
        ("3", "Listener crea registro empleado", "MySQL", "INSERT trabajadores"),
        ("4", "Listener crea registro nomina", "MySQL", "INSERT nominas"),
        ("5", "Sistema notifica a Gerencia", "Redis", "Push de confirmacion")
    ]
    pdf.tabla_simple(['Paso', 'Accion', 'BD', 'Detalle'], sync_contratar, [20, 70, 35, 65])

    pdf.subtitulo('18.10 Metricas y KPIs del Proceso')

    pdf.parrafo('El sistema puede calcular automaticamente estos KPIs de RRHH:')
    kpis_rrhh = [
        ("CVs recibidos/mes", "COUNT candidatos por mes", "PostgreSQL"),
        ("Tasa primera criba", "% aprobados vs total", "PostgreSQL"),
        ("Tasa segunda criba", "% aprobados vs primera criba", "PostgreSQL"),
        ("Tasa contacto", "% llamadas exitosas", "PostgreSQL"),
        ("Tasa entrevista", "% citas confirmadas", "PostgreSQL"),
        ("Tasa contratacion", "% contratados vs entrevistados", "PostgreSQL"),
        ("Tiempo medio proceso", "Dias desde CV hasta contrato", "PostgreSQL"),
        ("Coste por contratacion", "Recursos usados / contratados", "PostgreSQL")
    ]
    pdf.tabla_simple(['KPI', 'Calculo', 'Fuente'], kpis_rrhh, [50, 80, 60])

    pdf.add_page()
    pdf.subtitulo('18.11 Pantallas del Frontend RRHH por Fase')

    pdf.parrafo('Detalle de las vistas y pantallas especificas del frontend Vue.js RRHH:')

    pantallas_rrhh = [
        ("Fase 1", "-", "Sin frontend (automatico)"),
        ("Fase 2", "-", "Sin frontend (automatico)"),
        ("Fase 3", "/rrhh/candidatos", "Lista candidatos preseleccionados"),
        ("Fase 3", "/rrhh/candidatos/:id", "Ficha completa del candidato"),
        ("Fase 3", "/rrhh/comparar", "Comparador de candidatos"),
        ("Fase 4", "/rrhh/llamadas", "Gestor de llamadas pendientes"),
        ("Fase 4", "/rrhh/llamadas/:id", "Registro de llamada"),
        ("Fase 5", "/rrhh/entrevistas", "Calendario de entrevistas"),
        ("Fase 5", "/rrhh/entrevistas/:id", "Evaluacion post-entrevista"),
        ("Fase 6", "/rrhh/pool", "Pool de candidatos en reserva")
    ]
    pdf.tabla_simple(['Fase', 'Ruta', 'Pantalla'], pantallas_rrhh, [25, 60, 105])

    pdf.subtitulo('18.12 Detalle de Cada Pantalla')

    pdf.parrafo('PANTALLA: /rrhh/candidatos (Lista de Candidatos)')
    pantalla_lista = [
        ("Tabla", "Lista de candidatos con filtros", "Nombre, email, estado, fecha"),
        ("Filtros", "Por estado, fecha, skills", "Dropdown + busqueda"),
        ("Acciones", "Ver ficha, aprobar, descartar", "Botones por fila"),
        ("Widget", "Chat IA flotante", "Preguntas sobre candidatos"),
        ("Widget", "Campanita alertas", "Nuevos CVs, tareas pendientes")
    ]
    pdf.tabla_simple(['Elemento', 'Descripcion', 'Detalle'], pantalla_lista, [35, 65, 90])

    pdf.parrafo('PANTALLA: /rrhh/candidatos/:id (Ficha del Candidato)')
    pantalla_ficha = [
        ("Cabecera", "Foto + datos basicos", "Nombre, email, telefono, ubicacion"),
        ("Seccion CV", "Datos extraidos por IA", "Experiencia, formacion, skills"),
        ("Seccion Doc", "PDF original del CV", "Visor embebido"),
        ("Seccion Notas", "Notas internas RRHH", "Editor de texto"),
        ("Seccion Hist", "Historial de acciones", "Timeline de estados"),
        ("Botones", "Aprobar / Descartar / Llamar", "Acciones principales"),
        ("Chat IA", "Preguntas sobre este CV", "'Resume este CV', 'Skills clave?'")
    ]
    pdf.tabla_simple(['Elemento', 'Descripcion', 'Detalle'], pantalla_ficha, [35, 60, 95])

    pdf.add_page()
    pdf.parrafo('PANTALLA: /rrhh/llamadas (Gestor de Llamadas)')
    pantalla_llamadas = [
        ("Alerta", "Progreso X/Y", "Barra: 5/20 llamadas completadas"),
        ("Lista", "Candidatos a llamar", "Ordenados por prioridad"),
        ("Por fila", "Nombre + telefono + boton", "Click para registrar llamada"),
        ("Modal", "Registrar resultado", "Contesta/No contesta/Rechaza"),
        ("Modal", "Agendar cita", "Selector de fecha y hora"),
        ("Resumen", "Estadisticas del dia", "Llamadas hechas, citas, rechazos")
    ]
    pdf.tabla_simple(['Elemento', 'Descripcion', 'Detalle'], pantalla_llamadas, [35, 55, 100])

    pdf.parrafo('PANTALLA: /rrhh/entrevistas (Calendario)')
    pantalla_calendario = [
        ("Vista", "Calendario mensual/semanal", "Citas programadas"),
        ("Evento", "Click en cita", "Abre ficha del candidato"),
        ("Color", "Por estado", "Pendiente/Realizada/Cancelada"),
        ("Accion", "Arrastrar para mover", "Reagendar entrevista"),
        ("Panel", "Entrevistas de hoy", "Lista lateral con accesos rapidos")
    ]
    pdf.tabla_simple(['Elemento', 'Descripcion', 'Detalle'], pantalla_calendario, [35, 55, 100])

    pdf.parrafo('PANTALLA: /rrhh/entrevistas/:id (Evaluacion)')
    pantalla_eval = [
        ("Cabecera", "Datos del candidato", "Nombre + puesto solicitado"),
        ("Formulario", "Puntuacion competencias", "1-5 estrellas por area"),
        ("Areas", "Tecnica, comunicacion, actitud", "Sliders o estrellas"),
        ("Textarea", "Observaciones", "Notas de la entrevista"),
        ("Decision", "Contratar/2a entrev/Pool/Descartar", "Radio buttons"),
        ("Boton", "Guardar evaluacion", "Guarda y notifica")
    ]
    pdf.tabla_simple(['Elemento', 'Descripcion', 'Detalle'], pantalla_eval, [35, 55, 100])

    pdf.parrafo('PANTALLA: /rrhh/pool (Candidatos en Reserva)')
    pantalla_pool = [
        ("Tabla", "Candidatos en espera", "Nombre, fecha, motivo, skills"),
        ("Filtros", "Por skills, fecha, puntuacion", "Busqueda avanzada"),
        ("Accion", "Reactivar candidato", "Vuelve al proceso activo"),
        ("Alerta IA", "Sugerencias automaticas", "'3 candidatos coinciden con vacante X'"),
        ("Busqueda", "Semantica por skills", "'Buscar expertos en logistica'")
    ]
    pdf.tabla_simple(['Elemento', 'Descripcion', 'Detalle'], pantalla_pool, [35, 55, 100])

    pdf.add_page()
    pdf.subtitulo('18.13 Widgets Comunes en Todas las Pantallas RRHH')

    pdf.parrafo('Todos los frontends RRHH incluyen estos widgets:')
    widgets_rrhh = [
        ("Campanita", "Esquina superior derecha", "Alertas y notificaciones"),
        ("Chat IA", "Flotante inferior derecha", "Asistente conversacional"),
        ("Breadcrumb", "Cabecera", "Navegacion: RRHH > Candidatos > Juan"),
        ("Usuario", "Esquina superior derecha", "Nombre + rol + logout"),
        ("Menu lateral", "Izquierda", "Navegacion entre pantallas")
    ]
    pdf.tabla_simple(['Widget', 'Posicion', 'Funcion'], widgets_rrhh, [40, 60, 90])

    pdf.parrafo('Estructura del menu lateral RRHH:')
    menu_rrhh = [
        ("Dashboard", "/rrhh", "Resumen y KPIs"),
        ("Candidatos", "/rrhh/candidatos", "Gestion de CVs"),
        ("Llamadas", "/rrhh/llamadas", "Gestor de contactos"),
        ("Entrevistas", "/rrhh/entrevistas", "Calendario y evaluaciones"),
        ("Pool", "/rrhh/pool", "Candidatos en reserva"),
        ("Vacantes", "/rrhh/vacantes", "Puestos abiertos"),
        ("Reportes", "/rrhh/reportes", "Estadisticas y KPIs"),
        ("Configuracion", "/rrhh/config", "Criterios de criba, plantillas")
    ]
    pdf.tabla_simple(['Menu', 'Ruta', 'Descripcion'], menu_rrhh, [40, 55, 95])

    pdf.add_page()
    pdf.subtitulo('18.14 Actividades por Trabajador en el Flujo RRHH')

    pdf.parrafo('Detalle de cada actividad, quien la realiza y que componentes utiliza:')

    pdf.parrafo('FASE 1: ENTRADA DE CVs')
    fase1_actividades = [
        ("Candidato", "Envia CV por email/web", "-", "Laravel", "-", "-"),
        ("Sistema", "Verifica si ya es empleado", "-", "FastAPI", "MySQL", "Auto"),
        ("Sistema", "Extrae texto del PDF", "-", "FastAPI", "-", "Docs"),
        ("Sistema", "Parsea datos con LLM", "-", "FastAPI+Ollama", "-", "Docs"),
        ("Sistema", "Guarda candidato", "-", "FastAPI", "PG", "Docs"),
        ("Sistema", "Guarda embeddings CV", "-", "FastAPI", "Chroma", "Docs")
    ]
    pdf.tabla_simple(['Quien', 'Actividad', 'Frontend', 'Backend', 'BD', 'Agente'], fase1_actividades, [28, 48, 25, 38, 25, 22])

    pdf.parrafo('FASE 2: PRIMERA CRIBA (AUTOMATICA)')
    fase2_actividades = [
        ("Sistema", "Ejecuta job de criba", "-", "Celery", "-", "Alertas"),
        ("Sistema", "Consulta historial empleado", "-", "FastAPI", "MySQL", "Asist"),
        ("Sistema", "Evalua criterios minimos", "-", "FastAPI", "PG", "Asist"),
        ("Sistema", "Clasifica candidato", "-", "FastAPI", "PG", "Asist"),
        ("Sistema", "Notifica a RRHH", "-", "Laravel Echo", "Redis", "Alertas")
    ]
    pdf.tabla_simple(['Quien', 'Actividad', 'Frontend', 'Backend', 'BD', 'Agente'], fase2_actividades, [28, 48, 25, 38, 25, 22])

    pdf.parrafo('FASE 3: SEGUNDA CRIBA (MANUAL)')
    fase3_actividades = [
        ("RRHH", "Abre lista candidatos", "Vue /candidatos", "Laravel", "PG", "-"),
        ("RRHH", "Ve ficha candidato", "Vue /candidatos/:id", "Laravel", "PG", "-"),
        ("RRHH", "Ve si fue empleado antes", "Vue /candidatos/:id", "Laravel", "MySQL", "-"),
        ("RRHH", "Pregunta al chat IA", "Vue (widget)", "FastAPI", "PG+Chroma", "Asist"),
        ("RRHH", "Compara candidatos", "Vue /comparar", "FastAPI", "PG+Chroma", "Asist"),
        ("RRHH", "Aprueba o descarta", "Vue /candidatos/:id", "Laravel", "PG", "-"),
        ("RRHH", "Escribe notas", "Vue /candidatos/:id", "Laravel", "PG", "-")
    ]
    pdf.tabla_simple(['Quien', 'Actividad', 'Frontend', 'Backend', 'BD', 'Agente'], fase3_actividades, [22, 42, 40, 30, 32, 20])

    pdf.add_page()
    pdf.parrafo('FASE 4: LLAMADAS A CANDIDATOS')
    fase4_actividades = [
        ("Gerencia", "Selecciona candidatos", "Vue /candidatos", "Laravel", "PG", "-"),
        ("Gerencia", "Asigna tarea a RRHH", "Vue /candidatos", "Laravel", "PG", "Alertas"),
        ("Sistema", "Crea alerta 0/X", "-", "Laravel", "PG+Redis", "Alertas"),
        ("RRHH", "Ve alerta en panel", "Vue (campanita)", "Echo", "Redis", "Alertas"),
        ("RRHH", "Abre gestor llamadas", "Vue /llamadas", "Laravel", "PG", "-"),
        ("RRHH", "Llama al candidato", "Vue /llamadas/:id", "-", "-", "-"),
        ("RRHH", "Registra resultado", "Vue /llamadas/:id", "Laravel", "PG", "-"),
        ("RRHH", "Agenda cita", "Vue /llamadas/:id", "Laravel", "PG", "-"),
        ("Sistema", "Actualiza X/Y", "-", "Laravel", "PG", "Alertas"),
        ("Sistema", "Cierra alerta", "-", "Laravel", "PG", "Alertas")
    ]
    pdf.tabla_simple(['Quien', 'Actividad', 'Frontend', 'Backend', 'BD', 'Agente'], fase4_actividades, [25, 42, 38, 28, 30, 23])

    pdf.parrafo('FASE 5: ENTREVISTAS Y CONTRATACION')
    fase5_actividades = [
        ("RRHH", "Consulta calendario", "Vue /entrevistas", "Laravel", "PG", "-"),
        ("RRHH", "Ve citas del dia", "Vue /entrevistas", "Laravel", "PG", "-"),
        ("RRHH", "Realiza entrevista", "-", "-", "-", "-"),
        ("RRHH", "Evalua competencias", "Vue /entrev/:id", "Laravel", "PG", "-"),
        ("RRHH", "Escribe observaciones", "Vue /entrev/:id", "Laravel", "PG", "-"),
        ("RRHH", "Consulta salario puesto", "Vue /entrev/:id", "Laravel", "MySQL", "-"),
        ("RRHH", "Decide contratar", "Vue /entrev/:id", "Laravel", "PG", "-"),
        ("Sistema", "Crea empleado en ERP", "-", "Laravel", "MySQL", "Auto"),
        ("Sistema", "Crea registro nomina", "-", "Laravel", "MySQL", "Auto"),
        ("Sistema", "Notifica a gerencia", "-", "Echo", "Redis", "Alertas")
    ]
    pdf.tabla_simple(['Quien', 'Actividad', 'Frontend', 'Backend', 'BD', 'Agente'], fase5_actividades, [25, 42, 35, 28, 28, 22])

    pdf.add_page()
    pdf.parrafo('FASE 6: REACTIVACION DE CANDIDATOS')
    fase6_actividades = [
        ("Sistema", "Detecta nueva vacante", "-", "Celery", "MySQL", "Alertas"),
        ("Sistema", "Busca en pool por skills", "-", "FastAPI", "Chroma", "Docs"),
        ("Sistema", "Filtra por historial", "-", "FastAPI", "MySQL", "Asist"),
        ("Sistema", "Crea alerta sugerencias", "-", "Laravel", "PG", "Alertas"),
        ("RRHH", "Ve alerta reactivacion", "Vue (campanita)", "Echo", "Redis", "Alertas"),
        ("RRHH", "Abre pool candidatos", "Vue /pool", "Laravel", "PG", "-"),
        ("RRHH", "Revisa sugeridos", "Vue /pool", "FastAPI", "PG+Chroma", "Asist"),
        ("RRHH", "Reactiva candidato", "Vue /pool", "Laravel", "PG", "-"),
        ("Sistema", "Mueve a Fase 4", "-", "Laravel", "PG", "-")
    ]
    pdf.tabla_simple(['Quien', 'Actividad', 'Frontend', 'Backend', 'BD', 'Agente'], fase6_actividades, [25, 42, 38, 28, 33, 22])

    pdf.subtitulo('18.15 Resumen de Actividades por Rol')

    pdf.parrafo('Cuantas actividades realiza cada trabajador en el proceso completo:')
    resumen_roles = [
        ("Sistema/Agentes", "23", "Automaticas", "Deteccion, criba, alertas, sync"),
        ("RRHH", "22", "Manuales", "Revision, llamadas, entrevistas, pool"),
        ("Gerencia", "2", "Supervision", "Asignar tareas, recibir notificaciones"),
        ("Candidato", "1", "Externa", "Enviar CV")
    ]
    pdf.tabla_simple(['Rol', 'Actividades', 'Tipo', 'Principales Tareas'], resumen_roles, [40, 30, 35, 85])

    pdf.parrafo('Distribucion de trabajo humano vs automatico:')
    distribucion = [
        ("Fase 1", "0%", "100%", "Totalmente automatizada"),
        ("Fase 2", "0%", "100%", "Totalmente automatizada"),
        ("Fase 3", "100%", "0%", "RRHH revisa con ayuda IA"),
        ("Fase 4", "80%", "20%", "RRHH llama, sistema trackea"),
        ("Fase 5", "100%", "0%", "RRHH entrevista y evalua"),
        ("Fase 6", "30%", "70%", "Sistema sugiere, RRHH decide")
    ]
    pdf.tabla_simple(['Fase', 'Humano', 'Automatico', 'Descripcion'], distribucion, [30, 30, 35, 95])

    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.set_x(10)
    pdf.multi_cell(0, 6, 'Este documento sirve como guia de referencia para el diseno e implementacion '
                         'del sistema multi-agente. Se recomienda adaptar la arquitectura segun las '
                         'necesidades especificas del negocio y los recursos disponibles.')

    # Guardar PDF
    output_path = r'C:\Users\usuario\Proyecto_IA_MultiAgente_v6.pdf'
    pdf.output(output_path)
    return output_path

if __name__ == '__main__':
    path = crear_pdf()
    print(f'PDF generado exitosamente en: {path}')
