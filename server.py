''' Executing this function initiates the application of emotion
    detection to be executed over the Flask channel and deployed on
    localhost:5000.
'''
# Import Flask, render_template, request from the flask pramework package
# Import the emotion detector function from the package created
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

#Initiate the flask app
app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotional_detector():
    ''' This function detects emotion using Watson AI API'''
    # Retrieve the text to analyze from the request arguments
    # Check if its valid
    text_to_analyze = request.args.get('textToAnalyze')
    # if not text_to_analyze:
    #     return "Please try enter something. It's fun!!"

    # Pass the text to the emotion_detector function and store the response
    emotional_response = emotion_detector(text_to_analyze)

    # Extract the dominant_emotionfrom the response
    # Check if the isSuccess is None, indicating an error or invalid input
    is_error = emotional_response.get('message')
    if is_error:
        return is_error

    # Alternative Approach
    # is_400 = emotional_response.get('dominant_emotion')
    # if is_400 is None:
    #     return "<b>Invalid text! Please try again!</b>"

    # Format the emotional response
    output = (
        f"For the given statement, the system response is "
        f"'anger': {emotional_response['anger']}, "
        f"'disgust': {emotional_response['disgust']}, "
        f"'fear': {emotional_response['fear']}, "
        f"'joy': {emotional_response['joy']} and "
        f"'sadness': {emotional_response['sadness']}. "
        f"The dominant emotion is {emotional_response['dominant_emotion']}."
    )
    return output

@app.route("/")
def render_index_page():
    ''' This function initiates the rendering of the main application
        page over the Flask channel
    '''
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
