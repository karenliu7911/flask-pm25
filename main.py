from flask import Flask, render_template, jsonify
import database

app = Flask(__name__)


# 取得某縣市的資料
@app.route("/api/data/<county>")  # <參數>
def api_data_by_county(county):
    rows = database.get_data_by_county(county)["rows"]
    return jsonify(rows)


# 取得全部縣市的名稱(不重複)
@app.route("/api/counties")
def api_counties():
    counties = database.get_counties()["rows"]
    counties = [c[0] for c in counties]  # 只需要第1行(0位置)的值

    return jsonify(counties)


@app.route("/")
def index():

    result = database.get_latest_data()
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
