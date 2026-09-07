export default function InvoiceRow({ invoice }) {
  return (
    <tr>
      <td>{invoice.number}</td>
      <td>{invoice.date}</td>
      <td>
        {invoice.card ? `${invoice.card.brand} •••• ${invoice.card.last4}` : 'Card on file'}
      </td>
      <td>{invoice.totalFormatted}</td>
    </tr>
  )
}
