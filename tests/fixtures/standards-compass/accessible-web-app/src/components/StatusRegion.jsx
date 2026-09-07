export default function StatusRegion({ message }) {
  return (
    <p role="status" aria-live="polite" className="status">
      {message}
    </p>
  )
}
