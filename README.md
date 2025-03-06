# Gitea Hash Extractor & Cracker 🔒💻

Este script de Python permite extraer y crackear hashes de contraseñas almacenados en una base de datos SQLite3 de Gitea. Los hashes extraídos están en formato **PBKDF2** y pueden ser convertidos a un formato compatible con **Hashcat** para su posterior cracking. Además, el script puede realizar el cracking de los hashes directamente dentro del propio script utilizando un diccionario de contraseñas.

## Requisitos 🚀


Puedes instalar todas las dependencias necesarias usando `pip`:
```bash
pip install -r requirements.txt
```

## Descripción del Script 📝

Este script permite:

1. **Extraer los hashes de contraseñas** desde una base de datos SQLite3 de Gitea.
2. **Guardar los hashes extraídos** en un archivo con formato compatible con **Hashcat**.
3. **Crackear los hashes** directamente en el script utilizando una lista de palabras (wordlist).
4. **Verificar las contraseñas** encontradas para los hashes extraídos.

## Uso ⚙️

1. Extraer los hashes de `gitea.db` y convertirlos a un formato compatible con Hashcat:

```bash
python3 GetGiteaPasswords.py -d gitea.db
```

2. Crackear los hashes utilizando el archivo `rockyou.txt`:

```bash
python3 GetGiteaPasswords.py -d gitea.db -w rockyou.txt --crack
```

## Argumentos del Script 🎯

```bash
usage: getGiteaPasswords.py [-h] -d SQLITE_DB [-w WORDLIST] [-c] [-o OUTPUT_FILE]

☕ Retrieve Gitea hashes stored in SQLite3 database with pbkdf2 format. ☕ 
 

	Format pbkdf2 hashes into hashcat format (Fastest Method):
		❯ python3 getGiteaPasswords.py -d gitea.db

	Crack hashes directly within the script (Slowest Method):
		❯ python3 getGiteaPasswords.py -d gitea.db -w rockyou.txt --crack

options:
  -h, --help                  show this help message and exit
  -d, --database SQLITE_DB    SQLite3 database file
  -w, --wordlist WORDLIST     Wordlist file
  -c, --crack                 Add this option to crack hashes in the script
  -o, --output   OUTPUT_FILE  Output file                                   (default = hashes.txt)
```

## Información Adicional 🔍

- Si deseas usar **Hashcat** para crackear los hashes, puedes usar el archivo `hashes.txt` generado con el siguiente comando:

```bash
hashcat hashes.txt /ruta/a/wordlist.txt
```

## Contribuciones 🤝

Las contribuciones a este proyecto son bienvenidas. Si encuentras errores o tienes mejoras que proponer, abre un **issue** o un **pull request**. ¡Todo aporte es bienvenido! 🙌

## Licencia 📜

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
