# Registro de cambios

🇩🇪 [Deutsch](CHANGELOG.md) · 🇬🇧 [English](CHANGELOG.en.md) · 🇫🇷 [Français](CHANGELOG.fr.md) · 🇮🇹 [Italiano](CHANGELOG.it.md) · 🇵🇱 [Polski](CHANGELOG.pl.md) · 🇨🇳 [简体中文](CHANGELOG.zh.md)

Todos los cambios importantes de SC Playtime. Formato basado en
[Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.5.0] – 2026-10-09

### Novedades
- **Cierres inesperados y desconexiones del servidor por parche:** al cerrarse el juego, SC
  Playtime lee el `Game.log` de Star Citizen y recuerda si lo cerraste tú, si el juego se
  cerró de forma inesperada o si el servidor cortó la conexión. El análisis muestra por
  parche los cierres inesperados (p. ej. «2 · cada 6h 30m») y las desconexiones, la ventana
  de sesiones una columna «Resultado». Las sesiones anteriores se clasifican al iniciar a
  partir de los registros guardados (`logbackups`).
- **Cronología del día** en el análisis: un día como línea de tiempo de 0 a 24 h con todas
  las sesiones en el color de su canal, las pausas como huecos, cierre inesperado (rojo) y
  desconexión (amarillo) como marcas; con ‹ › se pasa de un día jugado a otro.
- **Unir dos PC:** Menú → Datos → «Importar sesiones de otro PC …» añade el tiempo de juego
  del `playtime.db` (o de una copia) de otro PC. Las sesiones que ya están se reconocen y
  se omiten; antes se hace una copia de los datos actuales.
- **Desde cuándo se cuenta:** la casilla TOTAL muestra arriba a la derecha la fecha del
  primer registro.
- **Ayuda y registro de cambios en los siete idiomas** (antes solo alemán e inglés).

### Cambios
- La exportación CSV/JSON incluye una columna `ending` (`quit`, `crash`, `server`).

## [1.4.1] – 2026-10-09

### Mejoras
- **Overlay más rápido con un historial largo:** las estadísticas se recalculaban por
  completo cada segundo, y el trabajo crecía al cuadrado con el número de sesiones (1,5 s
  con 5000 sesiones – cada segundo, encima del juego). Ahora las sesiones terminadas se
  evalúan una sola vez y cada segundo solo se añade la sesión en curso: 2 ms en lugar de
  1500 ms.
- El punto que late redibuja el overlay 8 veces por segundo en lugar de 16.

### Seguridad
- Las actualizaciones solo se instalan si el archivo descargado coincide con la suma de
  comprobación que GitHub indica para la versión.
- La configuración se escribe primero completa en un archivo temporal y luego se sustituye
  – un cierre inesperado al guardar ya no la restablece.

## [1.4.0] – 2026-10-04

### Novedades
- **Retroceder en el gráfico:** en DÍA, SEMANA y MES las flechas ‹ › arriba a la derecha
  del gráfico retroceden hacia el pasado, la rueda del ratón paso a paso – hasta la
  primera sesión.
- **Análisis** (Menú → Análisis …): mapa de calor «¿Cuándo juegas?» por día y hora, además
  del **tiempo de juego por parche**. La versión de Star Citizen (p. ej. 4.3.1) se lee
  ahora de la carpeta de instalación y se guarda con cada sesión.
- **Editar sesiones** (Menú → Editar sesiones …): corregir inicio y fin o eliminar
  sesiones, p. ej. tras un reposo con el juego abierto.
- **Detección AFK** (Menú → Detección AFK): pausa opcional tras 5–30 minutos sin
  actividad; la sesión termina en la última pulsación y empieza una nueva con la siguiente
  actividad. El overlay muestra entonces «AFK».
- **Atajos globales** (Windows): Ctrl+Mayús+F9 muestra/oculta el overlay, Ctrl+Mayús+F11
  activa/desactiva «Dejar pasar los clics» – también en el juego. Se cambian en Menú →
  Atajos de teclado ….
- **Exportación** de todas las sesiones como CSV (para Excel) o JSON (Menú → Datos).
- **Copia automática:** una copia de la base de datos al día en `backups`, se conservan
  las 7 últimas; además «Hacer copia ahora» en el menú.
- **Nuevos idiomas:** Français, Español, Italiano, Polski y 简体中文 (ayuda y registro de
  cambios entonces en inglés).
- **Acerca de SC Playtime** en el menú, con versión, enlaces y botón de donación (PayPal).

### Correcciones
- El menú contextual (y el selector de color o los mensajes) desaparecía a menudo detrás
  del overlay o del juego. Ahora los menús y diálogos quedan siempre delante, y el overlay
  ya no se pone delante mientras uno está abierto.

