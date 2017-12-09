"""
One Page Flask
usage:
pip install flask
python3 app.py
http://127.0.0.1:5000/
"""
from flask import Flask, send_from_directory, json
from string import Template

app = Flask(__name__)
MINI = False

@app.route('/')
def ix():

    template = ""

    if MINI:

        template = MINI_TEMPLATE
        content = """
        <p>
        This is a barebones web application made with Flask and featuring a minimal 
        layout inplementing the Bulma CSS framework. Everything is included in one python file. 
        This makes for a basic starter Flask app for trying out some new CSS or javascript, but
        not so good for larger projects where you should divide the 
        code into multiple files, libraries, static files, etc..
        </p>
    
        <h2 class="is-2">Wait, there's more</h2>
        <p>
        Yes this minimal page is quite boring, so I built a second template that has a little
        more going on. To see that one, change the parameter in the app.py file 
        from MINI=True to MINI=False.
        Whereas this minimal version includes the HTML in a string in the python file, 
        the Maxi version loads a template from an external HTML file.
        </p>
    
        """

    else:
        # Maxi template is external html file
        content = """
        Here we have a Flask program in two files, one page of Python code 
        plus an HTML template. 
        The template file implements the Bulma CSS framework. See the Bulma documentation,
        it should be easy to understand.
        """
      
        # Read the maxi template file into a string
        with open('maxi.html', 'r') as template_file:
            template = template_file.read().replace('\n', '')

    placeholders = init_placeholders()
    # merge page specifics
    placeholders.update({
          "TITLE": "Home - One Page Flask", 
          "CONTENT_TITLE": "Home",
          "HOME_ACTIVE": "active",
          "CONTENT": content
          })

    html = build_page(template, placeholders)
    return html


@app.route('/sizes')
def sizes():
  
    template = MINI_TEMPLATE
    sizes = get_sizes()

    content = '<p>This page demonstrates a Flask route that does some data processing to build an html fragment that is displayed dynaically.</p>'
    content += '<ul>\n'
    for size in sizes:
        content += '<li>' + size + '</li>\n'
    content += '</ul>\n'

    content += '<h2 class="is-2">Raw JSON sizes</h2>'
    content += '<pre>' + str(sizes) + '</pre>'

    placeholders = init_placeholders()
    placeholders.update({
          "TITLE": "Sizes - Flasker", 
          "CONTENT_TITLE": "Sizes",
          "SIZES_ACTIVE": "active",
          "CONTENT": content
          })

    html = build_page(template, placeholders)
    return html


@app.route('/sizes_json')
def summary():
    """ No template, just return JSON """
    data = get_sizes()
    response = app.response_class(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    return response


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory("assets", filename)


def get_sizes():
    sizes = ['small', 'medium', 'large']
    return sizes


def init_placeholders():
    """ ohno Template barfs on missing placeholders """
    return {
        "HOME_ACTIVE": "",
        "SIZES_ACTIVE": "",
        "JSON_ACTIVE": "",
         }


def build_page(template_name, dic):
    html = Template(template_name).substitute(dic)
    return html


MINI_TEMPLATE = """<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="/assets/img/num1.jpg">
  <title>$TITLE</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.6.1/css/bulma.min.css">
  <style>
    .active {
      font-weight: 800;
    }
  </style>
</head>

<body>
  <section class="hero is-info">
    <div class="hero-head">
      <nav class="navbar">
        <div class="container">
          <div class="navbar-brand">
            <a class="navbar-item" href="/">
              <h1 class="title is-6">
                <span class="icon  has-text-info">
                  <i class="fa fa-file-o"></i>
                </span>
                ONE PAGE FLASK
              </h1>
            </a>
            <span class="navbar-burger burger" data-target="navbarMenuHeroA">
            <span></span>
            <span></span>
            <span></span>
            </span>
          </div>
          <div id="navbarMenuHeroA" class="navbar-menu">
            <div class="navbar-end">
              <a class="navbar-item $SIZES_ACTIVE" href="/sizes">
                Sizes
              </a>
              <a class="navbar-item" href="/sizes_json">
                JSON Sizes
              </a>
            </div>
          </div>
        </div>
      </nav>
    </div>

    <!-- Hero content: will be in the middle -->
    <div class="hero-body">
      <div class="container has-text-centered">
        <h1 class="title">
        Hello
      </h1>
        <h2 class="subtitle">
        A one page Flask and Bulma page
      </h2>
      </div>
    </div>
  </section>

  <section>
    <div class="container >
      <div class="columns">
        <div class="column is-2"></div>

        <div class="column">
          <div class="content">
            <h1>$CONTENT_TITLE</h1>
          </div>
          <div class="content">
            $CONTENT
          </div>
        </div>
        <div class="column is-2"></div>
      </div>
    </div>
  </section>

</body>
</html>
"""


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


