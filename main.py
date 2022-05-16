from flask import Flask,render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import io

app=Flask(__name__)


#(2i4,1x,a2,1x,i1,4f10.3,4f8.3)
def get_masses():
    widths = [(1, 4), (5, 8), (9, 11), (12, 13),
              (14, 23), (24, 33), (34, 43), (44, 53),
              (54, 61), (62, 69), (70, 77), (78, -1)]
    df = pd.read_fwf('mass.dat', colspecs=widths)
    df.dropna(subset=["Mexp"], inplace=True)
    return df

@app.route('/masses.png')
def masses_png():
    df = get_masses()
    fig = df.plot(kind="scatter", x='Z', y="A", s=10, c="Mexp", colormap="viridis").get_figure()
    output = io.BytesIO()
    fig.savefig(output, format="png")
    return output.getvalue(), 200, {"Content-Type": "image/png"}


@app.route('/masses/<int:z>.png')
def masses_z(z):
    df = get_masses()
    df = df[df["Z"] == z]
    fig = df.plot(kind="scatter", x='A', y="Mexp").get_figure()
    output = io.BytesIO()
    fig.savefig(output, format="png")
    return output.getvalue(), 200, {"Content-Type": "image/png"}



@app.route('/')
def index():
    df = get_masses()
    return render_template("index.html", title= "Mass Hesaplama", masses = df.to_html())

if __name__=='__main__':
    app.run()



