from flask import Flask
from flask import request
from flask import redirect
from flask import render_template_string
import serial

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html lang="en">
<body>
    <h1>Enter some text</h1>
    <form action="." method="POST">
        <input style="margin:1em; border:2px solid #ffc600; font-size:4em; border-radius:10px; padding:.25em;" type="text" name="text">
        <input style="height:50px;" type="submit" name="my-form" value="Send">
    </form>
</body>
</html>
"""

arduino = serial.Serial('/dev/ttyUSB0', 9600)

@app.route('/')
def my_form():
        return render_template_string(html)

@app.route('/', methods=['POST'])
def my_form_post():

    # clear display
    arduino.write(b'\x0C')
    # write user input string
    text = request.form['text']
    processed_text = text[:40]
    arduino.write(bytearray(str(processed_text)))

    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
