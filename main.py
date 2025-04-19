from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import io
from pydub import AudioSegment

app = Flask(__name__)
chuyenkhoan = []

@app.route('/webhook', methods=['POST'])
def webhook():
    # Lấy dữ liệu JSON gửi đến
    data = request.get_json()
    
    # In dữ liệu nhận được ra console (hoặc xử lý theo nhu cầu)
    print("Received webhook data:", data)

    chuyenkhoan.append(data)
    
    # Trả về phản hồi JSON cho phía gửi
    return jsonify({"status": "success"}), 200

@app.route('/currentCK', methods=['GET'])
def currentCK():
    # Trả về số lượng chuyển khoản hiện tại
    return jsonify({"currentCK": len(chuyenkhoan)}), 200


@app.route('/lastCK', methods=['GET'])
def lastCK():
    # trả về chuyển khoản cuối cùng
    if len(chuyenkhoan) == 0:
        return jsonify({"status": "no data"}), 404
    
    last_transaction = chuyenkhoan[-1]
    return jsonify(last_transaction), 200

# giao dien index kiem tra danh sach chuyen khoan
@app.route('/chuyenkhoan', methods=['GET'])
def get_chuyenkhoan():
    # Trả về danh sách chuyển khoản dưới dạng JSON
    return jsonify(chuyenkhoan), 200

# Giao diện chính
@app.route('/')
def index():
    return '''
    <h1>Chuyển Khoản</h1>
    <p>Để xem danh sách chuyển khoản, hãy truy cập <a href="/chuyenkhoan">/chuyenkhoan</a></p>
    '''
@app.route('/tts',methods=['GET'])
def tts():
    text = request.args.get('text', '').strip()
    if not text: 
        return jsonify({"status":"no text"}), 400
    try:
        tts = gTTS(text=text, lang='vi')
        mp3_buffer = io.BytesIO()
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)  


        sound = AudioSegment.from_file(mp3_buffer, format="mp3")
        loudsound = sound + 30

        output_buffer = io.BytesIO()
        loudsound.export(output_buffer, format="mp3")
        output_buffer.seek(0)
        return send_file(output_buffer, mimetype='audio/mpeg', as_attachment=False, download_name='output.mp3')  
    except:
        return jsonify({"status":"error"}), 500



if __name__ == '__main__':
    app.run(port=7860, host='0.0.0.0', debug=True)
