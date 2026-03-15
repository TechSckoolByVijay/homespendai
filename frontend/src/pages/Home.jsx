import { useState } from 'react'
import ReceiptScanner from '../components/ReceiptScanner'
import InsightsDashboard from '../components/InsightsDashboard'

export default function Home({ user, onSignUp }) {
  const [hasProcessedReceipt, setHasProcessedReceipt] = useState(false)
  const [email, setEmail] = useState('')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [saved, setSaved] = useState(false)

  async function handleSave(e) {
    e.preventDefault()
    if (!email) return
    setSaving(true)
    setError('')
    try {
      await onSignUp(email)
      setSaved(true)
    } catch (err) {
      setError(err?.message || 'Could not sign up right now.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="space-y-5">
      <ReceiptScanner
        userId={user.user_id}
        onProcessed={() => setHasProcessedReceipt(true)}
      />

      {hasProcessedReceipt && (
        <>
          <div className="rounded-2xl bg-white p-4 shadow-sm dark:bg-slate-800">
            <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">Receipt processed</p>
            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">Showing latest insights for this session.</p>
          </div>
          <InsightsDashboard userId={user.user_id} />
        </>
      )}

      {hasProcessedReceipt && user.isGuest && !saved && (
        <div className="rounded-3xl border border-indigo-100 bg-indigo-50 p-5 shadow-sm dark:border-indigo-900/40 dark:bg-indigo-900/20">
          <p className="text-base font-bold text-indigo-900 dark:text-indigo-200">Save your data – sign up</p>
          <p className="mt-1 text-sm text-indigo-700 dark:text-indigo-300">
            Create your profile to keep receipts and analytics tied to your account.
          </p>
          <form onSubmit={handleSave} className="mt-4 flex gap-2">
            <input
              type="email"
              required
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="min-w-0 flex-1 rounded-xl border border-indigo-200 bg-white px-3 py-2 text-sm outline-none ring-indigo-500 focus:ring dark:border-indigo-700 dark:bg-slate-900 dark:text-slate-100"
            />
            <button
              type="submit"
              disabled={saving}
              className="shrink-0 rounded-xl bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-60"
            >
              {saving ? 'Saving…' : 'Sign up'}
            </button>
          </form>
          {error && <p className="mt-2 text-xs text-red-500">{error}</p>}
        </div>
      )}

      {saved && (
        <div className="rounded-2xl bg-emerald-50 p-4 text-sm text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
          ✅ Your profile is ready. New receipts will now be saved to your account.
        </div>
      )}
    </section>
  )
}
