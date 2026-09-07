import { render, screen } from '@testing-library/react'
import BookingForm from '../BookingForm'

test('every field has an accessible name', () => {
  render(<BookingForm onSubmit={() => {}} />)
  expect(screen.getByLabelText('Patient name')).toBeTruthy()
  expect(screen.getByLabelText('Preferred date')).toBeTruthy()
})
