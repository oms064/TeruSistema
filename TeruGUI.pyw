import tkinter as tk
from tkinter import messagebox as mb
import SistemaTeru
		
class MesaGUI(tk.Frame):
	"""
	Aquí es donde se se hace la comanda para una mesa
	Esta clase es llamada desde Instanciador y puede instanciar tantas MesaGUI como sea necesario.
	"""
	def __init__(self, sistema, nombreMesa="", master=None):
		tk.Frame.__init__(self, master)
		self.nombreMesa = nombreMesa
		self.master.title("Comanda: " + str(self.nombreMesa.get()))
		self.master.geometry("480x270")
		self.pack()
		self.sistema = sistema
		self.createWidgets()

	def createWidgets(self):
		"""
		Este método es llamado siempre desde init, se crean todos los widgets dentro de la ventana
		"""
		self.numClientes = tk.StringVar()
		self.dinRecibido = tk.StringVar()
		self.propina = tk.StringVar()
		self.total = tk.StringVar()
		self.tarjeta = tk.IntVar()
		self.idCliente = tk.StringVar()

		tk.Label(self.master, text="Clientes:").place(x=50, y=10)
		tk.Entry(self.master, textvariable=self.numClientes).place(x=110, y=10)

		tk.Label(self.master, text="Cambiar Nombre:").place(x=300, y=10)
		tk.Entry(self.master, textvariable=self.nombreMesa, width=10).place(x=410, y=10)
		tk.Button(self.master, text="Cambiar", command=self.cambiarMesa).place(x=415, y=35)

		tk.Label(self.master, text="Propina:").place(x=50, y=30)
		tk.Entry(self.master, textvariable=self.propina).place(x=110, y=30)

		tk.Label(self.master, text="Consumo:").place(x=40, y=50)
		tk.Entry(self.master, textvariable=self.total).place(x=110, y=50)

		tk.Label(self.master, text="Dinero recibido:").place(x=10, y=70)
		tk.Entry(self.master, textvariable=self.dinRecibido).place(x=110, y=70)
		tk.Checkbutton(self.master, text="Tarjeta:", variable=self.tarjeta).place(x=250, y=70)

		tk.Label(self.master, text="ID Cliente:").place(x=40, y=90)
		tk.Entry(self.master, textvariable=self.idCliente).place(x=110, y=90)

		tk.Button(self.master, text="Aceptar", command=self.confirmarComanda).place(x=185,y=115)
		tk.Button(self.master, text="Borrar", command=self.clearComanda).place(x=125,y=115)

		tk.Label(self.master, text="Mesa:").place(x=350,y=110)
		self.labelMesa = tk.Label(self.master, text=self.nombreMesa.get()[:2], font=("Times", 50))
		self.labelMesa.place(x=380,y=130)

		tk.Label(self.master, text="Consumo:").place(x=40, y=150)
		self.textoConsumo = tk.Text(self.master, width=24, height=5)
		self.textoConsumo.place(x=110, y=150)
		tk.Button(self.master, text="Añadir", command=self.agregar).place(x=260, y=240)
		tk.Button(self.master, text="Calcular", command=self.consumo).place(x=200, y=240)
		tk.Button(self.master, text="Borrar", command=self.clearConsumo).place(x=140,y=240)


	def cambiarMesa(self):
		"""
		Se el asigna el nombre a la mesa en caso de que no exista o se quiera cambiar.
		El nombre aparece en el título de la ventana.
		"""
		if self.nombreMesa.get() != "":
			self.master.title("Comanda: " + str(self.nombreMesa.get()))
			self.labelMesa.config(text=self.nombreMesa.get()[:2])
			self.nombreMesa.set("")

	def confirmarComanda(self):
		"""
		Se confirma que la comanda sea correcta.
		Se existe algún error se abrirá una ventana indicando que hay un error.(Cualquier error)
		"""
		if self.propina.get() == "":
			self.propina.set("0")
		self.master.withdraw()
		self.sistema.nuevaComanda(self.numClientes.get(), self.total.get(), self.dinRecibido.get(), self.propina.get(), bool(self.tarjeta.get()), self.idCliente.get())
		if self.sistema:
			mb.showinfo("¡Error!", "Se ha producido un error.")
		else:
			if mb.askokcancel("Comanda", self.sistema.comanda.cobro()):
				self.aceptarComanda()
			else:
				self.show()

	def clearComanda(self):
		"""
		Se limpian los datos de la comanda.
		"""
		self.numClientes.set("")
		self.dinRecibido.set("")
		self.propina.set("")
		self.total.set("")
		
	def clearConsumo(self):
		"""
		Se limpia los datos de consumo.
		"""
		self.textoConsumo.delete('1.0', '2.0')

	def consumo(self):
		"""
		Se obitene todos los valores escritos en consumo separados por espacios, se suman todos.
		"""
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			cons = self.sistema.calculoComanda(cons)
			self.total.set(cons["Total"])
			self.propina.set(cons["Propina"])
		except ValueError:
			self.consWindow = tk.Toplevel(self)
			self.consWindow.wm_title("Resultado")
			self.consWindow.geometry("200x150")
			tk.Label(self.consWindow, text="Error!").place(x=30, y=20)
			tk.Button(self.consWindow, text="Aceptar", command=self.consWindow.destroy).place(x=75,y=90)
		
	def agregar(self):
		"""
		Lo mismo que consumo pero se suma la cantida o lo que ya haya en Consumo.
		"""
		cons = self.textoConsumo.get("1.0","end").split()
		try:
			cons = [int(x) for x in cons]
			if self.total.get() == "":
				cons = self.sistema.calculoComanda(cons)
			else:
				cons = self.sistema.calculoComanda(cons + [int(self.total.get())])
			self.total.set(cons["Total"])
			self.propina.set(cons["Propina"])
		except ValueError:
			self.consWindow = tk.Toplevel(self)
			self.consWindow.wm_title("Resultado")
			self.consWindow.geometry("200x150")
			tk.Label(self.consWindow, text="Error!").place(x=30, y=20)
			tk.Button(self.consWindow, text="Aceptar", command=self.consWindow.destroy).place(x=75,y=90)

	def aceptarConsumo(self):
		"""
		Se confirma el consumo.
		"""
		self.consWindow.destroy()
		self.master.destroy()
		self.clearConsumo()

	def aceptarComanda(self):
		"""
		Se confirma la comanda.
		"""
		self.sistema.commitComanda()
		self.clearComanda()

	def show(self):
		"""
		Se regresa a MesaGUI
		"""
		self.master.update()
		self.master.deiconify()

