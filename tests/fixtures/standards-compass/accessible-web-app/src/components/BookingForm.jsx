import { useId, useRef, useState } from 'react'

export default function BookingForm({ onSubmit }) {
  const nameId = useId()
  const dateId = useId()
  const errorId = useId()
  const [error, setError] = useState(null)
  const nameRef = useRef(null)

  function handleSubmit(e) {
    e.preventDefault()
    const name = e.target.elements[nameId].value
    if (!name) {
      setError('Enter the name the appointment is for.')
      nameRef.current.focus()
      return
    }
    setError(null)
    onSubmit({ name })
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <h2>Book an appointment</h2>

      {error && (
        <p id={errorId} role="alert" className="error">
          {error}
        </p>
      )}

      <label htmlFor={nameId}>Patient name</label>
      <input
        id={nameId}
        name={nameId}
        ref={nameRef}
        type="text"
        autoComplete="name"
        aria-invalid={error ? 'true' : undefined}
        aria-describedby={error ? errorId : undefined}
      />

      <label htmlFor={dateId}>Preferred date</label>
      <input id={dateId} name={dateId} type="date" />

      <button type="submit">Request appointment</button>
    </form>
  )
}
