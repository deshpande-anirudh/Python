from flask import jsonify, Flask, request, redirect
from datetime import datetime, timedelta, UTC

from api.url_shortner.sha256_utils import sha256_message
from api.url_shortner import base62_utils

short_url_store = {}

app = Flask("__name__")

"""
{
    "url": "https://www.example.com/sfsdfsdd/wewqe?key=sdsdsd",
    "expiration_time": 1212343121221,
    "user_id": "qwsdfdswedsdsf",
    "custom_alias": "sdsasdawe"
}
"""
@app.route("/v1/short_url", methods=["POST"])
def create_short_url():
    data = request.get_json()
    sha256_url = sha256_message(data["url"]) # 64 characters

    cur_time = datetime.now(UTC)
    future_date = cur_time + timedelta(days = 5*365)
    expiration_time = data["expiration_time"] or future_date.timestamp()

    start = 0
    short_url_key = ''

    while start <= 50:
        cur_key = sha256_url[start: start +  10]
        print(cur_key)
        cur_key_base_62 = base62_utils.base62_encode(cur_key)
        if cur_key_base_62 not in short_url_store:
            short_url_store[cur_key_base_62] = {
                "long_url": data["url"],
                "user_id": data["user_id"],
                "expires_at": data["expiration_time"] or expiration_time,
            }
            short_url_key = cur_key_base_62
            break

        start += 10

    print(short_url_store)

    return jsonify({
        "short_url": short_url_key,
        "expiration_time": expiration_time
    }), 201

@app.route("/v1/short_url/<key>", methods=["GET"])
def get_long_url(key):
    print(short_url_store)
    if key in short_url_store:
        return redirect(short_url_store[key]["long_url"], code=302)

    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
