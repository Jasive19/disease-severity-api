import os
import cv2
import urllib
import numpy as np
from tensorflow.keras.models import load_model
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .apps import *
from rest_framework.decorators import api_view

class Welcome:
    @api_view(['GET'])
    def home(self):
        return Response("Welcome!!")

class LoadModel:

    def predictH5(request):
        NAME_MODEL = 'covid_model.h5'
        LABEL = ["COVID", "NEUMONIA VIRAL", "NORMAL", "TUBERCULOSIS"]
        url = request.data.get('url', False)
        
        if not url:
            return LoadModel.requiredParams()

        image = LoadModel.processImage(url)
        MODEL_FILE = os.path.join(settings.MODELS, NAME_MODEL)
        model = load_model(MODEL_FILE)

        # Predice el resultado
        model_pred = model.predict(image)
        probability = model_pred[0].flatten()

        maximo = max(probability)
        position = list(probability).index(maximo)
        severity = LABEL[position]
        percent_predict = str('%.2f' % (maximo*100))

        LoadModel.debug(maximo, model_pred, probability)
        options = ''
        for index, item in enumerate(probability):
            # if position != index:
            options += str('%.2f' % (item*100)) + ','

        options = options[:-1]
        return {
            'result': severity,
            'url': url,
            'percent': percent_predict,
            'options': options,
        }

    def processImage(url):
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        image = cv2.imdecode(arr, -1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = np.array(image) / 255
        image = np.expand_dims(image, axis=0)
        return image

    def validateUrl(self, url):
        validate = URLValidator(verify_exists=False)
        try:
            validate(url)
        except ValidationError:
            return Response({'success': False, 'message': 'La url proporcionada no es válida'})

        return False

    def requiredParams():
        return Response({
            'success': False,
            'message': 'Faltan parámetros para procesar el resultado',
            'validParameters': [
                {'name': 'url', 'type': 'string/text'},
                {'name': 'picture', 'type': 'file'}],
        })

    
    def debug(*args):
        print("**********************DEBUG***************************")
        print("-------------- MAXIMO ---------------")
        print(args[0])
        print("----------------  --------------------")
        print("---------- MODEL PREDIC ---------------")
        print(args[1])
        print("----------------  --------------------")
        print("----------------  --------------------")
        print("-----------  PROBABILITY  ----------------")
        print(args[2])
        print("----------------  --------------------")
        print("----------------  --------------------")
        print("**********************DEBUG***************************")
