const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

export async function registerUser(email, currentUserId = null) {
  const response = await fetch(`${BASE_URL}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, current_user_id: currentUserId })
  })
  if (!response.ok) throw new Error('Failed to register user')
  return response.json()
}

export async function fetchReceipts(userId) {
  const response = await fetch(`${BASE_URL}/receipts?user_id=${userId}`)
  if (!response.ok) throw new Error('Failed to fetch receipts')
  return response.json()
}

export async function uploadReceipt(userId, file) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/receipts/upload?user_id=${userId}`, {
    method: 'POST',
    body: formData
  })

  if (!response.ok) {
    let detail = 'Failed to upload receipt'
    try {
      const data = await response.json()
      detail = data?.detail || detail
    } catch {
      // ignore parse errors and keep default message
    }
    throw new Error(detail)
  }
  return response.json()
}

export async function fetchHealthInsights(userId) {
  const response = await fetch(`${BASE_URL}/insights/health?user_id=${userId}`)
  if (!response.ok) throw new Error('Failed to fetch insights')
  return response.json()
}
