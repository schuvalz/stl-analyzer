from flask import Flask, request, jsonify
import trimesh
import io

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_stl():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    try:
        # 파일을 읽어 3D 형상(trimesh)으로 변환
        mesh = trimesh.load(file, file_type='stl')

        # 5가지 값 계산
        bounds = mesh.extents  # [X, Y, Z]
        volume = mesh.volume   # 부피
        area = mesh.area       # 표면적

        # 결과를 JSON 형태로 반환
        return jsonify({
            "x": round(float(bounds[0]), 2),
            "y": round(float(bounds[1]), 2),
            "z": round(float(bounds[2]), 2),
            "volume": round(float(volume), 2),
            "surface_area": round(float(area), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
