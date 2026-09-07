export default function AppointmentList({ appointments, onCancel }) {
  if (appointments.length === 0) {
    return <p>You have no upcoming appointments.</p>
  }

  return (
    <table>
      <caption>Your upcoming appointments</caption>
      <thead>
        <tr>
          <th scope="col">Date</th>
          <th scope="col">Clinician</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        {appointments.map((a) => (
          <tr key={a.id}>
            <td>
              <time dateTime={a.startsAt}>{a.readableDate}</time>
            </td>
            <td>{a.clinician}</td>
            <td>
              <button type="button" onClick={() => onCancel(a.id)}>
                Cancel<span className="sr-only"> appointment on {a.readableDate}</span>
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
