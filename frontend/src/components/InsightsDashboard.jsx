import { useInsights } from '../hooks/useInsights'
import { useReceipts } from '../hooks/useReceipts'

function ScoreRing({ score }) {
  const pct = Math.min(100, Math.max(0, score || 0))
  const r = 38
  const circ = 2 * Math.PI * r
  const dash = (pct / 100) * circ
  const color = pct >= 70 ? '#10b981' : pct >= 40 ? '#f59e0b' : '#ef4444'

  return (
    <svg width="96" height="96" viewBox="0 0 96 96" className="-rotate-90">
      <circle cx="48" cy="48" r={r} fill="none" stroke="currentColor" strokeWidth="8"
        className="text-slate-100 dark:text-slate-700" />
      <circle cx="48" cy="48" r={r} fill="none" stroke={color} strokeWidth="8"
        strokeLinecap="round" strokeDasharray={`${dash} ${circ}`} />
    </svg>
  )
}

const CATEGORY_ICONS = {
  grocery: '🛒', dining: '🍽️', transport: '🚗', health: '💊',
  entertainment: '🎬', default: '📦',
}

export default function InsightsDashboard({ userId }) {
  const { health, loading: insightsLoading } = useInsights(userId)
  const { receipts, loading: receiptsLoading } = useReceipts(userId)

  // Build category totals from receipts
  const categoryTotals = receipts.reduce((acc, r) => {
    const cat = r.category || 'Other'
    acc[cat] = (acc[cat] || 0) + parseFloat(r.total_amount || 0)
    return acc
  }, {})
  const sortedCats = Object.entries(categoryTotals).sort((a, b) => b[1] - a[1])
  const totalSpend = sortedCats.reduce((s, [, v]) => s + v, 0)

  const score = health?.score ?? 0
  const notes = health?.notes ?? []
  const scoreLabel = score >= 70 ? 'Great' : score >= 40 ? 'Fair' : 'Needs work'
  const scoreColor = score >= 70 ? 'text-emerald-500' : score >= 40 ? 'text-amber-500' : 'text-red-500'

  return (
    <section className="space-y-4">
      {/* Score card */}
      <div className="flex items-center gap-5 rounded-3xl bg-white p-5 shadow-sm dark:bg-slate-800">
        <div className="relative flex shrink-0 items-center justify-center">
          <ScoreRing score={score} />
          <div className="absolute flex flex-col items-center">
            <span className={`text-xl font-extrabold ${scoreColor}`}>{score}</span>
            <span className="text-xs text-slate-400">/100</span>
          </div>
        </div>
        <div className="min-w-0">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">Health Score</p>
          <p className={`text-2xl font-extrabold ${scoreColor}`}>{scoreLabel}</p>
          <p className="mt-0.5 text-xs text-slate-400 dark:text-slate-500">
            {receipts.length} receipt{receipts.length !== 1 ? 's' : ''} analysed
          </p>
        </div>
      </div>

      {/* Spending by category */}
      {sortedCats.length > 0 && (
        <div className="rounded-3xl bg-white p-5 shadow-sm dark:bg-slate-800">
          <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">Spending by category</p>
          <ul className="space-y-3">
            {sortedCats.map(([cat, total]) => {
              const pct = totalSpend > 0 ? (total / totalSpend) * 100 : 0
              const icon = CATEGORY_ICONS[cat.toLowerCase()] ?? CATEGORY_ICONS.default
              return (
                <li key={cat}>
                  <div className="mb-1 flex items-center justify-between text-sm">
                    <span className="flex items-center gap-1.5 font-medium text-slate-700 dark:text-slate-200">
                      {icon} {cat}
                    </span>
                    <span className="text-slate-500 dark:text-slate-400">${total.toFixed(2)}</span>
                  </div>
                  <div className="h-1.5 w-full overflow-hidden rounded-full bg-slate-100 dark:bg-slate-700">
                    <div
                      className="h-full rounded-full bg-indigo-500 transition-all"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </li>
              )
            })}
          </ul>
        </div>
      )}

      {/* AI Notes */}
      {notes.length > 0 && (
        <div className="rounded-3xl bg-white p-5 shadow-sm dark:bg-slate-800">
          <p className="mb-3 text-xs font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">Recommendations</p>
          <ul className="space-y-2">
            {notes.map((note, i) => (
              <li key={i} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
                <span className="mt-0.5 shrink-0 text-indigo-500">•</span>
                {note}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Empty state */}
      {!insightsLoading && !receiptsLoading && receipts.length === 0 && (
        <div className="flex flex-col items-center gap-3 rounded-3xl bg-white px-6 py-12 text-center dark:bg-slate-800">
          <span className="text-5xl">📊</span>
          <p className="text-base font-semibold text-slate-700 dark:text-slate-200">No insights yet</p>
          <p className="text-sm text-slate-400 dark:text-slate-500">Upload receipts to see your spending insights</p>
        </div>
      )}
    </section>
  )
}
