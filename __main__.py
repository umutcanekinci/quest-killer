#!/usr/bin/env python3

try:

	import sys
	from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
	from PyQt5 import QtCore, QtGui
	from PyQt5.Qt import Qt
	from hashlib import md5
	from mysql.connector import *
	from mysql.connector import errorcode
	from settings import *
	from gui.LoginWindowGUI import Ui_LoginWindow
	from gui.MainWindowGUI import Ui_MainWindow

except ImportError and AttributeError as Err:
	
	App = QApplication(sys.argv)
	Message = QMessageBox()
	Message.setIcon(QMessageBox.Critical)
	Message.setWindowTitle("Import Error")
	Message.setText("Cannot import packages. Plese contact to author.\nmuetnmuetn@gmail.com\n\nImport Error:")
	Message.addButton("Exit", QMessageBox.ActionRole).clicked.connect(sys.exit)
	try: Message.setInformativeText(str(Err))
	except: pass
	Message.exec_()
	sys.exit(App.exec_())

class MainWindow(QMainWindow, Ui_MainWindow):

	def __init__(self, parent=None):

		super(MainWindow, self).__init__(parent)
		self.setupUi(self)

class LoginWindow(QMainWindow, Ui_LoginWindow):

	def __init__(self, parent=None):

		super(LoginWindow, self).__init__(parent)
		self.setupUi(self)
		
		self.MainWin = MainWindow()
		self.MainWin.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
		
		self.LoginButton.clicked.connect(self.Login)
		self.RegisterButton.clicked.connect(self.Register)
		self.ExitButton.mousePressEvent = self.Exit

	def keyPressEvent(self, Event):

		if Event.key() == Qt.Key_Escape:
			self.Exit()
		elif Event.key() == Qt.Key_Tab:
			self.Active(None)

	def Sql(self, SQL, Fetch="One", TryAgainFunc=None):

		try:
			Connection = connect(**DbConfig)
			Cursor = Connection.cursor()
			Data = Cursor.execute(SQL)
			#if Data == None: return None
			return Cursor.fetchone() if Fetch == "One" else Cursor.fetchall()
			
		except Error as Err:

			Message = QMessageBox()
			Message.setIcon(QMessageBox.Critical)
			Message.setWindowTitle("MySQL Error")
			Message.setText("Cannot connect to database. Plese contact to author.\nmuetnmuetn@gmail.com\nMySQL error:")
			Message.addButton("Exit", QMessageBox.ActionRole).clicked.connect(self.Exit)
			Message.addButton("Try Again", Message.ActionRole).clicked.connect(TryAgainFunc)
			Message.addButton(QMessageBox.Ok).clicked.connect(Message.close)
			if Err.errno == errorcode.ER_ACCESS_DENIED_ERROR: Message.setInformativeText("Something is wrong with database username or database password !")
			elif Err.errno == errorcode.ER_BAD_DB_ERROR: Message.setInformativeText("Database does not exist !")
			else:
				try: Message.setInformativeText(Err)
				except: pass
			Message.exec_()
			#if Connection.is_connected(): Connection.rollback()

	def Info(self, Message, Color="orange"):

		if self.Menu.currentIndex() == 0:
			self.LoginInfoLabel.setStyleSheet("background-color: "+Color+"; color: white;")
			self.LoginInfoLabel.setText(Message)
		elif self.Menu.currentIndex() == 1:
			self.RegisterInfoLabel.setStyleSheet("background-color: "+Color+"; color: white;")
			self.RegisterInfoLabel.setText(Message)
		
	def Login(self):
		
		self.LoginInfoLabel.setText("")
		Username = self.LoginUsernameInput.text()
		Password = self.LoginPasswordInput.text()

		# my free database provider became too pricy so i cant connect it anymore
		"""
		User = self.Sql("SELECT * FROM users WHERE name='"+Username+"' or email='"+Username+"'", TryAgainFunc=self.Login)
		
		if Username == "" or Password == "": self.Info("Please fill all blanks !")
		elif len(Username) == 1: self.Info("Username is very short !")
		elif len(Password) < 8: self.Info("Password is very short !")
		elif User == None: self.Info("User not found !")
		elif User[-1] != 1: self.Info("User is blocked !", "red")
		elif User[2] != md5(Password.encode("utf-8")).hexdigest(): self.Info("Password is not correct !",)

		else:
		"""		
		
		self.MainWin.show()
		
	def Register(self):

		self.RegisterInfoLabel.setText("")
		Username = self.RegisterUsernameInput.text()
		Password = self.RegisterPasswordInput.text()
		Email = self.RegisterEmailInput.text()
		School = self.RegisterSchoolCombobox.currentText()
		Class = self.RegisterClassCombobox.currentText()
		Rank = 1 if self.RegisterJobCombobox.currentText() == "Student" else 2
		
		if Username == "" or Password == "" or Email == "": self.Info("Please fill all blanks !")
		elif len(Username) == 1: self.Info("Username is very short !")
		elif len(Password) < 8: self.Info("Password is very short !")
		elif len(Email) < 7 or "@" not in Email[1:-4] or Email[-4:] != ".com" or Email[-5] == "@": self.Info("Email is invalid !")
		else:
			Password = md5(Password.encode("utf-8")).hexdigest()

			try:
				
				# my free database provider became too pricy so i cant connect it anymore
				
				"""
				self.Connect(self.Login)
				self.Cursor.execute("SELECT * FROM users WHERE name='"+Username+"'")

				for User in self.Cursor:
					self.Info("A user with this username already exists !")
				else:
					self.Cursor.execute("SELECT * FROM users WHERE email='"+Email+"'")
					
					for User in self.Cursor:
						self.Info("A user with this email already exists !")
					else:
						self.Cursor.execute("INSERT INTO users(name, password, email, education, rank) VALUES('"+Username+"', '"+Password+"', '"+Email+"', '"+School+"---"+Class+"', "+str(Rank)+")")
						self.Connection.commit()
						self.Info("Registered successfuly ! You can login now.", "green")
						self.Menu.setCurrentWidget(self.LoginTab)
						self.Info("Registered successfuly ! You can login now.", "green")
				self.Disconnect()
				"""
			except Error as Err:
				
				self.MysqlError(Err)

	def Exit(self, event):
		self.close()
		sys.exit()
		
if __name__ == "__main__":

	App = QApplication(sys.argv)
	LoginWin = LoginWindow()
	LoginWin.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
	LoginWin.show()
	sys.exit(App.exec_())
