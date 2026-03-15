export default function UploadButton({ onSelectFile }) {
  return (
    <label className="inline-flex w-full cursor-pointer items-center justify-center rounded-2xl bg-emerald-600 px-4 py-3 text-white shadow-sm">
      <span className="font-semibold">Upload Receipt</span>
      <input type="file" accept="image/*,.pdf" className="hidden" onChange={(e) => onSelectFile?.(e.target.files?.[0])} />
    </label>
  )
}
