# Gitea Hash Extractor & Cracker 🔒💻

Este script de Python permite extraer y crackear hashes de contraseñas almacenados en una base de datos SQLite3 de Gitea. Los hashes extraídos están en formato **PBKDF2** y pueden ser convertidos a un formato compatible con **Hashcat** para su posterior cracking. Además, el script puede realizar el cracking de los hashes directamente dentro del propio script utilizando un diccionario de contraseñas.

## Requisitos 🚀

Puedes instalar todas las dependencias necesarias usando `pip`:
```bash
pip install -r requirements.txt
```

## Argumentos del Script 🎯

```ps
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

## Uso ⚙️

1. Extraer los hashes de `gitea.db` y convertirlos a un formato compatible con Hashcat:

```bash
python3 GetGiteaPasswords.py -d gitea.db
```

2. Crackear los hashes utilizando el archivo `rockyou.txt` **(Forma más lenta)**:

```bash
python3 GetGiteaPasswords.py -d gitea.db -w rockyou.txt --crack
```

## Información Adicional 🔍

1. Si deseas usar **Hashcat** para crackear los hashes, puedes usar el archivo generado con el siguiente comando **(Forma más rápida)**:

```bash
hashcat hashes.txt /ruta/a/wordlist.txt
```

## Futuras Mejoras 🚀

Planeamos agregar nuevas funcionalidades para hacer el script aún más potente y versátil:

- 🔹 **Exportación de resultados en múltiples formatos** como JSON o CSV.
- 🔹 **Implementación de un potfile (almacén de hashes crackeados)** para evitar volver a crackear contraseñas ya resueltas y mejorar la eficiencia. 🚀

¡Si tienes alguna sugerencia o mejora, no dudes en contribuir al proyecto! 🎉

### Advertencia legal ⚠️

> [!WARNING]
> Este software está destinado solo para uso personal y debe utilizarse únicamente en entornos controlados y con autorización previa. El empleo de esta herramienta en sistemas o redes sin la debida autorización puede ser ilegal y contravenir políticas de seguridad. El desarrollador no se hace responsable de daños, pérdidas o consecuencias resultantes de su uso inapropiado o no autorizado. Antes de utilizar esta herramienta, asegúrate de cumplir con todas las leyes y regulaciones locales pertinentes.