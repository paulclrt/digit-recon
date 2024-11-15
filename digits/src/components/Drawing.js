import React, { useEffect, useRef } from 'react';
import "./Drawing.css"

function Drawing({dataToParent}) {
  const canvasRef = useRef(null);
  const isPaintingRef = useRef(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.lineWidth = 2;
      ctx.lineCap = 'round';

      // Set canvas size to 28x28 pixels for drawing (this is the actual size)
      canvas.width = 28;
      canvas.height = 28;
      canvas.style.border = '2px solid black';

      // Calculate scaling factor (actual size vs display size)
      const scale = 280 / 28;

      const handleMouseDown = (e) => {
        const rect = canvas.getBoundingClientRect();
        isPaintingRef.current = true;
        
        // Calculate scaled mouse coordinates
        const scaledX = (e.clientX - rect.left) / scale;
        const scaledY = (e.clientY - rect.top) / scale;

        ctx.beginPath();
        ctx.moveTo(scaledX, scaledY);
      };
      
      const handleMouseMove = (e) => {
        if (!isPaintingRef.current) return;
        const rect = canvas.getBoundingClientRect();
        
        // Calculate scaled mouse coordinates
        const scaledX = (e.clientX - rect.left) / scale;
        const scaledY = (e.clientY - rect.top) / scale;

        ctx.lineTo(scaledX, scaledY);
        ctx.stroke();
      };
      
      const handleMouseUp = () => {
        isPaintingRef.current = false;
        ctx.stroke();
        ctx.beginPath();
      };

      canvas.addEventListener('mousedown', handleMouseDown);
      canvas.addEventListener('mousemove', handleMouseMove);
      canvas.addEventListener('mouseup', handleMouseUp);
      canvas.addEventListener('mouseleave', handleMouseUp);

      return () => {
        canvas.removeEventListener('mousedown', handleMouseDown);
        canvas.removeEventListener('mousemove', handleMouseMove);
        canvas.removeEventListener('mouseup', handleMouseUp);
        canvas.removeEventListener('mouseleave', handleMouseUp);
      };
    }
  }, []);
  const exportAs28x28 = async () => {
    const canvas = canvasRef.current;

    // Convert canvas to image (base64 encoded PNG)
    const dataURL = canvas.toDataURL('image/png');
    console.log(dataURL)

    // Create FormData to send image as file in a POST request
    const formData = new FormData();
    const byteArray = Uint8Array.from(atob(dataURL.split(',')[1]), c => c.charCodeAt(0));
    const blob = new Blob([byteArray], { type: 'image/png' });

    formData.append('image', blob, 'image.png');

    try {
      const response = await fetch('/api/analyzeimage', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload image');
      }

      const result = await response.json();
      console.log('Model Result:', result);
      dataToParent(result)

      // Handle result (e.g., show feedback to user)
    } catch (error) {
      console.error('Error uploading image:', error);
    }
  };


  function clearCanva() {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  return (
    <div className="drawingbox">
      <canvas ref={canvasRef} style={{ width: '280px', height: '280px' }}></canvas>
      <div className='buttons'>
        <button  onClick={exportAs28x28}>Send to AI</button>
        <button  onClick={clearCanva}>Clear Canva</button>
      </div>
    </div>
  );
}

export default Drawing;
