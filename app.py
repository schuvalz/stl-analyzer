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
        # 1. 파일 데이터를 메모리에 읽어들임
        file_bytes = io.BytesIO(file.read())
        
        # 2. trimesh.load 를 사용하되, 명확하게 stl 파일임을 지정
        # (load_mesh가 아니라 load가 맞습니다. 제 실수입니다.)
        mesh = trimesh.load(file_bytes, file_type='stl')

        # 3. 5가지 값 계산
        # STL 파일이 여러 개의 파트로 나뉘어 있을 수 있으므로 통합된 geometry를 사용
        if isinstance(mesh, trimesh.Scene):
            geometry = mesh.dump(concatenate=True)
        else:
            geometry = mesh

        bounds = geometry.extents  # [X, Y, Z]
        volume = geometry.volume   # 부피
        area = geometry.area       # 표면적

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
