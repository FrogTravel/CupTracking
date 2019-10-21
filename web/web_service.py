from flask import Flask, render_template
import os
app = Flask(__name__, template_folder='templates')

@app.route('/appeared')
def appeared():
    images = os.listdir(os.path.join(app.static_folder, "appeared"))
    images.reverse()
    return render_template('img_temp_app.html', images=images)

@app.route('/disappeared')
def disappeared():
    images = os.listdir(os.path.join(app.static_folder, "disappeared"))
    images.reverse()
    return render_template('img_temp_dis.html', images=images)

if __name__ == '__main__':

   app.run()