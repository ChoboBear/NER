from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys
import stanza
#stanza.download('ru')
def udalit_povtor(x):
        x = x.split(',')
        x.sort()
        a = set(x)
        x = list(a)
        long = len(x)
        text = ''
        for i in range(1,len(x)):
            text += x[i] + ',\n'
        return text, long
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('kursich.ui', self)
        self.comp_btn.clicked.connect(self.complete_fnc) 
        self.create_btn.clicked.connect(self.create_fnc)
        self.load_btn.clicked.connect(self.load_fnc)
   
    def load_fnc(self):
        fname = QFileDialog.getOpenFileName(self)[0]
        f = open(fname,'r',errors='ignore').read()
        f = f.encode('cp1251').decode('utf-8','ignore')
        self.usual_text.setText(f)
        
    def complete_fnc(self):
        try:
            line = self.usual_text.toPlainText()
            nlp = stanza.Pipeline(lang='ru', processors='tokenize,ner')
            doc = nlp(line)
            per_att = ''
            loc_att = ''
            org_att = ''
            misc_att = ''
            for sent in doc.sentences:
                for ent in sent.ents:
                    if ent.type == 'PER':
                        per_att += ent.text + ','
                    elif ent.type == 'LOC':
                        loc_att += ent.text + ','
                    elif ent.type == 'ORG':
                        org_att += ent.text + ','
                    elif ent.type == 'MISC':
                        misc_att += ent.text + ','
        
            self.per_text.setText(f'{udalit_povtor(per_att)[0]}\t')
            self.loc_text.setText(f'{udalit_povtor(loc_att)[0]}\t')
            self.org_text.setText(f'{udalit_povtor(org_att)[0]}\t')
            self.misc_text.setText(f'{udalit_povtor(misc_att)[0]}\t')

            self.per_amm.setText(str(udalit_povtor(per_att)[1]-1))
            self.loc_amm.setText(str(udalit_povtor(loc_att)[1]-1))
            self.org_amm.setText(str(udalit_povtor(org_att)[1]-1))
            self.misc_amm.setText(str(udalit_povtor(misc_att)[1]-1))
        except:
            ex1 = App_mistake()
            ex1.show()
          
    def create_fnc(self):
        text = "Location;Person;Organization;Other\n"
        
        location = (self.loc_text.toPlainText()).split(',\n')
        person = (self.per_text.toPlainText()).split(',\n')
        organization = (self.org_text.toPlainText()).split(',\n')
        miscelanous = (self.misc_text.toPlainText()).split(',\n')
        all = []
        all.append(location)
        all.append(person)
        all.append(organization)
        all.append(miscelanous)
        for i in all:
            if i == max(all, key= len):
                for i2 in all:
                    for i3 in range(len(i)-len(i2)):
                        i2.append(' ')
                for i1 in range(len(i)):
                    text+= f"{all[0][i1]};{all[1][i1]};{all[2][i1]};{all[3][i1]}\n"
        file = open("gotovo.csv", "w", encoding='cp1251', errors = 'ignore')
        file.write(text)
        file.close

class App_mistake(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('kursss_okno.ui', self)
     
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
