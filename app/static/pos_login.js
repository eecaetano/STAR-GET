const video = document.getElementById('video');

async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    video.play();
  } catch (err) {
    console.error('Erro ao acessar a câmera:', err);
  }
}

// inicia automaticamente
window.addEventListener('load', startCamera);
