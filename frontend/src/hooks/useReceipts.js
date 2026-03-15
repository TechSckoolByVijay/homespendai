import { useEffect, useState } from 'react'
import { fetchReceipts } from '../services/api'

export function useReceipts(userId) {
  const [receipts, setReceipts] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true
    async function load() {
      setLoading(true)
      try {
        const data = await fetchReceipts(userId)
        if (mounted) setReceipts(data)
      } catch {
        if (mounted) setReceipts([])
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [userId])

  return { receipts, loading }
}
