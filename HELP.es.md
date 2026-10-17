# SC Playtime – Ayuda

🇩🇪 [Deutsch](HILFE.md) · 🇬🇧 [English](HELP.md) · 🇫🇷 [Français](HELP.fr.md) · 🇮🇹 [Italiano](HELP.it.md) · 🇵🇱 [Polski](HELP.pl.md) · 🇨🇳 [简体中文](HELP.zh.md)

SC Playtime es un pequeño overlay que cuenta cuánto tiempo juegas a Star Citizen (u otros
juegos). Se coloca como un panel estrecho sobre el juego y muestra la sesión en curso y
tus estadísticas. Funciona en **Windows** y **Linux**.

- [Instalación e inicio](#instalación-e-inicio)
- [El overlay](#el-overlay)
- [Uso con el ratón](#uso-con-el-ratón)
- [El menú](#el-menú)
- [Colores](#colores)
- [Idioma](#idioma)
- [Varios juegos](#varios-juegos)
- [Canales (LIVE, PTU, …)](#canales-live-ptu-)
- [Análisis (mapa de calor, cronología del día, parches)](#análisis-mapa-de-calor-cronología-del-día-parches)
- [Editar sesiones](#editar-sesiones)
- [Detección AFK](#detección-afk)
- [Anti-AFK](#anti-afk)
- [Atajos de teclado](#atajos-de-teclado)
- [Exportar y copias de seguridad](#exportar-y-copias-de-seguridad)
- [Cómo se cuenta](#cómo-se-cuenta)
- [Actualizaciones](#actualizaciones)
- [Linux](#linux)
- [Tus datos](#tus-datos)
- [Preguntas frecuentes](#preguntas-frecuentes)

---

## Instalación e inicio

**Windows:** descarga `SC-Playtime.exe` de la
[página de versiones](https://github.com/hofergeorg-tech/sc-playtime/releases/latest),
ponlo en su propia carpeta (p. ej. `Documentos\SC-Playtime`) e inícialo. No hace falta
instalar nada; el icono de la bandeja (un reloj en un marco) aparece abajo a la derecha de
la barra de tareas.

**Linux:** ver [Linux](#linux).

**Desde el código fuente (Windows):**

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\pythonw.exe run.pyw
```

Solo se ejecuta una instancia a la vez. Un segundo inicio (p. ej. inicio automático más
uno manual) se cierra al momento, para que nada se cuente dos veces.

> **Importante:** Star Citizen debe ejecutarse en modo **«Ventana sin bordes»**. En
> pantalla completa exclusiva no se puede dibujar ningún overlay encima – esto vale para
> todos los overlays.

## El overlay

### Vista compacta

| Elemento | Significado |
| --- | --- |
| Punto arriba a la izquierda | late en verde mientras el juego está abierto; amarillo en AFK; gris desconectado |
| Nombre del juego | el juego mostrado y a su lado el canal (p. ej. **LIVE**) |
| **EN JUEGO** / **AFK** / **DESCONECTADO** | estado arriba a la derecha (AFK: ver [Detección AFK](#detección-afk)) |
| Reloj grande | duración de la sesión en curso; desconectado, la de la última sesión |
| HOY / SEMANA | jugado hoy y desde el lunes de esta semana |

### Estadísticas desplegadas

Un clic en la cabecera del overlay despliega o pliega las estadísticas.

- **Filtro de canal** (TODOS, LIVE, PTU, …): muestra las estadísticas de un solo canal o
  de todos juntos. Aparece en cuanto se han registrado sesiones con canal.
- **Casillas:**

  | Casilla | Significado |
  | --- | --- |
  | HOY | tiempo de juego desde medianoche |
  | SEMANA | desde el lunes a las 0:00 |
  | MES | desde el día 1 del mes |
  | AÑO | desde el 1 de enero |
  | TOTAL | todo lo registrado; arriba a la derecha la fecha del primer registro (desde cuándo se cuenta) |
  | RACHA | días seguidos con al menos 1 minuto de juego. No haber jugado todavía hoy no rompe la racha. |

- **Gráfico** con las pestañas:

  | Pestaña | muestra |
  | --- | --- |
  | DÍA | los últimos 14 días |
  | SEMANA | las últimas 12 semanas |
  | MES | los últimos 12 meses |
  | AÑO | los últimos 5 años |
  | TOTAL | cada año desde tu primera sesión |

  El periodo actual se resalta en verde. Al pasar el ratón por una barra se muestran abajo
  el periodo exacto y el tiempo de juego.

  **Retroceder** (DÍA, SEMANA, MES): las flechas ‹ › arriba a la derecha del gráfico
  saltan medio gráfico hacia el pasado o de vuelta hacia hoy. Con la **rueda del ratón**
  sobre el gráfico se avanza paso a paso (hacia arriba = más antiguo). No se puede
  retroceder más allá de la primera sesión. Al cambiar de pestaña o de filtro, el gráfico
  vuelve a hoy.

  Con un filtro de canal activo (p. ej. PTU), las barras de color muestran solo ese
  canal. Detrás aparece en gris el total de todos los canales y la escala sigue siendo la
  de «TODOS» – así se ve al momento qué parte corresponde al canal. Al pasar el ratón se
  muestra p. ej. «PTU 6m / 11h 31m».
- **Pie:** número de sesiones, sesión media y más larga (las sesiones de menos de 1 minuto
  no cuentan aquí).

## Uso con el ratón

| Acción | Efecto |
| --- | --- |
| Clic en la cabecera | desplegar/plegar estadísticas |
| Arrastrar con el botón izquierdo | mover el overlay (salvo con «Bloquear posición») |
| Clic en un chip de canal | elegir el filtro de canal |
| Clic en una pestaña | cambiar el periodo del gráfico |
| Clic en ‹ / › del gráfico | retroceder / avanzar |
| Rueda sobre el gráfico | un periodo atrás (arriba) o adelante (abajo) |
| Ratón sobre una barra | valores exactos en el pie |
| Clic derecho en el overlay | menú |
| Clic izquierdo en el icono de la bandeja | mostrar/ocultar el overlay |
| Clic derecho en el icono de la bandeja | menú (también con el overlay oculto) |

La posición, el estado desplegado, la pestaña y el filtro se guardan y se restauran en el
siguiente inicio.

## El menú

| Entrada | Función |
| --- | --- |
| Mostrar/Ocultar overlay | solo en el menú de la bandeja |
| Mostrar estadísticas | igual que un clic en la cabecera |
| Juego | elegir el juego mostrado, añadir o quitar juegos |
| Análisis … | mapa de calor, cronología del día y tiempo por parche, ver [Análisis](#análisis-mapa-de-calor-cronología-del-día-parches) |
| Editar sesiones … | corregir o eliminar sesiones, ver [Editar sesiones](#editar-sesiones) |
| FONDO (deslizador) | opacidad solo del fondo oscuro; el texto sigue totalmente visible |
| OPACIDAD TOTAL (deslizador) | opacidad de todo el overlay (20–100 %) |
| Colores | ver [Colores](#colores) |
| Idioma | ver [Idioma](#idioma) |
| Bloquear posición | el overlay ya no se puede mover |
| Dejar pasar los clics | los clics atraviesan el overlay hacia el juego. Solo se desactiva desde el **icono de la bandeja** o el [atajo](#atajos-de-teclado). |
| Mostrar solo mientras un juego está abierto | el overlay se oculta automáticamente sin juego |
| Detección AFK | no contar el tiempo sin actividad, ver [Detección AFK](#detección-afk) |
| Atajos de teclado … | teclas globales para mostrar/ocultar, ver [Atajos de teclado](#atajos-de-teclado) |
| Iniciar con Windows / Iniciar al iniciar sesión | inicio automático al iniciar sesión (sin permisos de administrador) |
| Ayuda … | esta ayuda |
| Novedades … | registro de cambios de cada versión |
| Acerca de SC Playtime … | versión, enlaces, licencia y botón de donación (PayPal) |
| Buscar actualizaciones | consultar GitHub ahora mismo, ver [Actualizaciones](#actualizaciones) |
| Buscar actualizaciones automáticamente | al iniciar y cada 12 horas (por defecto: activado) |
| ⬆ Instalar la actualización … | aparece arriba del todo cuando hay una versión nueva |
| Datos | exportar CSV/JSON, copias, sesiones de otro PC, carpeta de datos, ver [Exportar y copias de seguridad](#exportar-y-copias-de-seguridad) |
| Salir | cerrar el overlay; antes se guarda la sesión en curso |

## Colores

**Menú → Colores** tiene dos apartados. Cada uno ofrece plantillas y además «Elegir color
de fondo …» y «Elegir color de texto …».

**Casillas de estadísticas (en juego)** – desconectado, las casillas son siempre oscuras
con estilo HUD. En cuanto el juego está abierto, se colorean:

- Verde / Oscuro (por defecto)
- Cian / Oscuro
- Ámbar / Oscuro
- Sin color (HUD) – las casillas siguen oscuras también en el juego

**Canal activo** – el chip de canal seleccionado (en la cabecera y en el filtro):

- Automático (color del canal, texto oscuro) – LIVE verde, PTU amarillo, …
- Verde oscuro / Blanco, Negro / Verde, Azul oscuro / Blanco, Blanco / Negro

Consejo: para leer bien, combina fondos claros con texto oscuro y al revés.

## Idioma

**Menú → Idioma** (con bandera) ofrece:

- **Automático (sistema)** – por defecto; el idioma del sistema operativo si está
  disponible, si no inglés
- 🇩🇪 **Deutsch**
- 🇬🇧 **English**
- 🇫🇷 **Français**, 🇪🇸 **Español**, 🇮🇹 **Italiano**, 🇵🇱 **Polski**, 🇨🇳 **简体中文**

El cambio se aplica al momento al overlay, el menú, los mensajes, la ayuda y «Novedades»
– la ayuda y el registro de cambios existen en los siete idiomas.

## Varios juegos

Por defecto se sigue `StarCitizen.exe`. Para añadir más juegos:

1. Clic derecho → **Juego → Añadir juego …**
2. Elige el programa del juego (Windows: el `.exe`; Linux: ver más abajo).
3. Escribe un nombre para mostrar.

El juego se reconoce por el nombre de su programa. Cuando un juego está abierto, el
overlay lo muestra automáticamente; si hay varios, el elegido en el menú. **Quitar juego**
deja de seguirlo – sus sesiones anteriores se conservan.

## Canales (LIVE, PTU, …)

El canal se lee de la carpeta de instalación:

```
…\StarCitizen\LIVE\Bin64\StarCitizen.exe   →  LIVE
…\StarCitizen\PTU\Bin64\StarCitizen.exe    →  PTU
```

Igual con EPTU, HOTFIX y TECH-PREVIEW. Cada sesión recuerda su canal, así las
estadísticas se muestran por canal o todas juntas («TODOS»).

## Análisis (mapa de calor, cronología del día, parches)

**Menú → Análisis …** abre una ventana para el juego mostrado y el filtro de canal
elegido:

- **¿Cuándo juegas?** – un mapa de calor con los días de la semana en filas y las 24
  horas en columnas. Cuanto más clara una casilla, más jugaste a esa hora. Al pasar el
  ratón ves el tiempo exacto; debajo aparecen el día y la hora en que más juegas.
- **Cronología del día** – un día como línea de tiempo de 0 a 24 h: cada sesión es una
  barra del color de su canal, los huecos son pausas o tiempo AFK. Una **marca roja** al
  final de una sesión indica un cierre inesperado, una **amarilla** una desconexión del
  servidor. Con ‹ › pasas de un día jugado a otro; al pasar el ratón por una barra ves la
  hora, la duración, el canal, el parche y cómo terminó la sesión.
- **Tiempo de juego por parche** – tiempo de juego, porcentaje, número de sesiones,
  **cierres inesperados**, **desconexiones** y periodo para cada versión de Star Citizen
  (p. ej. 4.3.1). En los cierres inesperados se muestra además su frecuencia, p. ej.
  «2 · cada 6h 30m» – así ves si un parche es más estable que el anterior. El parche se lee
  al iniciar cada sesión de `build_manifest.id` o `Game.log` en la carpeta de instalación
  (p. ej. `…\StarCitizen\LIVE\`). Las sesiones anteriores a la versión 1.4 y los juegos sin
  estos archivos aparecen como «desconocido».

### Cierres inesperados y desconexiones del servidor

Cuando Star Citizen se cierra, SC Playtime lee el final de `Game.log` (solo lectura):

| En el registro | Significado |
| --- | --- |
| `<SystemQuit>` con «Quit via console command» / «User closed the application» | **cerrado** – lo cerraste tú |
| `<SystemQuit>` con otro motivo, p. ej. «Back-end services are unresponsive» | **desconexión del servidor** – se perdió la conexión con el servidor/backend |
| sin línea `<SystemQuit>`, pero con traspaso al recolector de fallos | **cierre inesperado** |

Las sesiones anteriores se clasifican al iniciar SC Playtime: Star Citizen guarda el
registro de cada inicio en la carpeta `logbackups`, y el registro correcto se encuentra por
la hora en que terminó la sesión. No se pueden clasificar las sesiones sin registro, los
juegos que no son Star Citizen ni las sesiones que terminaron en una pausa AFK. La
instalación se encuentra automáticamente (carpeta por defecto o carpeta desde la que se
ejecutó el juego).

## Editar sesiones

**Menú → Editar sesiones …** lista todas las sesiones del juego mostrado, las más recientes
arriba. Sirve para corregir errores, p. ej. si el PC estuvo en reposo con el juego
abierto:

- La columna **Resultado** muestra cómo terminó la sesión: cerrado, **cierre inesperado**
  (rojo) o **desconexión del servidor** (amarillo), ver
  [Cierres inesperados y desconexiones del servidor](#cierres-inesperados-y-desconexiones-del-servidor).
- **Editar …** (o doble clic): cambiar inicio y fin.
- **Eliminar**: quitar una o varias sesiones marcadas (Ctrl/Mayús para selección múltiple).
  No se puede deshacer – en caso de duda, haz antes una [copia](#exportar-y-copias-de-seguridad).

La sesión en curso (verde, «en curso») queda bloqueada hasta que se cierra el juego.

## Detección AFK

En **Menú → Detección AFK** puedes hacer que no cuente el tiempo sin actividad:
**Desactivada** (por defecto) o pausar tras **5, 10, 15 o 30 minutos** sin teclado, ratón
ni mando.

- Al llegar a ese tiempo, la sesión termina en la **última pulsación** – así el tiempo de
  espera tampoco cuenta. El overlay muestra **AFK** con un punto amarillo.
- En cuanto vuelve a haber actividad y el juego sigue abierto, empieza automáticamente
  una sesión nueva.
- Cuenta cualquier actividad en el PC, no solo en el juego.
- En Linux funciona con X11/XWayland (biblioteca `libXss`); sin ella la detección no tiene
  efecto.

## Anti-AFK

Star Citizen te expulsa tras un rato sin actividad. **Menú → Anti-AFK** mantiene el juego
despierto (solo **Windows**):

- **Anti-AFK activo** es el interruptor principal (también **Ctrl+Mayús+F12**). Mientras esté
  activado, las acciones elegidas se ejecutan a su ritmo, incluso mientras juegas.
- **Pulsar la tecla:** pulsa la tecla a la derecha de la P (` en teclado español, [ en US),
  por defecto cada 5 s. Mejor no asignarle nada en el juego.
- **Mover el ratón:** recorre un pequeño patrón (derecha–izquierda, arriba–abajo, cuadrado,
  círculo o aleatorio) y vuelve al punto de partida. **Distancia** (1–100 píxeles),
  **velocidad** e **intervalo del ratón** son configurables.
- Solo se envía **si el juego está en primer plano**: nunca escribirás por error en un chat u
  otra ventana.
- Se envían scancodes reales; Star Citizen ignora los simples códigos de tecla (como los de
  «Move Mouse»).
- **Anillos en el overlay:** junto al reloj, un anillo por acción muestra su ritmo y el overlay
  indica **ANTI-AFK**. Un clic en un anillo activa o desactiva esa acción.
- Las entradas del Anti-AFK no cuentan como actividad: la [detección AFK](#detección-afk) sigue
  pausando si tú no haces nada.

## Atajos de teclado

Los atajos globales funcionan en todas partes, también con el juego en primer plano (solo
**Windows**):

| Por defecto | Efecto |
| --- | --- |
| **Ctrl+Mayús+F9** | mostrar/ocultar el overlay |
| **Ctrl+Mayús+F11** | activar/desactivar «Dejar pasar los clics» |
| **Ctrl+Mayús+F12** | activar/desactivar Anti-AFK |

Se cambian en **Menú → Atajos de teclado …**: haz clic en el campo, pulsa la combinación
nueva, vacíalo con ✕ (= sin atajo). Se permiten letras, cifras, F1–F24, Inicio/Fin/Insert/
Supr, RePág/AvPág, flechas, Pausa y Espacio – salvo con las teclas F, siempre con Ctrl,
Mayús, Alt o Win. Si otro programa ya usa la combinación, aparece un aviso.

## Exportar y copias de seguridad

En **Menú → Datos**:

| Entrada | Función |
| --- | --- |
| Exportar como CSV … | todas las sesiones de todos los juegos como tabla, p. ej. para Excel (columnas: juego, canal, parche, inicio, fin, duración en segundos y minutos, resultado `quit`/`crash`/`server`) |
| Exportar como JSON … | lo mismo en JSON, horas además con zona horaria y como marca de tiempo Unix |
| Hacer copia ahora | crear ahora mismo una copia de la base de datos |
| Copia automática diaria (7 días) | una copia al día; se conservan las 7 últimas (por defecto: activado) |
| Abrir carpeta de copias | carpeta `backups` dentro de la carpeta de datos |
| Importar sesiones de otro PC … | añadir el tiempo de juego de un segundo PC, ver abajo |
| Abrir carpeta de datos | carpeta con la base de datos y la configuración |

**Restaurar una copia:** cierra el overlay, sustituye `playtime.db` en la carpeta de datos
por el archivo deseado de `backups` (p. ej. copia `playtime-2026-10-04.db` y cámbiale el
nombre a `playtime.db`) y vuelve a iniciar el overlay.

### Unir dos PC

Si juegas en varios PC, añade el tiempo de juego del otro PC así:

1. En el otro PC, toma el archivo `playtime.db` de la carpeta de datos (o una copia de
   `backups`), p. ej. con una memoria USB o una carpeta en la nube.
2. Aquí, **Menú → Datos → Importar sesiones de otro PC …** y elige el archivo.
3. SC Playtime indica cuántas sesiones son nuevas y cuántas ya están, y tras tu
   confirmación importa solo las nuevas. Antes se hace una copia de los datos actuales.

Una sesión cuenta como «ya está» si se solapa en el tiempo con una sesión del mismo juego
de aquí – el mismo juego no se ejecuta a la vez en dos PC. Por eso puedes volver a
importar el mismo archivo más adelante sin que nada cuente dos veces. También se importan
el canal, el parche y el resultado. Los juegos que aún no existen aquí se indican: sus
sesiones se guardan y aparecen en cuanto añadas el juego con el mismo nombre.

## Cómo se cuenta

- La lista de procesos se lee cada 2 segundos. Solo se **lee** – no se inyecta nada en el
  juego.
- Si inicias el overlay con el juego ya abierto, la sesión cuenta igualmente desde el
  inicio real del juego.
- El final de la sesión se guarda cada 30 segundos. Si el PC se cuelga, se pierden como
  mucho esos 30 segundos.
- Las sesiones que pasan la medianoche (o un límite de semana/mes) se reparten de forma
  proporcional.

## Actualizaciones

La versión actual aparece arriba en el menú (p. ej. «SC PLAYTIME 1.5.0»).

- **Automático:** con «Buscar actualizaciones automáticamente» activado, SC Playtime
  consulta GitHub poco después de iniciarse y luego cada 12 horas. Si hay una versión
  nueva, aparece un aviso en el icono de la bandeja y arriba del menú la entrada
  **«⬆ Instalar la actualización …»**.
- **A mano:** Menú → «Buscar actualizaciones».
- **Instalar:** tras confirmar, se descarga la versión nueva y se compara con la suma de
  comprobación que GitHub indica para la versión – si no coincide, no se instala nada. El
  overlay guarda la sesión en curso, se cierra, sustituye el programa y se reinicia.
  Después se muestra una vez «Novedades». La configuración y los tiempos de juego se
  conservan.
- Si SC Playtime se ejecuta desde el código fuente (`run.pyw`) en lugar del programa
  compilado, «Instalar» abre la página de versiones en el navegador – no hay un archivo
  de programa que sustituir. Para actualizar con un clic, usa el EXE y desactiva y vuelve a
  activar el inicio automático en el menú.

Todas las versiones están también en
<https://github.com/hofergeorg-tech/sc-playtime/releases>.

## Linux

**Programa listo:** descarga `SC-Playtime-linux-x86_64` de la
[página de versiones](https://github.com/hofergeorg-tech/sc-playtime/releases/latest),
ponlo p. ej. en `~/Aplicaciones/`, hazlo ejecutable e inícialo:

```bash
chmod +x SC-Playtime-linux-x86_64
./SC-Playtime-linux-x86_64
```

**Desde el código fuente:**

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.pyw
```

Notas:

- **Star Citizen con Wine/Proton/Lutris** se detecta igual que en Windows – canal incluido
  (LIVE, PTU, …), porque también se lee la ruta de Windows del juego. Los cierres
  inesperados y desconexiones solo se detectan en Windows.
- **Juegos nativos de Linux:** añádelos con «Añadir juego …» eligiendo su programa (pon el
  filtro en «Todos los archivos»). Se reconocen por el nombre del programa.
- **Wayland:** en Wayland las ventanas no pueden elegir su posición ni quedarse en primer
  plano. Por eso SC Playtime se inicia automáticamente mediante **XWayland**, disponible en
  casi todos los escritorios. Para otra opción, define tú mismo `QT_QPA_PLATFORM`.
- **Icono de la bandeja en GNOME:** GNOME solo muestra iconos con la extensión
  «AppIndicator and KStatusNotifierItem Support». KDE, XFCE, Cinnamon y demás no necesitan
  nada.
- El **inicio automático** se llama «Iniciar al iniciar sesión» en el menú y crea
  `~/.config/autostart/sc-playtime.desktop`.
- Los **datos** están en `~/.local/share/SC-Playtime/`.

## Tus datos

Todo se guarda en local (Menú → «Abrir carpeta de datos»):

- Windows: `%APPDATA%\SC-Playtime\`
- Linux: `~/.local/share/SC-Playtime/`

| Archivo | Contenido |
| --- | --- |
| `playtime.db` | base de datos SQLite con todas las sesiones (juego, canal, inicio, fin, parche, resultado) |
| `settings.json` | posición, transparencia, colores, idioma, lista de juegos, carpetas de Star Citizen encontradas, … |
| `backups/` | copias diarias de la base de datos, ver [Exportar y copias de seguridad](#exportar-y-copias-de-seguridad) |

Tus tiempos de juego y tu configuración nunca salen de tu PC. La única conexión a
Internet es la búsqueda de actualizaciones: solo consulta la información pública de
versiones en GitHub y se puede desactivar en el menú. Para hacer una copia o mudarte,
copia sin más la carpeta. Para restablecer la configuración, borra `settings.json` con el
overlay cerrado.

## Preguntas frecuentes

**El overlay no se ve en el juego.**
Pon Star Citizen en «Ventana sin bordes». Comprueba que no se haya ocultado desde el icono
de la bandeja.

**Ya no puedo hacer clic en el overlay.**
«Dejar pasar los clics» está activado. Pulsa **Ctrl+Mayús+F11** o haz clic derecho en el
icono de la bandeja y quita la marca.

**El menú o una ventana aparece detrás del juego.**
Desde la versión 1.4, los menús y diálogos se muestran siempre delante del overlay y del
juego. Si aun así una ventana queda tapada, cambia a ella con Alt+Tab.

**El tiempo de juego es incorrecto porque dejé el juego abierto.**
Corrige la sesión en **Menú → Editar sesiones …** y activa en adelante la
[detección AFK](#detección-afk).

**El overlay ha desaparecido.**
Un clic izquierdo en el icono de la bandeja lo vuelve a mostrar. Con «Mostrar solo
mientras un juego está abierto» no aparece sin juego.

**El inicio automático ya no funciona.**
La entrada apunta a la ubicación del programa o de `run.pyw`. Tras mover la carpeta,
desactiva y vuelve a activar el inicio automático en el menú.

**La actualización falla.**
Comprueba la conexión a Internet y vuelve a intentarlo con «Buscar actualizaciones». Si
el programa está en una carpeta protegida (p. ej. `C:\Archivos de programa` o
`/usr/bin`), no puede sustituirse a sí mismo – descarga la versión nueva desde la página
de versiones o pon el programa en su propia carpeta.

**Windows dice «Windows protegió su PC».**
El EXE todavía no tiene firma digital (solicitada, ver [CODE_SIGNING.md](CODE_SIGNING.md)),
por eso SmartScreen avisa con las descargas nuevas. Haz clic en «Más información» →
«Ejecutar de todas formas». Para comprobar que el archivo se compiló realmente desde este
repositorio:
`gh attestation verify SC-Playtime.exe --repo hofergeorg-tech/sc-playtime`

**¿Interfiere con el antitrampas?**
SC Playtime solo lee la lista de procesos y la hora de inicio del juego con funciones
normales del sistema, como el Administrador de tareas, y tras cerrar el juego el archivo de
texto `Game.log`. No accede al juego.

**Una sesión no tiene resultado.**
El registro no mostraba ni un final normal ni un cierre inesperado – p. ej. si Star
Citizen se cerró desde el Administrador de tareas, se fue la luz, la sesión terminó en una
pausa AFK o ya no existe registro. La clasificación solo sirve para las estadísticas y no
cambia el tiempo de juego.
