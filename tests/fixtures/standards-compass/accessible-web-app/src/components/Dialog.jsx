import { useEffect, useRef } from 'react'

export default function Dialog({ open, title, onClose, children }) {
  const ref = useRef(null)
  const previouslyFocused = useRef(null)

  useEffect(() => {
    if (!open) return
    previouslyFocused.current = document.activeElement
    ref.current?.showModal()
    ref.current?.querySelector('button, [href], input, select, textarea')?.focus()
    return () => previouslyFocused.current?.focus()
  }, [open])

  return (
    <dialog ref={ref} aria-labelledby="dialog-title" onClose={onClose}>
      <h2 id="dialog-title">{title}</h2>
      {children}
      <button type="button" onClick={onClose}>
        Close
      </button>
    </dialog>
  )
}
