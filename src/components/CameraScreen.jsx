import React, { useRef, useEffect, useState } from 'react';

export default function CameraScreen({ setScreen, setIngredients }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [detected, setDetected] = useState([]);

  useEffect(() => {
    async function startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        alert('카메라 접근 실패: ' + err.message);
        setScreen('input');
      }
    }

    startCamera();

    return () => {
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
      }
    };
  }, [setScreen]);

  const captureAndDetect = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (video && canvas) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/png'));
      const formData = new FormData();
      formData.append('image', blob, `captured_${Date.now()}.png`);

      try {
        const res = await fetch('http://localhost:8000/upload-and-detect', {
          method: 'POST',
          body: formData,
        });
        const result = await res.json();
        setDetected(result.unique_objects);
        alert('감지된 재료: ' + result.unique_objects.join(', '));

        // 선택 사항: 기존 재료에 추가
        if (setIngredients) {
          setIngredients((prev) => [...new Set([...prev, ...result.unique_objects])]);
        }

      } catch (err) {
        alert('감지 실패: ' + err.message);
      }
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>카메라 화면</h2>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        style={{ width: '100%', borderRadius: '10px' }}
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />

      <button onClick={captureAndDetect} style={{ marginTop: 10 }}>
        📸 촬영 및 감지
      </button>

      <button onClick={() => setScreen('input')} style={{ marginTop: 10 }}>
        ← 돌아가기
      </button>

      {detected.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <strong>감지된 재료:</strong>
          <ul>
            {detected.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
