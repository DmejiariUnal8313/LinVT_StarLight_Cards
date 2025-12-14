# LinVT StarLight Cards

Pequeño proyecto de cartas con Pygame. Contiene la lógica del juego, recursos de cartas y utilidades para desarrollo.

## Estructura relevante
- `src/main.py`: entrypoint (lanza `GameApp`).
- `src/game_app.py`: clase `GameApp` (bucle principal, UI, eventos).
- `src/card.py`: definición de cartas y `cards_info`.
- `src/utils.py`: utilidades (carga de imágenes con manejo de errores).
- `src/check_images_exist.py`: test rápido que verifica que los ficheros de imagen existen.
- `src/check_resources.py`: test que verifica imágenes usando Pygame (requiere `pygame`).
- `requirements.txt`: dependencias del proyecto.

## Requisitos
- Python 3.8+ (se recomienda usar el entorno virtual del proyecto).

## Instalación rápida (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Nota: la instalación de `pygame` puede requerir herramientas de compilación en Windows. Si `pip install -r requirements.txt` falla, instala una rueda precompilada apropiada o consulta la documentación de Pygame.

## Ejecutar el juego
```powershell
python src\main.py
```

## Tests y comprobaciones de recursos
- Comprobar que las rutas de imagen listadas en `cards_info` existen (no requiere Pygame):
```powershell
python src\check_images_exist.py
```
- Comprobar que las imágenes funcionan con Pygame (prueba headless con driver `dummy`):
```powershell
# En PowerShell
$env:SDL_VIDEODRIVER='dummy'
python src\check_resources.py
```

## Notas de diseño y próximos pasos
- `main.py` ahora es un entrypoint que crea `GameApp` en `src/game_app.py`.
- Se corrigió el reparto de mazos para evitar asignar la misma lista a ambos jugadores y se añadió cacheado básico de imágenes escaladas.
- `load_image` en `src/utils.py` ahora maneja errores y devuelve un placeholder si la carga falla.

Si quieres, puedo:
- Añadir tests con `pytest`.
- Crear un pequeño CI que ejecute `check_images_exist.py`.
- Completar la refactorización para extraer más módulos (UI, recursos, lógica del juego).

---
Creado automáticamente por el asistente de refactorización.
