import { useState, useEffect } from 'react'
import { Link, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import Home from './pages/Home'
import Receipts from './pages/Receipts'
import Insights from './pages/Insights'
import { registerUser } from './services/api'

const NAV = [
  { to: '/', label: 'Scan', icon: '📷' },
  { to: '/receipts', label: 'Receipts', icon: '🧾' },
  { to: '/insights', label: 'Insights', icon: '📊' },
]

export default function App() {
  const [dark, setDark] = useState(() =>
    window.matchMedia('(prefers-color-scheme: dark)').matches
  )

  function createGuestUser() {
    const id = (window.crypto?.randomUUID?.() || `${Date.now()}-${Math.random()}`)
    return {
      user_id: id,
      email: null,
      isGuest: true,
    }
  }

  const [user, setUser] = useState(() => {
    try {
      const raw = localStorage.getItem('expense_user')
      return raw ? JSON.parse(raw) : createGuestUser()
    } catch {
      return createGuestUser()
    }
  })
  const location = useLocation()

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
  }, [dark])

  useEffect(() => {
    if (user) {
      localStorage.setItem('expense_user', JSON.stringify(user))
    }
  }, [user])

  async function signUp(email) {
    const registered = await registerUser(email.trim().toLowerCase())
    setUser({ ...registered, isGuest: false })
    return registered
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-900 dark:text-slate-100">
      <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/80 backdrop-blur dark:border-slate-700 dark:bg-slate-900/80">
        <div className="mx-auto flex max-w-lg items-center justify-between px-4 py-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">🧾</span>
            <h1 className="text-base font-bold tracking-tight">Receipt Intelligence</h1>
          </div>
          <div className="flex items-center gap-2">
            <span className="max-w-36 truncate rounded-full bg-slate-100 px-2.5 py-1 text-xs text-slate-600 dark:bg-slate-800 dark:text-slate-300">
              {user?.isGuest ? 'Guest mode' : user?.email}
            </span>
            <button
              onClick={() => setDark(d => !d)}
              className="rounded-full p-2 text-lg transition hover:bg-slate-100 dark:hover:bg-slate-800"
              aria-label="Toggle dark mode"
            >
              {dark ? '☀️' : '🌙'}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-lg px-4 pb-24 pt-5">
        <Routes>
          <Route path="/" element={<Home user={user} onSignUp={signUp} />} />
          <Route path="/receipts" element={<Receipts userId={user.user_id} />} />
          <Route path="/insights" element={<Insights userId={user.user_id} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>

      <nav className="fixed bottom-0 left-0 right-0 z-10 border-t border-slate-200 bg-white/90 backdrop-blur dark:border-slate-700 dark:bg-slate-900/90">
        <div className="mx-auto grid max-w-lg grid-cols-3">
          {NAV.map(({ to, label, icon }) => {
            const active = location.pathname === to
            return (
              <Link
                key={to}
                to={to}
                className={`flex flex-col items-center gap-0.5 py-2.5 text-xs font-medium transition-colors
                  ${active
                    ? 'text-indigo-600 dark:text-indigo-400'
                    : 'text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-100'
                  }`}
              >
                <span className="text-lg leading-none">{icon}</span>
                {label}
                {active && (
                  <span className="mt-0.5 h-0.5 w-4 rounded-full bg-indigo-600 dark:bg-indigo-400" />
                )}
              </Link>
            )
          })}
        </div>
      </nav>
    </div>
  )
}
