import { useEffect, useState } from 'react'
import { fetchHealthInsights } from '../services/api'

export function useInsights(userId) {
  const [health, setHealth] = useState({ score: 0, notes: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    async function load() {
      try {
        const data = await fetchHealthInsights(userId)
        if (mounted) setHealth(data)
      } catch {
        if (mounted) setHealth({ score: 0, notes: ['No insights yet'] })
      } finally {
        if (mounted) setLoading(false)
      }
    }
    load()
    return () => {
      mounted = false
    }
  }, [userId])

  return { health, loading }
}
