from flask import Flask, request, jsonify
import trimesh
import os
import tempfile

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_stl():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    try:
        # 가장 확실한 방법: 메모리(BytesIO)가 아닌 임시 파일로 하드디스크에 직접 저장 후 로드
        with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as temp:
            file.save(temp.name)
            temp_path = temp.name

        # 임시 파일 경로를 주어 trimesh 내부 버그 원천 차단
        mesh = trimesh.load(temp_path)

        # 5가지 값 계산
        if isinstance(mesh, trimesh.Scene):
            geometry = mesh.dump(concatenate=True)
        else:
            geometry = mesh

        bounds = geometry.extents  # [X, Y, Z]
        volume = geometry.volume   # 부피
        area = geometry.area       # 표면적

        # 사용한 임시 파일은 서버 용량을 위해 삭제
        os.remove(temp_path)

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
