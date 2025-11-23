README.md — STAR-GET
🚀 STAR-GET

Sistema demonstrativo de cadastro biométrico, reconhecimento facial e simulação de porta automatizada, totalmente executado no navegador, sem necessidade de backend.

Este projeto foi desenvolvido como prova de conceito para uso educacional e institucional, apresentando um fluxo completo:

📥 Cadastro do usuário
Captura de imagem via webcam, geração de descritor facial ou hash (fallback) e armazenamento local.

🔍 Teste de Reconhecimento
Compara o rosto capturado com os descritores salvos.

🚪 Simulação de Porta
Interface animada que “abre” a porta quando o reconhecimento é autorizado.

🧠 Tecnologias Utilizadas

HTML5 / CSS3 (Flexbox + Grid + Glass UI)

JavaScript moderno (ES6 Modules)

face-api.js para detecção facial no frontend

IndexedDB / LocalStorage para armazenamento no navegador

Web Audio API para sons de feedback

Layout responsivo para desktop e mobile

📂 Estrutura do Projeto
/
├── index.html
├── cadastro.html
├── test.html
├── door.html
├── assets/
│   ├── styles.css
│   ├── face-lib.js
│   └── logo.png
└── models/
    ├── tiny_face_detector_model-weights_manifest.json
    ├── face_recognition_model-weights_manifest.json
    ├── face_landmark_68_model-weights_manifest.json
    └── (arquivos .bin dos modelos)
