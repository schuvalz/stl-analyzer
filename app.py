from flask import Flask, request, jsonify
from stl import mesh
import os
import tempfile

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_stl():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    try:
        # 안전하게 하드디스크에 임시 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.stl') as temp:
            file.save(temp.name)
            temp_path = temp.name

        # numpy-stl 라이브러리로 STL 분석 (에러 확률 0%)
        stl_mesh = mesh.Mesh.from_file(temp_path)

        # X, Y, Z 크기 계산
        bounds = stl_mesh.max_ - stl_mesh.min_
        
        # 부피 계산
        volume, cog, inertia = stl_mesh.get_mass_properties()
        
        # 표면적 계산
        surface_area = stl_mesh.areas.sum()

        # 다 쓴 파일은 삭제
        os.remove(temp_path)

        return jsonify({
            "x": round(float(bounds[0]), 2),
            "y": round(float(bounds[1]), 2),
            "z": round(float(bounds[2]), 2),
            "volume": round(float(volume), 2),
            "surface_area": round(float(surface_area), 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
