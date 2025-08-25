"""
Emotion Detection Module - IBM Watson AI Engine
"""

import json
import requests

def emotion_detector(text_to_analyse):
    """Emotion Detector using IBM Watson Emotion API
    """
    # Define the URL for the emotion detection API
    base_url = 'https://sn-watson-emotion.labs.skills.network/v1/'
    endpoint = 'watson.runtime.nlp.v1/NlpService/EmotionPredict'
    url = base_url + endpoint

    # Create the payload with the text to be analyzed
    myobj = { "raw_document": { "text": text_to_analyse } }

    # Set the headers with the required model ID for the API
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # # Checking for empty input/white spaces
    # if (text_to_analyse is None) or (not text_to_analyse.strip()):
    #     return {'input error': 'Please enter valid text, not empty or whitespace'}

    # Make a POST request to the API with the payload and headers
    try:
        response = requests.post(url, json=myobj, headers=header, timeout=20)
    except requests.exceptions.Timeout:
        return {'error': 'The request timed out!'}
    except requests.exceptions.RequestException as e:
        return {'error': f'An error occurred: {e}'}

    # If the response status code is 200
    if 200 <= response.status_code < 300:
        # Parse the response from the API
        formatted_response = json.loads(response.text)
        emotion_scores = formatted_response['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        return_response = {
                            'anger': emotion_scores['anger'],
                            'disgust': emotion_scores['disgust'],
                            'fear': emotion_scores['fear'],
                            'joy': emotion_scores['joy'],
                            'sadness': emotion_scores['sadness'],
                            'dominant_emotion': dominant_emotion
                            }
    # If the response status code is 400
    elif 400 <= response.status_code < 500:
        emotion_scores = {'anger':1, 'disgust':1, 'fear':1, 'joy':1, 'sadness':1}
        return_response = {key: None for key in emotion_scores}
        return_response['dominant_emotion'] = None
    elif 500 <= response.status_code < 600:
        return_response = {'message': f"Server error '{response.status_code}' please try again"}
    else:
        return_response = {'message': f"Server response '{response.status_code}' {response.text}"}

    # Return response
    return return_response