## [1.3.2] – 2026-09-29

### Correcciones
- **Gráfico con filtro de canal:** con p. ej. PTU elegido, el gráfico se veía igual que
  con TODOS, porque siempre se ajustaba a su barra más alta – 6 minutos de PTU llenaban la
  altura igual que 11 horas en total. Ahora la escala sigue siendo la de TODOS, el total se
  muestra en gris detrás y el canal elegido se dibuja en su color delante. Al pasar el
  ratón se muestra «PTU 6m / 11h 31m».

## [1.3.1] – 2026-09-29

### Novedades
- **Prueba de origen:** cada archivo publicado se puede verificar con una atestación de
  GitHub (`gh attestation verify …`). La firma de Windows mediante SignPath Foundation
  está solicitada y preparada en la compilación.
- Licencia: MIT.
- Ayuda: apartado sobre el aviso de SmartScreen.

## [1.3.0] – 2026-09-29

### Novedades
- **Idioma inglés:** Menú → Idioma con banderas (🇩🇪 Deutsch, 🇬🇧 English) o «Automático»
  según el idioma del sistema. Overlay, menú, mensajes, ayuda y registro de cambios están
  totalmente traducidos; se pueden añadir más idiomas fácilmente.
- **Soporte para Linux:** detección de procesos mediante `/proc` (incluido Star Citizen
  con Wine/Proton/Lutris con canal), inicio automático mediante `~/.config/autostart`,
  datos en `~/.local/share/SC-Playtime`, inicio automático mediante XWayland. Programa
  listo `SC-Playtime-linux-x86_64` en la versión, actualización automática también en
  Linux.
- Compilaciones y pruebas automáticas para Windows y Linux con GitHub Actions.

### Correcciones
- Los mensajes (p. ej. «Sin actualización») mostraban texto oscuro sobre fondo oscuro y
  parecían vacíos.

## [1.2.0] – 2026-09-29

### Novedades
- **Función de actualización:** al iniciar y cada 12 horas comprueba en GitHub si hay una
  versión nueva. Si la hay, aparece un aviso en el icono de la bandeja y «Instalar la
  actualización» arriba del menú. El EXE descarga la versión nueva, se sustituye y se
  reinicia – antes se guarda la sesión en curso.
- Menú: **Buscar actualizaciones** y **Buscar actualizaciones automáticamente** (se puede
  desactivar).
- Menú: **Ayuda** y **Novedades** abren la ayuda y el registro de cambios directamente en
  el programa, también sin conexión.
- Tras una actualización, «Novedades» se muestra automáticamente una vez.
- Número de versión en el título del menú y en las ventanas.

## [1.1.0] – 2026-09-29

### Novedades
- **Colores ajustables** (Menú → Colores):
  - *Casillas de estadísticas (en juego)*: plantillas Verde, Cian, Ámbar o «Sin color»,
    además de libre elección de color de fondo y de texto.
  - *Canal activo*: plantillas para el chip de canal seleccionado y libre elección de
    color.
- Las casillas de estadísticas se colorean mientras el juego está abierto (por defecto:
  verde con texto oscuro). Sin juego siguen oscuras con estilo HUD.
- Ayuda (`HILFE.md`) con todas las funciones.

### Correcciones
- Durante el juego, las casillas y los chips de canal se rellenaban por error de verde
  claro y el texto blanco apenas se leía. La causa era el color de relleno del punto de
  estado, que seguía activo después.

## [1.0.0] – 2026-09-28

Primera versión.

### Novedades
- Overlay sin bordes con estilo HUD de Star Citizen, siempre delante.
- Detección automática de `StarCitizen.exe` (lista de procesos, cada 2 s, solo lectura).
- Detección del canal desde la carpeta de instalación: LIVE, PTU, EPTU, HOTFIX,
  TECH-PREVIEW; estadísticas por canal o todas juntas.
- Varios juegos: añadir y quitar cualquier EXE.
- Vista compacta: reloj de sesión, hoy, semana.
- Estadísticas desplegadas: casillas (hoy, semana, mes, año, total, racha), gráfico de
  barras día / semana / mes / año / total con valores al pasar el ratón, sesiones, media y
  sesión más larga.
- Transparencia del fondo y transparencia total ajustables por separado.
- Bloquear posición, dejar pasar los clics, mostrar solo mientras un juego está abierto.
- Icono en la bandeja, una sola instancia, inicio con Windows (sin administrador).
- Almacenamiento en SQLite en `%APPDATA%\SC-Playtime\`; fin de sesión guardado cada 30 s.
- Compilación en un solo EXE con PyInstaller (`build.py`).
