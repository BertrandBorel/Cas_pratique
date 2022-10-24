'''Application : Vérifier l'uniforme

Objectif : 
Vérifier si l'utilisateur porte bien un gilet et un casque. 
L'application confirme par message si les conditions sont remplies ou non.
_____________________________________________________________________________'''


# Importations nécessaires : 
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes 
import av
import cv2
import torch
import numpy as np
import time
import streamlit as st


# importation du modèle yolov5 
model_yolo = torch.hub.load('ultralytics/yolov5', 'custom', path='Models/batch_40_300/last.pt', force_reload=False)


# Liste contenant les labels
Label = ['Casque','Gilet','NO CASQUE','NO GILET']
# respectivement : [0, 1, 2, 3]


font = cv2.FONT_HERSHEY_PLAIN

colors = np.random.uniform(0, 255, size=(2, 3))
classid = 0

# seuil du modèle :
CONFIDENCE_THRESHOLD = 0.8

# titre principal
st.title("Vérification de l'uniforme")

# liste vide, par la suite contiendra les labels
number=[]


class VideoProcessor:

    def recv(self, frame):
 
        frm = frame.to_ndarray(format="bgr24")
        
        boxes = []
        class_ids = []
        results = model_yolo(frm)


        for i in range(0,len(results.pred[0])) :
            if results.pred[0][i,4] > CONFIDENCE_THRESHOLD :
                x = int(results.pred[0][i,0])
                y = int(results.pred[0][i,1])
                w = int(results.pred[0][i,2])
                h = int(results.pred[0][i,3])
                box = np.array([x, y, w, h])
                boxes.append(box)
                class_ids.append(int(results.pred[0][i,5]))

        for box, classid in zip(boxes,class_ids):
            color = colors[int(classid) % len(colors)]
            cv2.rectangle(frm, box, color, 2)
            cv2.rectangle(frm, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
            cv2.putText(frm, Label[classid], (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))

            number.append(Label[classid])

            # récupération du dernier label
            classe = number[-1]
            
            # condition pour la création du message
            if classe == "NO CASQUE" or classe == "NO GILET" :
                msg = "Uniforme incomplet"
                print(msg)
            else : 
                msg = "Uniforme complet"
                print(msg)

            # Ecriture du message dans un fichier 'txt'    
            with open('file.txt', 'w') as file:
                file.write(msg)            

        return av.VideoFrame.from_ndarray(frm, format='bgr24')

# possibilité de mute
muted = st.checkbox("Mute")



webrtc_streamer( key="mute_sample", 
                video_processor_factory=VideoProcessor,
                video_html_attrs=VideoHTMLAttributes( autoPlay=True, controls=True, style={"width": "100%"}, muted=muted ), ) 

 

# bouton = affiche le texte
button = st.button('Lancer la détection :')
button_placeholder = st.empty()
time.sleep(2)
button = False
button_placeholder.write(f'**Résultat :**')

# variable vide qui accueille le texte
texte = st.empty()

# ouverture du fichier, affichage du texte
while True :
    with open('file.txt') as f:
        first_line = f.readline()
        texte.write(first_line)
        time.sleep(5)