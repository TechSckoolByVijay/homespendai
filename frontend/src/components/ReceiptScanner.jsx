import { useState, useRef } from 'react'
import { uploadReceipt } from '../services/api'

export default function ReceiptScanner({ userId, onProcessed }) {
  const [status, setStatus] = useState('idle') // idle | uploading | success | error
  const [message, setMessage] = useState('')
  const cameraInputRef = useRef(null)
  const fileInputRef = useRef(null)

  async function handleFile(file) {
    if (!file) return
    setStatus('uploading')
    setMessage('')
    try {
      await uploadReceipt(userId, file)
      setStatus('success')
      setMessage('Receipt processed! Insights updated below.')
      onProcessed?.()
    } catch (err) {
      setStatus('error')
      setMessage(err?.message || 'Upload failed. Please try again.')
    }
  }

  const isMobile = /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent)

  return (
    <section className="space-y-5">
      {/* Hero scan card */}
      <div className="overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-600 to-violet-600 p-px shadow-xl shadow-indigo-200 dark:shadow-indigo-900/40">
        <div className="rounded-3xl bg-gradient-to-br from-indigo-600 to-violet-600 px-6 pb-8 pt-8 text-center text-white">
          <div className="mx-auto mb-4 flex h-20 w-20 items-center justify-center rounded-full bg-white/20 text-4xl shadow-inner">
            📷
          </div>
          <h2 className="mb-1 text-2xl font-extrabold tracking-tight">Scan Receipt</h2>
          <p className="mb-6 text-sm text-indigo-200">
            {isMobile
              ? 'Tap to open your camera and capture a receipt'
              : 'Click to pick a receipt image or PDF from your computer'}
          </p>

          {/* Hidden inputs */}
          {/* Mobile: camera with capture */}
          <input
            ref={cameraInputRef}
            type="file"
            accept="image/*"
            capture="environment"
            className="hidden"
            onChange={e => handleFile(e.target.files?.[0])}
          />
          {/* Desktop / fallback: file picker without capture */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,.pdf"
            className="hidden"
            onChange={e => handleFile(e.target.files?.[0])}
          />

          <button
            disabled={status === 'uploading'}
            onClick={() => isMobile
              ? cameraInputRef.current?.click()
              : fileInputRef.current?.click()
            }
            className="w-full rounded-2xl bg-white py-4 text-base font-bold text-indigo-700
              shadow-md transition active:scale-95 disabled:opacity-60
              hover:bg-indigo-50 disabled:cursor-not-allowed"
          >
            {status === 'uploading' ? '⏳  Processing…' : isMobile ? '📷  Open Camera' : '📁  Choose File'}
          </button>
        </div>
      </div>

      {/* Divider with OR */}
      {isMobile && (
        <div className="flex items-center gap-3 text-xs text-slate-400 dark:text-slate-500">
          <span className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
          or upload from gallery
          <span className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
        </div>
      )}

      {/* Upload from file on mobile too */}
      {isMobile && (
        <button
          disabled={status === 'uploading'}
          onClick={() => fileInputRef.current?.click()}
          className="w-full rounded-2xl border-2 border-dashed border-slate-300 bg-white py-4 text-sm font-semibold
            text-slate-600 transition hover:border-indigo-400 hover:text-indigo-600
            dark:border-slate-600 dark:bg-slate-800 dark:text-slate-300 dark:hover:border-indigo-400
            disabled:opacity-60"
        >
          🖼️  Upload from Gallery / PDF
        </button>
      )}

      {/* Status feedback */}
      {status === 'success' && (
        <div className="flex items-start gap-3 rounded-2xl bg-emerald-50 p-4 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
          <span className="text-xl">✅</span>
          <div>
            <p className="font-semibold">Success!</p>
            <p className="text-sm">{message}</p>
          </div>
        </div>
      )}
      {status === 'error' && (
        <div className="flex items-start gap-3 rounded-2xl bg-red-50 p-4 text-red-700 dark:bg-red-900/30 dark:text-red-400">
          <span className="text-xl">❌</span>
          <div>
            <p className="font-semibold">Upload failed</p>
            <p className="text-sm">{message}</p>
          </div>
        </div>
      )}

      {/* Info card */}
      <div className="rounded-2xl bg-white p-4 dark:bg-slate-800">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-500">What happens next</p>
        <ol className="space-y-2 text-sm text-slate-600 dark:text-slate-300">
          {['Receipt stored in Azure Blob Storage', 'OCR extracts items & totals', 'AI categorises your spending', 'Insights generated automatically'].map((step, i) => (
            <li key={i} className="flex items-center gap-2">
              <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-xs font-bold text-indigo-700 dark:bg-indigo-900/50 dark:text-indigo-400">{i + 1}</span>
              {step}
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
