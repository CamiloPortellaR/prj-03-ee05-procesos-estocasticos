# prj-03-ee05-procesos-estocasticos

Curso EE05 Procesos Estocásticos. Cada sesión es un mini-proyecto
independiente en `sesiones/` (código en `core/` y `models/`, datos en
`data/`, documentos en `docs/`).

> **Antes de `dvc pull`:** hace falta el archivo `.dvc/config.local`, que no
> está en GitHub. Se saca de Bitwarden (ver «Mapa de Bitwarden»). Sin él, DVC
> no puede entrar a Google Drive.

## Dónde vive cada cosa

| Qué | Dónde | Cómo se recupera |
|---|---|---|
| Código, textos, `.gitignore` y punteros `.dvc` | GitHub | `git clone` |
| Datos (CSV, Excel), PDF, Word, gráficos, resultados `.npz` | Google Drive, vía DVC | `dvc pull` |
| Claves (`.dvc/config.local`) | Bitwarden | Copiar y pegar a mano |
| `.venv/`, `.dvc/cache/`, `__pycache__/`, `.tools/` | Ningún sitio, a propósito | Se reinstalan (pasos abajo) |

Regla: un archivo nuevo va a uno de esos sitios en la misma tarea en que se
crea. Ningún dato ni binario se hace `git add`; se hace `dvc add` y se sube
a Git solo su `.dvc`.

## Mapa de Bitwarden (qué hay y dónde; nunca su contenido)

Entrada: <https://vault.bitwarden.com>, cuenta del Director.
Carpeta: `prj-03-ee05-procesos-estocasticos`.

- **`.dvc/config.local — prj-03-ee05-procesos-estocasticos`** (tipo: Nota)
  - Qué tiene: el archivo `.dvc/config.local` completo, con el cliente de
    Google que usa DVC para entrar a Drive. Es el mismo cliente de
    `prj-02-capital-fluido-web` y `prj-04-ee74-topicos-manufactura`.
  - Se actualiza: cada vez que cambie ese archivo.

Si se agrega, renombra o borra algo en Bitwarden, se actualiza este mapa en
la misma tarea.

## Rehacer el proyecto en una PC nueva (Ubuntu)

1. Clonar:

   ```bash
   git clone https://github.com/CamiloPortellaR/prj-03-ee05-procesos-estocasticos.git
   cd prj-03-ee05-procesos-estocasticos
   ```

2. Entorno de Python (3.12):

   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

3. Claves: crear `.dvc/config.local` y pegar el contenido de la nota de
   Bitwarden de arriba.

4. Datos:

   ```bash
   .venv/bin/dvc pull
   ```

   La primera vez abre el navegador: iniciar sesión con la cuenta de Google
   dueña de la carpeta de Drive. Debe terminar sin errores y
   `.venv/bin/dvc status -c` debe decir «in sync».

5. Pandoc 3.6.4 (solo para exportar informes a Word/PDF):

   ```bash
   mkdir -p .tools/pandoc && cd .tools/pandoc
   wget https://github.com/jgm/pandoc/releases/download/3.6.4/pandoc-3.6.4-linux-amd64.tar.gz -O pandoc.tar.gz
   tar xzf pandoc.tar.gz --strip-components=1
   cd ../..
   ```

6. Activación automática del entorno (opcional): el archivo `.auto-venv`
   solo funciona si `~/.bashrc` tiene la función `__auto_project_venv`, que
   no está en este repositorio. Sin ella, activar a mano con
   `source .venv/bin/activate`.

## Si DVC responde «invalid_grant»

Venció el permiso de Google (con la app de Google Cloud en modo «Prueba»
vence cada 7 días). Apartar
`~/.cache/pydrive2fs/<client_id>/default.json`, correr
`.venv/bin/dvc status -c` e iniciar sesión otra vez con la cuenta dueña de
la carpeta de Drive.

## Al agregar datos nuevos

Primero Drive, después GitHub:

```bash
.venv/bin/dvc add ruta/al/archivo
.venv/bin/dvc push
git add ruta/al/archivo.dvc ruta/.gitignore
git commit -m "..."
git push
```
