from os import system as ossys
from platform import system as platsys


def instalar_matplotlib():
	"""Tenta instalar a biblioteca matplotlib no sistema atual.

	Raises:
		ImportError: Se houver falha durante ou após instalar o matplotlib.
	"""

	# Tente importar matplotlib, se falhar, tente instalar
	try:
		from matplotlib import pyplot

	except ImportError:

		print("Instalando matplotlib, aguarde...")

		# Se for Windows, dê o comando, instale e limpe a tela
		if (platsys().upper() == "WINDOWS"):
			ossys("pip install --user matplotlib /quiet")
			ossys("cls")

		# Senão, é MAC ou Linux
		else:
			ossys("sudo apt install python3-tk 2>&1 >/dev/null")
			ossys("pip3 install --user matplotlib 2>&1 >/dev/null")
			ossys("clear")

	# Se após tentar instalar, o erro ainda persistir, avise e saia
	finally:

		try:
			from matplotlib import pyplot

		except:
			raise ImportError("Falha ao instalar dependências necessárias. Bye.")
