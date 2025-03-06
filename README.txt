# Gitea Hash Extractor & Cracker 🔒💻

Este script de Python permite extraer y crackear hashes de contraseñas almacenados en una base de datos SQLite3 de Gitea. Los hashes extraídos están en formato PBKDF2 y pueden ser convertidos a un formato compatible con **Hashcat** para su posterior cracking. Además, el script puede realizar el cracking de los hashes directamente dentro del propio script utilizando un diccionario de contraseñas.

## Requisitos 🚀

- Python 3.x
- Bibliotecas de Python necesarias:
  - `colorama` 🌈
  - `pwn` 💥
  - `base64` 🔑
  - `binascii` 🖥️
  - `argparse` ⚙️
  - `sqlite3` 🗃️
  - `hashlib` 🔒
  - `multiprocessing` ⚡
  - `concurrent.futures` ⏱️

Puedes instalar todas las dependencias necesarias usando `pip`:
```bash
pip install colorama pwn
```

## Descripción del Script 📝

Este script permite:

1. **Extraer los hashes de contraseñas** desde una base de datos SQLite3 de Gitea.
2. **Guardar los hashes extraídos** en un archivo con formato compatible con **Hashcat**.
3. **Crackear los hashes** directamente en el script utilizando una lista de palabras (wordlist).
4. **Verificar las contraseñas** encontradas para los hashes extraídos.

## Uso ⚙️

### 1. Extraer y convertir los hashes a formato Hashcat

Para extraer los hashes de la base de datos SQLite3 de Gitea y convertirlos a un formato compatible con **Hashcat**, ejecuta el siguiente comando:

```bash
python3 GetGiteaPasswords.py -d gitea.db
```

Este comando extraerá los hashes de la base de datos `gitea.db` y los guardará en un archivo de salida llamado `hashes.txt` 📝.

### 2. Crackear los hashes utilizando un archivo wordlist 📜

Si quieres crackear los hashes directamente dentro del script, puedes usar un archivo wordlist de contraseñas con el siguiente comando:

```bash
python3 GetGiteaPasswords.py -d gitea.db -w /ruta/a/wordlist.txt --crack
```

Este comando cargará los hashes desde la base de datos `gitea.db`, utilizará el archivo `wordlist.txt` para intentar crackear las contraseñas y te mostrará los resultados en la terminal 💻.

### 3. Guardar los resultados de los hashes 💾

Si prefieres guardar los resultados en un archivo de salida, puedes especificar un nombre de archivo con el argumento `-o`:

```bash
python3 GetGiteaPasswords.py -d gitea.db -o resultados.txt
```

Esto guardará los hashes extraídos en un archivo llamado `resultados.txt` 📄.

## Argumentos del Script 🎯

- `-d, --database`: El archivo de base de datos SQLite3 que contiene los datos de Gitea (requerido).
- `-w, --wordlist`: El archivo de wordlist para crackear los hashes (opcional si se usa el modo de cracking).
- `-c, --crack`: Opción para activar el modo de cracking de los hashes 🔓.
- `-o, --output`: El archivo donde se guardarán los resultados (por defecto, `hashes.txt`).

## Ejemplo de uso 📚

1. Extraer los hashes de `gitea.db` y convertirlos a un formato compatible con Hashcat:

```bash
python3 GetGiteaPasswords.py -d gitea.db
```

2. Crackear los hashes utilizando el archivo `rockyou.txt`:

```bash
python3 GetGiteaPasswords.py -d gitea.db -w rockyou.txt --crack
```

3. Guardar los resultados en un archivo llamado `resultados.txt`:

```bash
python3 GetGiteaPasswords.py -d gitea.db -o resultados.txt
```

## Información Adicional 🔍

- Si deseas usar **Hashcat** para crackear los hashes, puedes usar el archivo `hashes.txt` generado con el siguiente comando:

```bash
hashcat -m 22000 hashes.txt /ruta/a/wordlist.txt
```

## Contribuciones 🤝

Las contribuciones a este proyecto son bienvenidas. Si encuentras errores o tienes mejoras que proponer, abre un **issue** o un **pull request**. ¡Todo aporte es bienvenido! 🙌

## Licencia 📜

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
