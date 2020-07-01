from app import utils
import flask
import os

HEALTH_API = flask.Blueprint(f"API_{os.environ.get('VERSION')}_HEALTH_OPS", __name__ )

@HEALTH_API.route('/acknowledge_health', methods=["POST"])
def acknowledge_health():
    data = flask.request.get_json()
    conn, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    query = (
        "INSERT INTO health_history (login_id, has_fever, has_cough, has_tiredness, "
        "has_breath_shortness, has_headache, created_at, updated_at) VALUES ( "
        f"{data['login_id']}, '{data['has_fever']}', '{data['has_cough']}', "
        f"'{data['has_tiredness']}', '{data['has_breath_shortness']}', '{data['has_headache']}'"
        f"'{timestamp}', '{timestamp}')"
    )
    cursor.execute(query)
    conn.commit()
    return utils.make_response("{error: None}", 200)


@HEALTH_API.route('/check_acknowledgement', methods=["POST"])
def check_acknowledgement():
    data = flask.request.get_json()
    login_id = data['login_id']
    _, cursor = utils.get_database_connection()
    timestamp = utils.get_utc_timestamp_now()

    query = (
        "SELECT COUNT(*) FROM health_history"
        f"WHERE created_at::date = date {timestamp[:-9]} and login_id = {login_id}"
    )
    cursor.execute(query)
    count = cursor.fetchone()[0]
    if count:
        return utils.make_response("{error: None, data: 'true'}", 200)
    return utils.make_response("{error: None, data: 'true'}", 200)