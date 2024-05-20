from flask import Flask, request, jsonify
from databasemanager import DatabaseManager

app = Flask(__name__)

database_context = DatabaseManager("teste")

@app.route("/cliente", methods=["GET"])
def get_cliente():
    try:
        clientes_rows = database_context.get_table("clientes")
        rows_data = []
        for row in clientes_rows:
            row_data = {
                "id_cliente": row[0],
                "nome": row[1],
                "morada": row[2],
                "telefone": row[3]
            }
            rows_data.append(row_data)
        return jsonify(rows_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)