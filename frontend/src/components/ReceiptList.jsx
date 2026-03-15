import { useState } from 'react'
import { useReceipts } from '../hooks/useReceipts'

const CATEGORY_COLORS = {
  grocery: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400',
  dining: 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-400',
  transport: 'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400',
  health: 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400',
  entertainment: 'bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-400',
  default: 'bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300',
}

function formatDate(raw) {
  if (!raw) return 'Unknown date'
  try { return new Date(raw).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) }
  catch { return raw }
}

function formatCurrency(amount) {
  const n = parseFloat(amount)
  return isNaN(n) ? '—' : `$${n.toFixed(2)}`
}

function SkeletonCard() {
  return (
    <div className="animate-pulse rounded-2xl bg-white p-4 dark:bg-slate-800">
      <div className="mb-2 h-4 w-1/2 rounded bg-slate-200 dark:bg-slate-700" />
      <div className="h-3 w-1/3 rounded bg-slate-100 dark:bg-slate-700" />
    </div>
  )
}

export default function ReceiptList({ userId }) {
  const { receipts, loading } = useReceipts(userId)
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="space-y-3">
      {loading && [1, 2, 3].map(i => <SkeletonCard key={i} />)}

      {!loading && receipts.length === 0 && (
        <div className="flex flex-col items-center gap-3 rounded-3xl bg-white px-6 py-14 text-center dark:bg-slate-800">
          <span className="text-5xl">🧾</span>
          <p className="text-base font-semibold text-slate-700 dark:text-slate-200">No receipts yet</p>
          <p className="text-sm text-slate-400 dark:text-slate-500">Scan or upload your first receipt to get started</p>
        </div>
      )}

      {!loading && receipts.map((receipt) => {
        const category = receipt.category?.toLowerCase() || 'default'
        const colorClass = CATEGORY_COLORS[category] ?? CATEGORY_COLORS.default
        const isOpen = expanded === receipt.id
        const items = receipt.items ?? []

        return (
          <article
            key={receipt.id}
            className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-slate-100 dark:bg-slate-800 dark:ring-slate-700"
          >
            <button
              onClick={() => setExpanded(isOpen ? null : receipt.id)}
              className="flex w-full items-center gap-3 p-4 text-left"
            >
              {/* Store icon */}
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-indigo-50 text-xl dark:bg-indigo-900/30">
                🏪
              </div>
              <div className="min-w-0 flex-1">
                <p className="truncate font-semibold text-slate-800 dark:text-slate-100">
                  {receipt.store_name || 'Unknown Store'}
                </p>
                <p className="text-xs text-slate-400 dark:text-slate-500">{formatDate(receipt.purchase_date)}</p>
              </div>
              <div className="flex shrink-0 flex-col items-end gap-1">
                <span className="text-base font-bold text-slate-800 dark:text-slate-100">
                  {formatCurrency(receipt.total_amount)}
                </span>
                {receipt.category && (
                  <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${colorClass}`}>
                    {receipt.category}
                  </span>
                )}
              </div>
              <span className="ml-1 text-slate-400">{isOpen ? '▲' : '▽'}</span>
            </button>

            {/* Expanded items */}
            {isOpen && items.length > 0 && (
              <div className="border-t border-slate-100 px-4 pb-4 pt-2 dark:border-slate-700">
                <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">Items</p>
                <ul className="space-y-1">
                  {items.map((item, idx) => (
                    <li key={idx} className="flex justify-between text-sm text-slate-600 dark:text-slate-300">
                      <span>{item.name || item.description || 'Item'}</span>
                      <span>{formatCurrency(item.price ?? item.amount)}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </article>
        )
      })}
    </div>
  )
}
