import sys
import time
import threading
from PyQt5.QtWidgets import *

class interface(QWidget):
    def __init__(self):
        super().__init__()
        self.init_Interface()

    def init_Interface(self):
        case1 = QRadioButton("Transferer tous les fichiers", self)
        case2 = QRadioButton("Recevoir tous les fichiers", self)
        case3 = QRadioButton("Remplacer les fichiers les plus vieux", self)

        self.button1 = QPushButton("Application")
        self.button1.clicked.connect(self.startProgressBar)
        self.button1.setEnabled(False)
        self.button2 = QPushButton("Se connecter")
        self.button2.clicked.connect(self.conectedToServer)
        self.button3 = QPushButton("Se deconnecter")
        self.button3.clicked.connect(self.disconectedToServer)
        self.button3.setEnabled(False)

        label1 = QLabel("Connection au serveur")
        self.label2 = QLabel("Recherche de connection")
        label3 = QLabel("Avance du transfert:")

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progress_bar_value=0
        self.progressBar.setValue(self.progress_bar_value)


        grille = QGridLayout()
        self.setLayout(grille)
        grille.addWidget(case1, 1,1)
        grille.addWidget(case2, 2,1)
        grille.addWidget(self.button2, 1,2)
        grille.addWidget(self.button3, 2,2)
        grille.addWidget(case3, 3,1)
        grille.addWidget(self.button1, 4,1)
        grille.addWidget(label1, 5, 1)
        grille.addWidget(self.label2, 6, 1)
        grille.addWidget(label3, 7, 1)
        grille.addWidget(self.progressBar, 8, 1)

        self.setGeometry(300,300,250,250)

        self.show()
    def conectedToServer(self):
        self.button1.setEnabled(True)
        self.button3.setEnabled(True)
        self.button2.setEnabled(False)
        self.label2.setText("connecte")
    def disconectedToServer(self):
        self.button1.setEnabled(False)
        self.button3.setEnabled(False)
        self.button2.setEnabled(True)
        self.label2.setText("connection perdu")

    def startProgressBar(self):
        threading.Thread(target=self.__startProgressBar).start()
    def __startProgressBar(self):
        print("e")
        count = 0
        while count < 100:
            count+=1
            time.sleep(0.1)
            self.progress_bar_value = count
            self.progressBar.setValue(self.progress_bar_value)




menu=QApplication(sys.argv)
a=interface()
sys.exit(menu.exec_())#comme le mainloop