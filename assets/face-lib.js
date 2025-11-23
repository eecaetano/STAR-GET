// assets/face-lib.js
export const FACE_API_CDN = "https://cdn.jsdelivr.net/npm/face-api.js@0.22.2/dist/face-api.min.js";

/**
 * loadFaceApiIfNeeded() - carrega face-api.js dinamicamente e os modelos.
 * modelsUrl: string URL relativa/absoluta onde os arquivos de modelo estão (ex: "/models")
 */
export async function loadFaceApiIfNeeded(modelsUrl="/models"){
  if(!window.faceapi){
    await import(FACE_API_CDN); // face-api define window.faceapi
  }
  // load models: tinyFaceDetector + faceRecognitionNet + faceLandmark68Net
  try{
    await faceapi.nets.tinyFaceDetector.loadFromUri(modelsUrl);
    await faceapi.nets.faceLandmark68Net.loadFromUri(modelsUrl);
    await faceapi.nets.faceRecognitionNet.loadFromUri(modelsUrl);
    return {ok:true, engine:'faceapi'};
  }catch(e){
    console.warn("Erro ao carregar modelos face-api:", e);
    return {ok:false, engine:'faceapi', error:e};
  }
}

/* store descriptors simply in localStorage as JSON array (for demo) */
const STORAGE_KEY = "starget_faces_v1";

export function saveDescriptor(descriptorObj){
  // descriptorObj = {id, name, descriptor: Float32Array}
  const raw = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  const entry = {
    id: descriptorObj.id ?? (Date.now()),
    name: descriptorObj.name,
    descriptor: Array.from(descriptorObj.descriptor),
    created: Date.now()
  };
  raw.push(entry);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(raw));
  return entry;
}

export function listDescriptors(){
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
}

export function clearDescriptors(){
  localStorage.removeItem(STORAGE_KEY);
}

/* convert face-api descriptor (Float32Array) to JS array and back helper */
export function descriptorFromFloat32(arr){
  if(Array.isArray(arr)) return new Float32Array(arr);
  return arr;
}

/* compare: Euclid distance */
export function euclideanDistance(a,b){
  let s=0;
  for(let i=0;i<a.length;i++){ const d=a[i]-b[i]; s += d*d; }
  return Math.sqrt(s);
}

/** findBestMatch */
export function findBestMatchProbe(probeDescriptor, threshold=0.45){
  const known = listDescriptors();
  if(!known.length) return {found:false, reason:'no-known'};
  let best = {idx:-1, dist: Infinity, item:null};
  for(let i=0;i<known.length;i++){
    const d = euclideanDistance(probeDescriptor, known[i].descriptor);
    if(d < best.dist){ best = {idx:i, dist:d, item:known[i]}; }
  }
  const ok = best.dist <= threshold;
  return {found: ok, best, threshold};
}
