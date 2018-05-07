from flask import Flask, render_template, request, jsonify, send_file, make_response

app = Flask(__name__)

@app.route('/files/<path>/<filename>')
def test(path, filename):

    # response = make_response(send_file('/home/ej/변성윤.txt'))
    #
    # basename = os.path.base_name

    print(request.url)

    print(path, filename)

    return send_file('/home/ej/byeon.txt', as_attachment=True, mimetype='text/csv; charset=x-EBCDIC-KoreanAndKoreanExtended'
)

if __name__=='__main__':

    app.run(host='0.0.0.0')
