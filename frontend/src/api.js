const API_BASE_URL = (import.meta.env.VITE_API_URL || '/api').replace(/\/$/, '')

async function request(path, options) {
  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, options)
  } catch {
    throw new Error('Could not reach the crop disease API. Make sure the backend is running on port 8000.')
  }

  const payload = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = payload.detail
    const message = typeof detail === 'string'
      ? detail
      : detail?.[0]?.msg || payload.message || `Request failed (${response.status})`
    throw new Error(message)
  }
  return payload
}

export function analyzeLeaf(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request('/predict', { method: 'POST', body: formData })
}

export function getHealth() {
  return request('/health')
}
