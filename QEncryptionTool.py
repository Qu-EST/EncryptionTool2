import os
#os.chdir(r'C:\Users\jee11\Documents\new_28-4\EncryptionTool\QuestProject ')
#print(os.getcwd())

from UI.EncryptionUI import EncryptionUI
import EncryptorData
all_data=EncryptorData.EncryptorData()
ui=EncryptionUI()
all_data.ui=ui
ui.mainloop()