class CierreGUI(tk.Frame):
	"""
	En esta ventana se maneja todo lo conciernente al cierre de caja.
	"""
	def __init__(self, sistema, master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self.sistema = sistema
		self.padre.withdraw()
		self.master.wm_title("Cierre")
		self.master.geometry("280x250")
		self.pack()
		self.createWidgets()
		self.master.protocol("WM_DELETE_WINDOW", self.showMain)

	def createWidgets(self):
		"""
		Se crean todos los widgets de la ventana.
		"""
		self.dinero = tk.StringVar()
		self.gastos = tk.StringVar()
		self.nomina = tk.StringVar()
		self.dineroInicial = tk.StringVar()
		self.dia = tk.StringVar()
		self.dineroLlevo = tk.StringVar()

		tk.Label(self.master, text="Fecha (dd-mm-año):").place(x=10,y=10)
		tk.Entry(self.master, textvariable=self.dia).place(x=130, y=10)
		tk.Label(self.master, text="Nota: Dejar vacío si se quiere el día de hoy").place(x=30,y=30)
		tk.Label(self.master, text="Dinero en caja:").place(x=45,y=60)
		tk.Entry(self.master, textvariable=self.dinero).place(x=130, y=60)
		tk.Label(self.master, text="Dinero Inicial:").place(x=50,y=90)
		tk.Entry(self.master, textvariable=self.dineroInicial).place(x=130, y=90)
		tk.Label(self.master, text="Gastos:").place(x=85,y=120)
		tk.Entry(self.master, textvariable=self.gastos).place(x=130, y=120)
		tk.Label(self.master, text="Nómina(Total):").place(x=45,y=150)
		tk.Entry(self.master, textvariable=self.nomina).place(x=130, y=150)

		tk.Button(self.master, text="Cancelar", command=self.showMain).place(x=50,y=180)
		tk.Button(self.master, text="Aceptar", command=self.cerrarCaja).place(x=150,y=180)

	def cerrarCaja(self):
		"""
		Llama al sistema para cerrar caja con los datos introducidos en la ventana CerrarCaja
		"""
		if self.dinero.get().isdigit():

			self.master.withdraw()
			self.reporteWindow = tk.Toplevel(self)
			self.reporteWindow.wm_title("Reporte del día")
			self.reporteWindow.geometry("280x280")

			reporte = self.sistema.cierreDeCaja(self.dinero.get(), self.dineroInicial.get(), self.gastos.get(), self.nomina.get(), self.dia.get())
			cadReporte = reporte[0].split(",")
			cadReporte = "Total Mesas: " + cadReporte[1] + "\nTotal Clientes: " + cadReporte[2] + \
			"\nDinero Inicial: " + cadReporte[3] + "\Ventas Efectivo: " + cadReporte[4] + "\nTerminal: " + cadReporte[5] + \
			"\nGastos: " + cadReporte[6] + "\nNomina: " + cadReporte[7] + "\nNeto: " + cadReporte[8] + "\nDinero: " + cadReporte[9] + \
			"\nSobra/Falta: " + cadReporte[10] + "\nPropinas: " + str(reporte[1])
			
			tk.Label(self.reporteWindow, text=cadReporte).place(x=80, y=10)
			tk.Label(self.reporteWindow, text="Llevo: ").place(x=60, y=180)
			tk.Entry(self.reporteWindow, textvariable=self.dineroLlevo).place(x=100, y=180)
			tk.Button(self.reporteWindow, text="Cancelar", command=self.cancelarReporte).place(x=50,y=210)
			tk.Button(self.reporteWindow, text="Aceptar", command=self.aceptarCierre).place(x=150,y=210)

	def aceptarCierre(self):
		"""
		Se confirma el cierre.
		"""
		self.sistema.commitCierre(self.dineroLlevo.get(), self.dia.get())
		self.reporteWindow.destroy()
		self.showMain()

	def showMain(self):
		"""
		Se retorna a la ventana padre.
		"""
		self.padre.abrirVentana()
		self.master.destroy()

	def cancelarReporte(self):

		self.reporteWindow.destroy()
		self.master.update()
		self.master.deiconify()

class Instanciador(tk.Frame):
	"""
		Ventana principal donde se sacaran nuevas comandas y se hará el cierre de caja
	"""
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.master.title("Teru Sistema")
		self.master.geometry("170x220")
		self.pack()
		master.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
		self.sistema = SistemaTeru.MainSystem()
		self.createWidgets()

	def createWidgets(self):
		self.textContador = tk.StringVar()
		self.nombreMesa = tk.StringVar()
		self.textContador.set("Mesas: " + str(self.sistema.conf["visitas"]))
		self.folioLabel = tk.Label(self.master, textvariable=self.textContador).place(x=60, y=10)
		tk.Label(self.master, text="Nombre Mesa:").place(x=10,y=40)
		tk.Entry(self.master, width=10, textvariable=self.nombreMesa).place(x=100,y=40)
		tk.Button(self.master, text="Nueva Mesa", command=self.nuevaMesa).place(x=50,y=70)
		tk.Button(self.master, text="Cierre de caja", command=self.datosCierre).place(x=45,y=110)
		tk.Button(self.master, text="Estado Actual", command=self.estadoActual).place(x=45, y=150)
		tk.Button(self.master, text="Clientes", command=self.abrirClientesGUI).place(x=55, y=190)

	def estadoActual(self):
		estado = self.sistema.getState()
		self.estadoWindow = tk.Toplevel(self)
		self.estadoWindow.wm_title("Estado Actual")
		self.estadoWindow.geometry("250x180")
		tk.Label(self.estadoWindow, text=estado).place(x=80, y=10)

	def abrirClientesGUI(self):
		"""
		Acción para el botón "Clientes" cuya ventana es para hacer acciones sobre la tabla de clientes
		"""
		ClientesGUI(self.sistema, tk.Toplevel(self), self)

	def nuevaMesa(self):
		"""
			Se abre una nueva ventana para cobrar una mesa
		"""
		self.sistema.conf["visitas"] += 1
		self.textContador.set("Mesas: " + str(self.sistema.conf["visitas"]))
		MesaGUI(self.sistema, self.nombreMesa, tk.Toplevel(self))

	def datosCierre(self):
		"""
		Accion para el boton "Cierre de Caja", nos pide los datos de cierre de caja y hacer la acción
		"""
		CierreGUI(self.sistema, tk.Toplevel(self), self)		

	def withdraw(self):
		self.master.withdraw()

	def abrirVentana(self):
		self.master.update()
		self.master.deiconify()

	def onCloseWindow(self):
		del self.sistema
		self.master.destroy()
		
class ClientesGUI(tk.Frame):
	"""
	En esta ventana se verán todas las acciones relacionados con la base de datos de los clientes.
	"""
	def __init__(self, sistema, master=None, padre=None):
		tk.Frame.__init__(self, master)		
		self.padre = padre
		self.sistema = sistema
		self.padre.withdraw()
		self.master.wm_title("Clientes")
		self.master.geometry("400x130")
		self.pack()
		self.createWidgets()
		self.master.protocol("WM_DELETE_WINDOW", self.showMain)

	def createWidgets(self):
		self.id = tk.StringVar()
		self.nick = tk.StringVar()
		self.correo = tk.StringVar()
		self.nombre = tk.StringVar()
		self.visitas = tk.StringVar()
		self.ultimaVisita = tk.StringVar()
		self.consumo = tk.StringVar()
		self.fechaIngreso = tk.StringVar()

		#Sección de la izquierda
		tk.Label(self.master, text="ID: ").place(x=30, y=10)
		tk.Entry(self.master, width=30, textvariable=self.id).place(x=60, y=10)
		tk.Label(self.master, text="Nick: ").place(x=20, y=30)
		tk.Entry(self.master, width=30, textvariable=self.nick).place(x=60, y=30)
		tk.Label(self.master, text="Correo: ").place(x=10, y=50)
		tk.Entry(self.master, width=30, textvariable=self.correo).place(x=60, y=50)
		tk.Label(self.master, text="Nombre: ").place(x=3, y=70)
		tk.Entry(self.master, width=30, textvariable=self.nombre).place(x=60, y=70)

		#Sección de la derecha
		tk.Label(self.master, text="Visitas: ").place(x=280, y=10)
		tk.Label(self.master, textvariable=self.visitas, bd=1).place(x=330, y=10)
		tk.Label(self.master, text="Ultima Visita: ").place(x=250, y=30)
		tk.Label(self.master, textvariable=self.ultimaVisita).place(x=330, y=30)
		tk.Label(self.master, text="Consumo:").place(x=265, y=50)
		tk.Label(self.master, textvariable=self.consumo).place(x=330, y=50)
		tk.Label(self.master, text="Ingreso:").place(x=275, y=70)
		tk.Label(self.master, textvariable=self.fechaIngreso).place(x=330, y=70)

		#Sección de abajo
		tk.Button(self.master, text="Buscar", command=self.busqueda).place(x=10, y=100)
		tk.Button(self.master, text="Insertar", command=self.insertar).place(x=65, y=100)
		tk.Button(self.master, text="Borrar", command=self.borrar).place(x=125, y=100)
		tk.Button(self.master, text="Actualizar", command=self.actualizar).place(x=180, y=100)
		tk.Button(self.master, text="Limpiar Campos", command=self.cls).place(x=270, y=100)
		

	def busqueda(self, identificador=""):
		"""
		Función para el botón de Buscar que funciona de la siguiente manera:
		En esta función si se envía como argumento el identificador se utilizará este ID
		para hacer la busqueda. De no ser así se hará el busqueda con la siguiente jerarquía:
			id -> nick -> correo -> nombre
		Es decir que si no se tiene escrito el id en su campo se buscará por nick y así sucesivamente.
		"""
		try:
			if identificador:
				query = self.sistema.clientesDB.buscarID(identificador)
			elif self.id.get():
				query = self.sistema.clientesDB.buscarID(self.id.get())
			elif self.nick.get():
				query = self.sistema.clientesDB.buscarNick(self.nick.get())
			elif self.correo.get():
				query = self.sistema.clientesDB.buscarCorreo(self.correo.get())
			elif self.nombre.get():
				query = self.sistema.clientesDB.buscarNombre(self.nombre.get())
			else:
				mb.showinfo("Error", "No se ingresaron datos", parent=self.master)
				return
		except:
			mb.showinfo(sys.exc_info()[0])
			return
		self.id.set(query.id)
		self.nick.set(query.nick)
		self.correo.set(query.correo)
		self.nombre.set(query.nombre)
		self.visitas.set(query.visitas)
		self.ultimaVisita.set(query.ultimaVisita)
		self.consumo.set(query.consumo)
		self.fechaIngreso.set(query.fechaIngreso)

	def insertar(self):
		"""
		Función para el botón de insertar que funciona de la siguiente manera:
		Se ingresará nick, correo y/o nombre, con esto se creará un nuevo cliente con un nuevo ID.
		"""
		if self.nombre.get() == "" and self.nick.get() == "" and self.correo.get() == "":
			mb.showinfo("Warning", "¡No se agregó ningún dato!", parent=self.master)
			return

		answer = mb.askquestion("Insertar", "¿Son correctos los datos?", icon="warning", parent=self.master)
		if answer == "yes":
			try:
				self.sistema.clientesDB.insertar(nombre=self.nombre.get(), correo=self.correo.get(), nick=self.nick.get())
				self.sistema.clientesDB.confirmar()
			except:
				mb.showinfo(sys.exc_info()[0])
				return
			self.busqueda(len(self.sistema.clientesDB))

	def borrar(self):
		"""
		Función para el botón de borrar que funciona de la siguiente manera:
		Se ingresará únicamente el ID, lo demás será ignorado. Se borrará el cliente con este ID.
		"""
		if self.id.get() == "":
			mb.showinfo("Advertencia", "¡Se debe ingresar un ID!", parent=self.master)
			return
		self.busqueda(self.id.get())
		if self.id.get() == "¡ERROR! No se encontró información":
			mb.showinfo("¡Error!", "No se encontraron coincidencias. No se continuará con el proceso.", parent=self.master)
			self.cls()
			return
		answer = mb.askquestion("Borrar", "Los datos se perderán permanentemente. Favor de revisar.", parent=self.master)
		if answer == "yes":
			try:
				self.sistema.clientesDB.borrar(self.id.get())
				self.sistema.clientesDB.confirmar()
			except:
				mb.showinfo(sys.exc_info()[0])
				return
			self.cls()

	def actualizar(self):
		"""
		Función para el botón que actualiza los datos de la siguiente manera:
		Se ingresa el ID (el cliente con este ID será modificado) y se ingresa solamente los datos que se quieran
		cambiar. Una vez hecho esto al dar click en Actualizar se nos mostrará los cambios que se harán y nos
		preguntará si es correcto.
		"""
		#Primero vemos que exista el ID
		if self.id.get() == "":
			mb.showinfo("Advertencia", "¡Se debe ingresar un ID!", parent=self.master)
			return
		#No tiene caso hacer nada si ningún valor se ha introducido
		if self.nick.get() == nick or self.nombre.get() == nombre or self.correo.get() == correo:
			mb.showinfo("Advertencia", "Todos los datos son iguales. ¡No se cambió nada!", parent=self.master)
			return
		#Variables auxiliares que son los nuevos valores potenciales
		nick = self.nick.get().strip()
		nombre = self.nombre.get().strip()
		correo = self.correo.get().strip()
		#Se hace una busqueda para poder mostrar los valores originales
		self.busqueda(self.id.get())
		#Si no se encontró el ID se nos indicará
		if self.id.get() == "¡ERROR! No se encontró información":
			mb.showinfo("¡Error!", "No se encontraron coincidencias. No se continuará con el proceso.", parent=self.master)
			self.cls()
			return
		#Para cada valor potencial, si tiene escrito algo se escribirá en el campo de la siguiente manera: {ORIGNAL} -> {NUEVO}
		if nick:
			self.nick.set(self.nick.get() + " -> " + nick)
		if nombre:
			self.nombre.set(self.nombre.get() + " -> " + nombre)
		if correo:
			self.correo.set(self.correo.get() + " -> " + correo)
		#Se nos preguntará si continuamos con el proceso
		answer = mb.askquestion("Actualizar", "¿Son correctos los datos a actualizar?")
		if answer == "yes":
			try:#Puede que la base de datos estuviera bloqueada
				self.sistema.clientesDB.actualizar(self.id.get(), nombre=nombre, nick=nick, correo=correo)
				self.sistema.clientesDB.confirmar()
			except:
				mb.showinfo(sys.exc_info()[0])
				return
			self.busqueda(self.id.get())
		else:
			self.nick.set(nick)
			self.nombre.set(nombre)
			self.correo.set(correo)

	def cls(self):
		self.id.set("")
		self.nick.set("")
		self.correo.set("")
		self.nombre.set("")
		self.visitas.set("")
		self.ultimaVisita.set("")
		self.consumo.set("")
		self.fechaIngreso.set("")

	def showMain(self):
		"""
		Se retorna a la ventana padre.
		"""
		self.padre.abrirVentana()
		self.master.destroy()




if __name__ == '__main__':
	root = tk.Tk()
	app = Instanciador(master=root)
	root.protocol("WM_DELETE_WINDOW", app.onCloseWindow)
	app.mainloop()
