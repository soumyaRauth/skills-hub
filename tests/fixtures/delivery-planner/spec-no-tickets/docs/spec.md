# Salon booking — spec

## Problem

Customers book appointments at a small hair salon by phone. The owner misses
calls while cutting hair, and double-books when two people call close together.

## Users

- **Customer**: books, sees and cancels their own appointments.
- **Owner**: sees the week, blocks out time, marks no-shows.

## What the first version does

1. A customer picks a service (cut, colour, cut and colour), a day and a free
   slot, enters name, email and phone, and gets a confirmation email.
2. A slot can be booked once. Two customers submitting the same slot at the
   same moment: one gets it, the other is told it has gone.
3. A customer can cancel from the link in the confirmation email.
4. The owner signs in and sees the week, with each booking's service and
   contact details.
5. The owner can block out a period (lunch, holiday); blocked slots are not
   offered.
6. The owner can mark a booking as a no-show.

## Opening hours

Tuesday to Saturday, 09:00–18:00. Slots are 30 minutes; a colour takes two
slots, cut and colour three.

## Not in the first version

Payments, deposits, SMS reminders, more than one stylist.

## Open questions

- Can a customer cancel on the day of the appointment?
- What happens to a customer's future bookings after a no-show?

## Stack

Node 20, Express, SQLite, deployed to a single small VPS.
